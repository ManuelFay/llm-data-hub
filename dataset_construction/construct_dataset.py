"""This code is used to aggregate all of the datasets needed to construct a pretraining dataset from a YAML config file."""

import argparse
import os
import random
from typing import Any, Callable, Dict, Optional, Tuple

import configue
import datasets
import pandas as pd
import tqdm
from transformers import PreTrainedTokenizer, AutoTokenizer
from datasets import Dataset, DatasetDict, concatenate_datasets, load_dataset
from huggingface_hub import HfApi

from dataset_construction.dataset_config import DataMix, DatasetConfig
from dataset_construction.utils import test_set_conformity


class DatasetConstructor:
    def __init__(self, mix, estimate_from_k: Optional[int] = None):
        self.mix = mix
        self.estimate_from_k = estimate_from_k

    def process_single_dataset(
        self,
        dataset: Dataset,
        dataset_key: str,
        filtering_function: Optional[Callable],
        preprocessing_function: Optional[Callable] = None,
    ) -> Dataset:
        """Filter and truncate a dataset, if needed."""

        if preprocessing_function is not None:
            dataset = dataset.map(preprocessing_function, num_proc=os.cpu_count())

        if filtering_function is not None:
            dataset = dataset.filter(filtering_function, num_proc=os.cpu_count())

        # Do it only if needed
        dataset = dataset.cast_column("id", datasets.Value(dtype="string", id=None))
        # dataset = dataset.cast_column("text", datasets.Value(dtype="string", id=None))
        dataset = dataset.add_column("dataset_id", [f"{dataset_key}"] * len(dataset))
        return dataset

    def build_single_dataset_dict(self, dataset_config: DatasetConfig) -> DatasetDict:
        """Load a single dataset from HF Datasets Hub, and apply the filtering function if provided."""
        # TODO: load partial dataset only if num_train is specified using HF datasets terminology [:n
        dataset_train = load_dataset(
            dataset_config.dataset_path,
            name=dataset_config.dataset_name,
            split=dataset_config.train_split,
            num_proc=os.cpu_count(),
            **dataset_config.dataset_kwargs
        )
        assert isinstance(dataset_train, Dataset)

        if dataset_config.build_test_set_from_train:
            print(f"Building test set from train set for {dataset_config.dataset_path} with len {len(dataset_train)}")
            num_test_set = test_set_conformity(dataset_train, dataset_config.num_test_examples)
            dataset_train_test = dataset_train.train_test_split(test_size=num_test_set)
            if dataset_config.num_train_examples:
                dataset_train = dataset_train_test["train"].select(range(dataset_config.num_train_examples))
            else:
                dataset_train = dataset_train_test["train"]
            dataset_test = dataset_train_test["test"]
        elif dataset_config.test_split is not None:
            print(f"Loading test set for {dataset_config.dataset_path} with len {dataset_config.num_test_examples}")
            if dataset_config.num_train_examples:
                dataset_train = dataset_train.select(range(dataset_config.num_train_examples))
            dataset_test = load_dataset(
                dataset_config.dataset_path,
                name=dataset_config.dataset_name,
                split=dataset_config.test_split,
                num_proc=os.cpu_count(),
                **dataset_config.dataset_kwargs
            )
            dataset_test = dataset_test.select(range(min(dataset_config.num_test_examples, len(dataset_test))))
        else:
            raise ValueError("Either build_test_set_from_train or test_split must be set")
        assert isinstance(dataset_test, Dataset)
        assert isinstance(dataset_train, Dataset)

        if dataset_config.text_column != "text":
            dataset_train = dataset_train.rename_column(dataset_config.text_column, "text")
            dataset_test = dataset_test.rename_column(dataset_config.text_column, "text")
        if dataset_config.id_column != "id":
            dataset_train = dataset_train.rename_column(dataset_config.id_column, "id")
            dataset_test = dataset_test.rename_column(dataset_config.id_column, "id")

        dataset_train = self.process_single_dataset(
            dataset_train,
            dataset_config.dataset_key,
            dataset_config.filtering_function,
            dataset_config.preprocessing_function,
        )
        dataset_test = self.process_single_dataset(
            dataset_test,
            dataset_config.dataset_key,
            dataset_config.filtering_function,
            dataset_config.preprocessing_function,
        )
        dataset = DatasetDict({"train": dataset_train, "test": dataset_test})

        dataset = dataset.remove_columns(list(set(dataset_train.column_names) - {"id", "text", "dataset_id"}))
        assert set(dataset["train"].column_names) == {"id", "text", "dataset_id"}, f"Mismatch in column names {dataset['train'].column_names}"
        return dataset

    def compute_dataset_stats(self,
                              dataset: Dataset,
                              tokenizer: Optional[PreTrainedTokenizer] = None) -> Dict[str, Any]:
        """Compute some stats about a dataset."""

        # Assume uniform distribution
        if self.estimate_from_k and len(dataset) > self.estimate_from_k:
            # idxs = random.choices(range(len(dataset)), k=100)
            idxs = range(self.estimate_from_k)
            ds_estimate = dataset.select(idxs)
        else:
            ds_estimate = dataset

        word_counts = [len(example["text"].split()) for example in ds_estimate]
        stats = {
            "num_examples": len(dataset),
            "num_words": len(dataset)*sum(word_counts)/len(word_counts),
            "word_distribution": word_counts,
            "dataset_gb": round(dataset.data.nbytes / 1e9, 3),
        }

        if tokenizer:
            def tok_and_count(example):
                encodings = tokenizer(example['text'],  return_tensors="np")
                return {"input_len": encodings["input_ids"].shape[1]}

            tok_counts = ds_estimate.map(tok_and_count, num_proc=os.cpu_count())["input_len"]
            stats.update({
                "num_tokens": len(dataset)*sum(tok_counts)/len(tok_counts),
                "token_distribution": tok_counts,
            })
        return stats

    def build_concatenated_dataset(self) -> Tuple[DatasetDict, DatasetDict]:
        dataset_list = []
        for dataset_config in tqdm.tqdm(self.mix.datasets, desc="Loading datasets"):
            print(f"Loading and filtering dataset {dataset_config.dataset_path}")
            ds: DatasetDict = self.build_single_dataset_dict(dataset_config)
            dataset_list.append(ds)

        final_dataset = DatasetDict(
            {
                "train": concatenate_datasets([ds["train"] for ds in dataset_list]),
                "test": concatenate_datasets([ds["test"] for ds in dataset_list]),
            }
        )
        if self.mix.shuffle:
            final_dataset = final_dataset.shuffle(seed=42)

        separate_dataset = None
        if self.mix.keep_separated_datasets_in_dataset_dict:
            separate_dataset = DatasetDict()
            for ds_config, ds in zip(self.mix.datasets, dataset_list):
                separate_dataset[f"{ds_config.dataset_key}Train"] = ds["train"]
                separate_dataset[f"{ds_config.dataset_key}Test"] = ds["test"]

        return final_dataset, separate_dataset

    def compute_stats(self, dataset: DatasetDict, tokenizer: Optional[PreTrainedTokenizer] = None) -> Dict:
        dataset_stats = {}
        for split in tqdm.tqdm(dataset.keys(), desc="Computing dataset stats"):
            dataset_stats[split] = self.compute_dataset_stats(dataset[split], tokenizer=tokenizer)
        # Create CSV file with stats
        return dataset_stats

    def compute_mix_stats(self,
                          final_ds,
                          separate_ds,
                          tokenizer: Optional[PreTrainedTokenizer] = None,
                          ) -> pd.DataFrame:

        if separate_ds is not None:
            final_ds_stats = self.compute_stats(separate_ds, tokenizer=tokenizer)
            df = pd.DataFrame.from_dict(final_ds_stats, orient="index")
            df.loc["Train"] = df[list(df.reset_index()["index"].apply(lambda x: "Train" in x))].sum(axis=0)
            df.loc["Test"] = df[list(df.reset_index()["index"].apply(lambda x: "Test" in x))].sum(axis=0)

            def bootstrap(k1, k2, n=10000):
                """Sample n lenghts from the distribution so as not to bias"""
                sampled_distrib = []
                for _ in range(n):
                    choices = [k for k in final_ds_stats.keys() if k.endswith(k1)]
                    weights = [final_ds_stats[k]["num_examples"] for k in choices]
                    weights = [w/sum(weights) for w in weights]
                    sampled_distrib.append(random.choice(final_ds_stats[random.choices(choices, weights=weights)[0]][k2]))
                return sampled_distrib

            from itertools import product
            k2_opts = ["word_distribution", "token_distribution"] if tokenizer else ["word_distribution"]
            for k1, k2 in product(["Train", "Test"], k2_opts):
                df.loc[k1, k2] = ",".join(map(str, bootstrap(k1, k2)))

        else:
            final_ds_stats = self.compute_stats(final_ds, tokenizer=tokenizer)
            df = pd.DataFrame.from_dict(final_ds_stats, orient="index")

        df["avg_word"] = df["num_words"] / df["num_examples"]
        if tokenizer:
            df["avg_tokens"] = df["num_tokens"] / df["num_examples"]
        return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="configs/pretraining_testing.yaml")
    parser.add_argument("--hub_id", type=str, default="manu/testing")
    parser.add_argument("--estimate_from_k", type=int, default=1000)
    parser.add_argument("--tokenizer_name", type=str, default=None)
    args = parser.parse_args()

    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer_name) if args.tokenizer_name else None

    # Init
    api = HfApi()
    config = configue.load(args.config)
    ds_constructor = DatasetConstructor(config["data_mix"], estimate_from_k=args.estimate_from_k)

    # Build dataset
    final_ds, separate_ds = ds_constructor.build_concatenated_dataset()

    # Compute stats
    if ds_constructor.mix.compute_dataset_stats:
        df = ds_constructor.compute_mix_stats(final_ds, separate_ds, tokenizer)
        df.to_csv("dataset_stats.csv")
        df.drop(columns=["word_distribution"], inplace=True)
        df.drop(columns=["token_distribution"], inplace=True)
        df.to_markdown(buf="dataset_stats.md")
        print(df)

    # Push to hub
    if args.hub_id is not None:
        final_ds.push_to_hub(args.hub_id, private=False)
        api.upload_file(
            repo_id=args.hub_id,
            path_or_fileobj="dataset_stats.csv",
            path_in_repo="dataset_stats.csv",
            repo_type="dataset",
        )
        api.upload_file(
            repo_id=args.hub_id,
            path_or_fileobj="dataset_stats.md",
            path_in_repo="dataset_stats.md",
            repo_type="dataset",
        )

        if separate_ds is not None:
            separate_ds.push_to_hub(f"{args.hub_id}_separate", private=False)
            api.upload_file(
                repo_id=f"{args.hub_id}_separate",
                path_or_fileobj="dataset_stats.csv",
                path_in_repo="dataset_stats.csv",
                repo_type="dataset",
            )
            api.upload_file(
                repo_id=f"{args.hub_id}_separate",
                path_or_fileobj="dataset_stats.md",
                path_in_repo="dataset_stats.md",
                repo_type="dataset",
            )

    # Clean up
    if ds_constructor.mix.compute_dataset_stats:
        if os.path.exists("dataset_stats.csv"):
            os.remove("dataset_stats.csv")
        if os.path.exists("dataset_stats.md"):
            os.remove("dataset_stats.md")

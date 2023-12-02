"""This code is used to aggregate all of the datasets needed to construct a pretraining dataset from a YAML config file."""

import argparse
import os
import time
import random
from typing import Any, Callable, Dict, Optional, Tuple

import configue
import datasets
import pandas as pd
import tqdm
import hashlib
from transformers import PreTrainedTokenizerFast, AutoTokenizer
from datasets import Dataset, DatasetDict, concatenate_datasets, load_dataset
from huggingface_hub import HfApi

from dataset_construction.dataset_config import DataMix, DatasetConfig
from dataset_construction.utils import test_set_conformity
from dataset_preprocessing.deduplication import deduplicate_dataset
import time


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
        print(f"Processing dataset {dataset_key} with {len(dataset)} samples")
        if preprocessing_function is not None:
            print(f"Applying preprocessing function to {dataset_key}")
            dataset = dataset.map(preprocessing_function,
                                  num_proc=os.cpu_count(),
                                  desc="Preprocessing function",
                                  # writer_batch_size=100
                                  )

        if filtering_function is not None:
            print(f"Applying filtering function to {dataset_key}")
            dataset = dataset.filter(filtering_function,
                                     num_proc=os.cpu_count(),
                                     desc="Filtering function",
                                     # writer_batch_size=100
                                     )

        # Do it only if needed
        print(f"ID type for {dataset_key} is {dataset.features['id'].dtype}")
        if dataset.features["id"].dtype != "string":
            print(f"Converting ID type for {dataset_key} to string")
            dataset = dataset.cast_column("id", datasets.Value(dtype="string", id=None))
        # dataset = dataset.cast_column("text", datasets.Value(dtype="string", id=None))
        print(f"Adding dataset_id column for {dataset_key}")
        time1 = time.time()

        # Extremely slow
        # dataset = dataset.add_column("dataset_id", [f"{dataset_key}"] * len(dataset))

        # Test solution
        def add_columns(examples):
            examples["dataset_id"] = [f"{dataset_key}"] * len(examples["id"])
            return examples

        dataset = dataset.map(add_columns,
                              num_proc=os.cpu_count(),
                              batched=True,
                              batch_size=100,
                              # writer_batch_size=100,
                              keep_in_memory=False,
                              desc="Adding dataset_id column")

        print(f"Time taken to add column: {time.time() - time1}")
        return dataset

    def build_single_dataset_dict(self, dataset_config: DatasetConfig) -> DatasetDict:
        """Load a single dataset from HF Datasets Hub, and apply the filtering function if provided."""
        if dataset_config.load_from_disk is True:
            print(f"Loading dataset {dataset_config.dataset_path} from disk")
            time1 = time.time()
            dataset_train = datasets.load_from_disk(dataset_config.dataset_path)["train"]
        else:
            print(f"Loading dataset {dataset_config.dataset_path} from HF Datasets Hub with {os.cpu_count()} workers")
            time1 = time.time()
            dataset_train = load_dataset(
                dataset_config.dataset_path,
                name=dataset_config.dataset_name,
                split=dataset_config.train_split,
                num_proc=os.cpu_count(),
                **dataset_config.dataset_kwargs
            )
        print(f"Time taken to load dataset: {time.time() - time1}")
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
            print(
                f"Loading test set for {dataset_config.dataset_path} with {dataset_config.num_test_examples if dataset_config.num_test_examples else 'all'} samples")
            if dataset_config.num_train_examples:
                dataset_train = dataset_train.select(range(dataset_config.num_train_examples))

            if dataset_config.load_from_disk is True:
                print(f"Loading test set for {dataset_config.dataset_path} from disk")
                dataset_test = datasets.load_from_disk(dataset_config.dataset_path)["test"]
            else:
                dataset_test = load_dataset(
                    dataset_config.dataset_path,
                    name=dataset_config.dataset_name,
                    split=dataset_config.test_split,
                    num_proc=os.cpu_count(),
                    **dataset_config.dataset_kwargs
                )
            if dataset_config.num_test_examples:
                dataset_test = dataset_test.select(range(min(dataset_config.num_test_examples, len(dataset_test))))
        else:
            raise ValueError("Either build_test_set_from_train or test_split must be set")
        assert isinstance(dataset_test, Dataset)
        assert isinstance(dataset_train, Dataset)
        print(f"Loaded {dataset_config.dataset_path} with {len(dataset_train)} train examples, {len(dataset_test)} test examples")

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
        print(f"Processed {dataset_config.dataset_path} with {len(dataset_train)} train examples, {len(dataset_test)} test examples")

        if dataset_config.needs_internal_deduplication:
            print(f"Performing internal deduplication: {dataset_config.dataset_path}")

            # print out stats before deduplication
            print(f"Before deduplication: {len(dataset_train)} train examples, {len(dataset_test)} test examples")
            dataset_test, uniques = deduplicate_dataset(dataset_test, num_workers=os.cpu_count())
            dataset_train, _ = deduplicate_dataset(dataset_train, num_workers=os.cpu_count(), blacklist=uniques)

            print(f"After deduplication: {len(dataset_train)} train examples, {len(dataset_test)} test examples")
            del uniques

        dataset = DatasetDict({"train": dataset_train, "test": dataset_test})

        # Remove columns that are not needed
        if len(list(set(dataset_train.column_names) - {"id", "text", "dataset_id"})) > 0:
            dataset = dataset.remove_columns(list(set(dataset_train.column_names) - {"id", "text", "dataset_id"}))
        assert set(dataset["train"].column_names) == {"id", "text",
                                                      "dataset_id"}, f"Mismatch in column names {dataset['train'].column_names}"
        return dataset

    def compute_dataset_stats(self,
                              dataset: Dataset,
                              tokenizer: Optional[PreTrainedTokenizerFast] = None) -> Dict[str, Any]:
        """Compute some stats about a dataset."""

        # Assume uniform distribution
        if self.estimate_from_k:
            # idxs = random.choices(range(len(dataset)), k=100)
            k = min(self.estimate_from_k, len(dataset))
            ds_estimate = dataset.select(range(k))
            while (ds_estimate.data.nbytes / 1e9 > 0.01) and k > 5:
                k = k // 2
                ds_estimate = dataset.select(range(k))
            print(f"Estimating stats from {k} samples, with a dataset size of {ds_estimate.data.nbytes / pow(2,30)} GB")
        else:
            ds_estimate = dataset

        word_counts = [len(example["text"].split()) for example in ds_estimate]
        stats = {
            "num_examples": len(dataset),
            "num_words": len(dataset) * sum(word_counts) / len(word_counts),
            "word_distribution": word_counts,
            "dataset_gb": round(dataset.data.nbytes / pow(2, 30), 3),
        }

        if tokenizer:
            def tok_and_count(example):
                encodings = tokenizer(example['text'], return_tensors="np")
                return {"input_len": encodings["input_ids"].shape[1]}

            tok_counts = ds_estimate.map(tok_and_count, num_proc=os.cpu_count())["input_len"]
            stats.update({
                "num_tokens": len(dataset) * sum(tok_counts) / len(tok_counts),
                "token_distribution": tok_counts,
            })
        return stats

    def single_dataset_macro(self, dataset_config: DatasetConfig) -> DatasetDict:
        print(f"Loading and filtering dataset {dataset_config.dataset_path}")
        mapper_fn = dataset_config.preprocessing_function if hasattr(dataset_config, "preprocessing_function") else None
        filter_fn = dataset_config.filtering_function if hasattr(dataset_config, "filtering_function") else None

        # hash the bytes of the function to check if it has changed.
        # Note: not exact because only intermediate source code is checked so changed magin numbers are not affected
        mapper_fn_hash = dataset_config.preprocessing_function.mapper_fn.__code__.co_code if mapper_fn else None
        filter_fn_hash = dataset_config.filtering_function.filter_fn.__code__.co_code if filter_fn else None
        # exclude preprocessing_function and mapping_function from the hash computation
        dataset_config_hash = hashlib.md5(
            str({k: v for k, v in dataset_config.__dict__.items() if "object at" not in str(v)}).encode(
                "utf-8")).hexdigest()
        if mapper_fn_hash:
            dataset_config_hash += hashlib.md5(str(mapper_fn_hash).encode("utf-8")).hexdigest()
        if filter_fn_hash:
            dataset_config_hash += hashlib.md5(str(filter_fn_hash).encode("utf-8")).hexdigest()

        if os.path.exists(os.path.join(self.mix.local_save_dir, "dataset_cache", dataset_config_hash)):
            print(f"Loading dataset {dataset_config.dataset_path} from cache")
            ds = datasets.load_from_disk(os.path.join(self.mix.local_save_dir, "dataset_cache", dataset_config_hash))
        else:
            ds: DatasetDict = self.build_single_dataset_dict(dataset_config)
            if self.mix.local_save_dir:
                print(f"Saving dataset {dataset_config.dataset_path} to cache")
                os.makedirs(os.path.join(self.mix.local_save_dir, "dataset_cache"), exist_ok=True)
                ds.save_to_disk(os.path.join(self.mix.local_save_dir, "dataset_cache", dataset_config_hash),
                                num_proc=os.cpu_count())
        return ds

    def build_concatenated_dataset(self) -> Tuple[DatasetDict, Optional[DatasetDict]]:
        dataset_list = []
        for dataset_config in tqdm.tqdm(self.mix.datasets, desc="Loading datasets"):
            ds = self.single_dataset_macro(dataset_config)
            dataset_list.append(ds)

        print(f"Concatenating {len(dataset_list)} datasets")
        final_dataset = DatasetDict(
            {
                "train": concatenate_datasets([ds["train"] for ds in dataset_list]),
                "test": concatenate_datasets([ds["test"] for ds in dataset_list]),
            }
        )
        if self.mix.shuffle:
            print("Shuffling dataset")
            final_dataset = final_dataset.shuffle(seed=42)

        separate_dataset = None
        if len(self.mix.datasets) > 1:
            separate_dataset = DatasetDict()
            for ds_config, ds in zip(self.mix.datasets, dataset_list):
                separate_dataset[f"{ds_config.dataset_key}Train"] = ds["train"]
                separate_dataset[f"{ds_config.dataset_key}Test"] = ds["test"]

        return final_dataset, separate_dataset

    def compute_stats(self, dataset: DatasetDict, tokenizer: Optional[PreTrainedTokenizerFast] = None) -> Dict:
        dataset_stats = {}
        for split in tqdm.tqdm(dataset.keys(), desc="Computing dataset stats"):
            dataset_stats[split] = self.compute_dataset_stats(dataset[split], tokenizer=tokenizer)
        # Create CSV file with stats
        return dataset_stats

    def compute_mix_stats(self,
                          final_ds,
                          separate_ds,
                          tokenizer: Optional[PreTrainedTokenizerFast] = None,
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
                    weights = [w / sum(weights) for w in weights]
                    sampled_distrib.append(
                        random.choice(final_ds_stats[random.choices(choices, weights=weights)[0]][k2]))
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
    parser.add_argument("--config", type=str, default="configs/mock_testing.yaml")
    parser.add_argument("--hub_id", type=str, default=None)
    parser.add_argument("--estimate_from_k", type=int, default=1000)
    parser.add_argument("--prep_config_n", type=int, default=-1)
    args = parser.parse_args()

    # Init
    api = HfApi()
    config = configue.load(args.config)
    tokenizer = AutoTokenizer.from_pretrained(config["tokenizer"]) if "tokenizer" in config.keys() else None
    assert (tokenizer is None) or isinstance(tokenizer, PreTrainedTokenizerFast)

    ds_constructor = DatasetConstructor(config["data_mix"], estimate_from_k=args.estimate_from_k)

    if args.prep_config_n >= 0:
        print(f"\nPreparing dataset {ds_constructor.mix.datasets[args.prep_config_n].dataset_key} from config")
        config_n = ds_constructor.mix.datasets[args.prep_config_n]
        ds_constructor.single_dataset_macro(config_n)
        print(f"Done {ds_constructor.mix.datasets[args.prep_config_n].dataset_key} !\n\n")
        exit()
    elif ds_constructor.mix.load_from_local_save_dir:
        final_ds = datasets.load_from_disk(f"{ds_constructor.mix.local_save_dir}/{ds_constructor.mix.name}")
        separate_ds = None
        if os.path.exists(f"{ds_constructor.mix.local_save_dir}/{ds_constructor.mix.name}_separate"):
            separate_ds = datasets.load_from_disk(
                f"{ds_constructor.mix.local_save_dir}/{ds_constructor.mix.name}_separate")

    else:
        final_ds, separate_ds = ds_constructor.build_concatenated_dataset()
        if ds_constructor.mix.local_save_dir:
            print(f"Saving dataset {ds_constructor.mix.name} to {ds_constructor.mix.local_save_dir}")
            final_ds.save_to_disk(f"{ds_constructor.mix.local_save_dir}/{ds_constructor.mix.name}", num_proc=os.cpu_count())
            if separate_ds is not None:
                separate_ds.save_to_disk(f"{ds_constructor.mix.local_save_dir}/{ds_constructor.mix.name}_separate", num_proc=os.cpu_count())

    # Compute stats
    if ds_constructor.mix.compute_dataset_stats:
        os.makedirs(f"{ds_constructor.mix.stats_save_dir}/{ds_constructor.mix.name}", exist_ok=True)
        df = ds_constructor.compute_mix_stats(final_ds, separate_ds, tokenizer)
        df["ratio"] = round(df["dataset_gb"]/df["dataset_gb"].sum(), 5) * 2     # train test split
        df.to_csv(f"{ds_constructor.mix.stats_save_dir}/{ds_constructor.mix.name}/dataset_stats.csv")
        df.drop(columns=["word_distribution"], inplace=True)
        if tokenizer:
            df.drop(columns=["token_distribution"], inplace=True)
        df.to_markdown(buf=f"{ds_constructor.mix.stats_save_dir}/{ds_constructor.mix.name}/dataset_stats.md")
        print(df)

    # Push to hub
    if args.hub_id is not None:
        # retries
        for n in range(20):
            try:
                final_ds.push_to_hub(args.hub_id,
                                     max_shard_size=ds_constructor.mix.max_shard_size,
                                     private=False)
                # Push config yaml
                api.upload_file(
                    repo_id=args.hub_id,
                    path_or_fileobj=args.config,
                    path_in_repo="config.yaml",
                    repo_type="dataset",
                )
                api.upload_file(
                    repo_id=args.hub_id,
                    path_or_fileobj=f"{ds_constructor.mix.stats_save_dir}/{ds_constructor.mix.name}/dataset_stats.csv",
                    path_in_repo="dataset_stats.csv",
                    repo_type="dataset",
                )
                api.upload_file(
                    repo_id=args.hub_id,
                    path_or_fileobj=f"{ds_constructor.mix.stats_save_dir}/{ds_constructor.mix.name}/dataset_stats.md",
                    path_in_repo="dataset_stats.md",
                    repo_type="dataset",
                )

                if separate_ds is not None and ds_constructor.mix.keep_separated_datasets_in_dataset_dict:
                    # only upload valid split
                    new_ds = DatasetDict({k: v for k, v in separate_ds.items() if "Test" in k})
                    new_ds.push_to_hub(f"{args.hub_id}_separate",
                                            max_shard_size=ds_constructor.mix.max_shard_size,
                                            private=False)
                    # Push config yaml
                    api.upload_file(
                        repo_id=f"{args.hub_id}_separate",
                        path_or_fileobj=args.config,
                        path_in_repo="config.yaml",
                        repo_type="dataset",
                    )
                    api.upload_file(
                        repo_id=f"{args.hub_id}_separate",
                        path_or_fileobj=f"{ds_constructor.mix.stats_save_dir}/{ds_constructor.mix.name}/dataset_stats.csv",
                        path_in_repo="dataset_stats.csv",
                        repo_type="dataset",
                    )
                    api.upload_file(
                        repo_id=f"{args.hub_id}_separate",
                        path_or_fileobj=f"{ds_constructor.mix.stats_save_dir}/{ds_constructor.mix.name}/dataset_stats.md",
                        path_in_repo="dataset_stats.md",
                        repo_type="dataset",
                    )
                break
            except Exception as e:
                print(e)
                print(f"Failed to push to hub, retrying #{n}")
                # exponential wait time
                time.sleep(min(pow(2, n), 3600))
    print("Done!")

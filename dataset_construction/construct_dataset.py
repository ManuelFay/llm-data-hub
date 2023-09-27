"""This code is used to aggregate all of the datasets needed to construct a pretraining dataset from a YAML config file."""

import argparse
import os
from typing import Any, Callable, Dict, Optional, Tuple

import configue
import pandas as pd
import tqdm
from datasets import Dataset, DatasetDict, concatenate_datasets, load_dataset
from huggingface_hub import HfApi

from dataset_construction.dataset_config import DataMix, DatasetConfig
from dataset_construction.utils import test_set_conformity


class DatasetConstructor:
    def __init__(self, mix):
        self.mix = mix

    def process_single_dataset(
        self,
        dataset: Dataset,
        num_tokens: Optional[int],
        filtering_function: Optional[Callable],
        preprocessing_function: Optional[Callable] = None,
    ) -> Dataset:
        """Filter and truncate a dataset, if needed."""

        if preprocessing_function is not None:
            dataset = dataset.map(preprocessing_function, num_proc=os.cpu_count())

        if filtering_function is not None:
            dataset = dataset.filter(filtering_function, num_proc=os.cpu_count())

        dataset = dataset.shuffle(seed=42)
        if num_tokens is not None:
            estimation_sample_size = min(1000, len(dataset))
            num_tokens_in_dataset = (
                sum([len(example["text"].split()) for example in dataset.select(range(estimation_sample_size))])
                / estimation_sample_size
            ) * len(dataset)
            estimated_samples_required = int((num_tokens / num_tokens_in_dataset) * len(dataset))
            dataset = dataset.select(range(estimated_samples_required))

        return dataset

    def build_single_dataset_dict(self, dataset_config: DatasetConfig) -> DatasetDict:
        """Load a single dataset from HF Datasets Hub, and apply the filtering function if provided."""
        dataset_train = load_dataset(
            dataset_config.dataset_path, name=dataset_config.dataset_name, split=dataset_config.train_split
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
                dataset_config.dataset_path, name=dataset_config.dataset_name, split=dataset_config.test_split
            )
            dataset_test = dataset_test.select(range(min(dataset_config.num_test_examples, len(dataset_test))))
        else:
            raise ValueError("Either build_test_set_from_train or test_split must be set")
        assert isinstance(dataset_test, Dataset)
        assert isinstance(dataset_train, Dataset)

        dataset_train = self.process_single_dataset(
            dataset_train,
            dataset_config.num_train_tokens,
            dataset_config.filtering_function,
            dataset_config.preprocessing_function,
        )
        dataset_test = self.process_single_dataset(
            dataset_test,
            dataset_config.num_test_tokens,
            dataset_config.filtering_function,
            dataset_config.preprocessing_function,
        )
        dataset = DatasetDict({"train": dataset_train, "test": dataset_test})
        # only keep the text field and the id field
        dataset = dataset.map(
            lambda example: {"text": example["text"], "id": f"{dataset_config.dataset_path}_{example['id']}"},
            remove_columns=dataset["train"].column_names,
            num_proc=os.cpu_count(),
        )
        return dataset

    @staticmethod
    def compute_dataset_stats(dataset: Dataset) -> Dict[str, Any]:
        """Compute some stats about a dataset."""
        word_counts = [len(example["text"].split()) for example in dataset]
        return {
            "num_examples": len(dataset),
            "num_words": sum(word_counts),
            "avg_words": sum(word_counts) / len(word_counts),
            "word_distribution": word_counts,
            "dataset_gb": round(dataset.data.nbytes / 1e9, 3),
        }

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
            for ds_name, ds in zip(self.mix.datasets, dataset_list):
                ds_name = ds_name.dataset_path.split("/")[-1].replace("-", "_")
                # camelcase name
                ds_name = "".join([word.capitalize() for word in ds_name.split("_")])
                separate_dataset[f"{ds_name}Train"] = ds["train"]
                separate_dataset[f"{ds_name}Test"] = ds["test"]

        return final_dataset, separate_dataset

    def compute_stats(self, dataset: DatasetDict) -> Dict:
        dataset_stats = {}
        for split in tqdm.tqdm(dataset.keys(), desc="Computing dataset stats"):
            dataset_stats[split] = self.compute_dataset_stats(dataset[split])
        # Create CSV file with stats
        return dataset_stats

    def compute_mix_stats(self, final_ds, separate_ds) -> pd.DataFrame:
        final_ds_stats = self.compute_stats(final_ds)
        if separate_ds is not None:
            final_ds_stats.update(self.compute_stats(separate_ds))
        df = pd.DataFrame.from_dict(final_ds_stats, orient="index")
        return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="configs/pretraining_testing.yaml")
    parser.add_argument("--hub_id", type=str, default="manu/testing")
    args = parser.parse_args()

    # Init
    api = HfApi()
    config = configue.load(args.config)
    ds_constructor = DatasetConstructor(config["data_mix"])

    # Build dataset
    final_ds, separate_ds = ds_constructor.build_concatenated_dataset()

    # Compute stats
    if ds_constructor.mix.compute_dataset_stats:
        df = ds_constructor.compute_mix_stats(final_ds, separate_ds)
        df.to_csv("dataset_stats.csv")
        df.drop(columns=["word_distribution"], inplace=True)
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

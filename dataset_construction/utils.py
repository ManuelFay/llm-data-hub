from typing import Optional
import hashlib

from dataset_construction.dataset_config import DatasetConfig


def test_set_conformity(dataset, num_test_samples: Optional[int]) -> int:
    """Make sure the test set is not too big."""
    if num_test_samples is not None:
        return min(num_test_samples, len(dataset))
    return min(max(100, len(dataset) // 100), 10000)


def get_config_hash(dataset_config: DatasetConfig):
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

    dataset_config_hash = hashlib.md5(str(dataset_config_hash).encode("utf-8")).hexdigest()

    return dataset_config.dataset_key + "_" + dataset_config_hash

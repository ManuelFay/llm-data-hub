from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Tuple, Union


@dataclass
class DatasetConfig:
    """All datasets should be on HF Datasets Hub, with at least a 'text' field.
    This class is used to load them from there."""

    dataset_path: str
    dataset_name: Optional[str] = None
    train_split: Optional[str] = "train"
    test_split: Optional[str] = None
    build_test_set_from_train: Optional[bool] = False
    num_train_examples: Optional[int] = None
    num_test_examples: Optional[int] = None
    num_train_tokens: Optional[int] = None
    num_test_tokens: Optional[int] = None
    filtering_function: Optional[Callable] = None
    preprocessing_function: Optional[Callable] = None
    tags: Optional[List[str]] = None
    # load_in_streaming_mode: Optional[bool] = False # Not implemented yet


@dataclass
class DataMix:
    datasets: List[DatasetConfig]
    name: str
    shuffle: bool = False
    compute_dataset_stats: bool = True
    keep_separated_datasets_in_dataset_dict: bool = False
    deduplicate_test_set: bool = False  # TODO: Not implemented yet
    ngram_path_for_extra_deduplication: Optional[str] = None  # TODO: Not implemented yet

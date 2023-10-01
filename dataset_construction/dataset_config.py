from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Tuple, Union


@dataclass
class DatasetConfig:
    """All datasets should be on HF Datasets Hub, with at least a 'text' field.
    This class is used to load them from there."""

    dataset_path: str
    dataset_name: Optional[str] = None
    dataset_key: Optional[str] = None
    train_split: Optional[str] = "train"
    test_split: Optional[str] = None
    dataset_kwargs: Optional[Dict] = None
    build_test_set_from_train: Optional[bool] = False
    num_train_examples: Optional[int] = None
    num_test_examples: Optional[int] = None
    # num_train_tokens: Optional[int] = None
    # num_test_tokens: Optional[int] = None
    filtering_function: Optional[Callable] = None
    preprocessing_function: Optional[Callable] = None
    tags: Optional[List[str]] = None
    text_column: str = "text"
    id_column: str = "id"
    # load_in_streaming_mode: Optional[bool] = False # Not implemented yet

    def __post_init__(self):
        if self.dataset_kwargs is None:
            self.dataset_kwargs = {"data_dir": None}
        if self.dataset_key is None:
            ds_name = self.dataset_path.split("/")[-1].replace("-", "_")
            if self.dataset_name is not None:
                ds_name += "_" + self.dataset_name.split("/")[-1].replace("-", "_")
            if self.dataset_kwargs is not None:
                kwargs_str = "_".join([x.replace("-", "_") for x in self.dataset_kwargs.values() if isinstance(x, str)])
                if len(kwargs_str) > 0:
                    ds_name += "_" + kwargs_str
            ds_name = "".join([word.capitalize() for word in ds_name.split("_")])
            self.dataset_key = ds_name


@dataclass
class DataMix:
    datasets: List[DatasetConfig]
    name: str
    shuffle: bool = False
    compute_dataset_stats: bool = True
    local_save_dir: Optional[str] = None
    load_from_local_save_dir: bool = False
    max_shard_size: Optional[Union[int, str]] = None
    keep_separated_datasets_in_dataset_dict: bool = False
    deduplicate_test_set: bool = False  # TODO: Not implemented yet
    ngram_path_for_extra_deduplication: Optional[str] = None  # TODO: Not implemented yet

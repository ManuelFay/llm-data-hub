# Dataset Construction

In order to build the final dataset, we specify the datamix in a YAML configuration file.
All datasets should be hosted on the HuggingFace hub.

The easiest dataset configuration has two splits, a train set split and test set split, and have a text and id column.
The diversity of datasets we may want to include however is realistically not always formatted and we provide options to 
process, filter, and sample from arbitrary datasets to construct the final mix.

### Usage

```bash
 python dataset_construction/construct_dataset.py --config your_config.yaml --hub_id hf_repo_id
```
Note that depending on the size of the datasets, large data sizes may be downloaded and uploaded and high RAM and memory
usages can be expected. Additionaly, BeamRunners can be specified to use Spark or Hadoop for data processing
rather than more Naive "DirectRunner" method (feature to be tested, still WIP).

### Dataset template

The DatasetConfig is specified as such:
```python
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
```

These datasets are then passed to the Datamix along with other options.
```python
@dataclass
class DataMix:
    datasets: List[DatasetConfig]
    name: str
    shuffle: bool = False
    compute_dataset_stats: bool = True
    keep_separated_datasets_in_dataset_dict: bool = False
    deduplicate_test_set: bool = False  # TODO: Not implemented yet
    ngram_path_for_extra_deduplication: Optional[str] = None  # TODO: Not implemented yet
```

Specifying a mix can be done through a YAML config file:

```yaml
data_mix:
  (): dataset_construction.DataMix
  name: "pretraining_testing"
  shuffle: false
  compute_dataset_stats: true
  keep_separated_datasets_in_dataset_dict: true
  deduplicate_test_set: false
  ngram_path_for_extra_deduplication: null
  datasets:
    - (): dataset_construction.DatasetConfig
      dataset_path: manu/wmt-en-fr
      test_split: "test"
      num_train_examples:  1000
      num_test_examples: 100
    - (): dataset_construction.DatasetConfig
      dataset_path: manu/french_librispeech_text_only
      build_test_set_from_train: true
      num_train_examples:  1000
      num_test_examples: 100
    - (): dataset_construction.DatasetConfig
      dataset_path: manu/french_podcasts
      build_test_set_from_train: true
      num_test_examples: 100
      filtering_function:
        (): dataset_collection.french.french_transcribed_podcast.PodcastFilter
      preprocessing_function:
        (): dataset_collection.french.french_transcribed_podcast.PodcastMapper
```

Most options are trivial to understand but filtering and preprocssing functions can be interesting to look into.

### Filtering and Mapping

Filters and mappers can be added to the YAML config, by instanciating a python object class, using the `configue` syntax:

```yaml
- filtering_function:
  (): module_name.outer_class_no_args_needed
- preprocessing_function:
  (): module_name.outer_class
    - arg1_defining_an object:
      (): module_name.class_name
       - arg1_1
    - arg2
```

This class should inherit from the abstract classes in `dataset_collection/abstract_mapper_and_filter.py`.
Create one per dataset (if needed), by overriding the mapper_fn and filter_fn class.

Args can be given to the Mapper Class by adding an `__init__` class and passing args in the YAML.

```python
"""To be used to filter from the hf dataset which is not in the correct format"""
from typing import Dict
from dataset_collection.abstract_mapper_and_filter import Mapper, Filter


class PodcastMapper(Mapper):
    def mapper_fn(self, example) -> Dict:
        """Keep only columns programme_id and transcript and rename as id, text"""
        return {"text": example["transcript"], "id": example['programme_id']}


class PodcastFilter(Filter):
    def filter_fn(self, example) -> bool:
        """Keep only columns programme_id and transcript and rename as id, text"""
        return isinstance(example["text"], str) and len(example["text"]) > 100
```

This can be useful to rename columns, or add heuristic filters.
Note however that this code is not very optimized and is better to already have clean datasets.


### Next steps

Most important next step is the test set deduplication (looking into it).

Depending on large scale load tests, maybe I'll add execution checkpointing (if fails occur, not having to map and filter datasets over).


# Deduplication

# 1 - Bloom Filter Deduplication Function

This Python function uses a Bloom Filter, a probabilistic data structure, to efficiently deduplicate a dataset based on a specified column. Bloom Filters excel in scenarios where you need to reduce unnecessary comparisons, providing a high probability of correctly identifying whether an item is in the dataset. This is especially valuable when working with large datasets, as it helps improve performance. However, it's essential to note that Bloom Filters can produce false positives, mistakenly indicating the presence of an item that isn't in the dataset. You can control the false positive rate by adjusting the filter's size.

Deduplication can be done within a dataset, or across datasets.

## Function Arguments

- `--hub_id_1` (str): The identifier for the Hugging Face dataset you want to deduplicate. 
- `--hub_id_2` (str, optional): Second identifier for another Hugging Face dataset for deduplication between two datasets.
- `--split_1` (str): The name of the first split.
- `--split_2` (str, optional): Second split name to performe external deduplication between two splits.
- `--column_name_1` (str): The name of the column used for deduplication in the first dataset.
- `--column_name_2` (str, optional): Name of the column used for deduplication in the second split.
- `--split_1_internal_deduplication` (boolean, optional): A flag to indicate whether internal deduplication should be applied to the first split (default: False).
- `--split_2_internal_deduplication` (boolean, optional): A flag to indicate whether internal deduplication should be applied to the second split (default: False).
- `--push_to_hub_1` (boolean, optional): A flag to indicate whether to push the deduplicated dataset for the first dataset to the Hugging Face Hub (default: False).
- `--push_to_hub_2` (boolean, optional): A flag to indicate whether to push the deduplicated dataset for the second dataset to the Hugging Face Hub (default: False).
- `--expected_size` (int, optional): The expected size of the Bloom Filter (default: 1000000).
- `--false_positive_rate` (float, optional): The desired false-positive rate for the Bloom Filter (default: 0.000001).
- `--streaming_mode` (boolean, optional): A flag to indicate whether to load the dataset in streaming mode (default: False).
- `--save_locally` (boolean, optional): A flag to indicate whether to save the deduplicated dataset locally (default: False).

## Example Usage
<b>Important:  Split 1 is the reference split, items are deleted in split 2 for external deduplication.</b>

### Internal split deduplication:
```bash
python bloom_filter.py --hub_id_1="Nicolas-BZRD/DOLE_opendata" --split_1=“test” --split_1_internal_deduplication      
```
Deduplicate the train split of the "DOLE_opendata" dataset based on the text column.

### Internal + External split deduplication (same dataset)
```bash
python bloom_filter.py --hub_id_1="Nicolas-BZRD/DOLE_opendata" --split_1="test" --split_2="train" --split_2_internal_deduplication --push_to_hub_1
```
Deletion of duplicate values in the "train" split, then deletion of elements contained in the "train" split which are also contained in the "test" split. The final dataset is then pushed onto the hugging face hub.

### External split deduplication (two different datasets)
```bash
python bloom_filter.py --hub_id_1="Nicolas-BZRD/DOLE_opendata" --hub_id_2="Nicolas-BZRD/CNIL_opendata"  --split_1="train" --split_2="train" 
```
Deletion of values contained in dataset "CNIL_opendata" of the "train" split that are also contained in the "train" split of dataset "DOLE_opendata". "DOLE_opendata" stay unchanged.

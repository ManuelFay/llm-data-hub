# Deduplication

Deduplication can be done within a dataset, or across datasets.

---

# Bloom Filter Deduplication Function

This Python function uses a Bloom Filter, a probabilistic data structure, to efficiently deduplicate a dataset based on a specified column. Bloom Filters excel in scenarios where you need to reduce unnecessary comparisons, providing a high probability of correctly identifying whether an item is in the dataset. This is especially valuable when working with large datasets, as it helps improve performance. However, it's essential to note that Bloom Filters can produce false positives, mistakenly indicating the presence of an item that isn't in the dataset. You can control the false positive rate by adjusting the filter's size.

## Function Arguments

- `--hugging_face_id` (str): The identifier for the Hugging Face dataset you want to deduplicate.
- `--column_name` (str, default="text"): The name of the column used for deduplication.
- `--expected_size` (int, default=10000): The expected size of the Bloom Filter. This affects memory usage and false-positive rate.
- `--false_positive_rate` (float, default=0.001): The desired false-positive rate for the Bloom Filter.
- `--deduplicate_test_split` (boolean): Whether to deduplicate the test split if it exists.
- `--streaming_mode` (boolean): Whether to load the dataset in streaming mode.
- `--push_to_hub` (boolean): Whether to push the deduplicated dataset to the Hugging Face Hub.
- `--save_locally` (boolean): Whether to save the deduplicated dataset locally.

## Example Usage

```bash
python bloom_filter.py --hugging_face_id="Nicolas-BZRD/DOLE_opendata" --save_locally      
```
Deduplicate the train split of the "DOLE_opendata" dataset to its text column and save it locally.

```bash
python bloom_filter.py --hugging_face_id="Nicolas-BZRD/DOLE_opendata" --streaming_mode --push_to_hub      
```
Deduplicate the train split of the "DOLE_opendata" dataset to its text column in streaming mode (useful for big dataset) and pushe the result in the hub.

```bash
python bloom_filter.py --hugging_face_id="Nicolas-BZRD/DOLE_opendata"
```
Deduplicate the train split and the test test split (do not do this to benchmark SOTA dataset) of the "DOLE_opendata" dataset over his text column.

---

To deduplicate within a dataset to keep only unique texts, MinHashLSH can be used.  

HF example: https://github.com/huggingface/transformers/blob/main/examples/research_projects/codeparrot/scripts/minhash_deduplication.py


To deduplicate across datasets or at larger scale, we can use Bloom filters at a paragraph level, once URL deduplication has been done.

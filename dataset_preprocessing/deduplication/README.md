# Deduplication

Deduplication can be done within a dataset, or across datasets.

To deduplicate within a dataset to keep only unique texts, MinHashLSH can be used.  

HF example: https://github.com/huggingface/transformers/blob/main/examples/research_projects/codeparrot/scripts/minhash_deduplication.py


To deduplicate across datasets or at larger scale, we can use Bloom filters at a paragraph level, once URL deduplication has been done.

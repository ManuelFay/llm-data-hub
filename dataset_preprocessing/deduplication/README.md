# Deduplication

Deduplication can be done within a dataset, or across datasets.

To deduplicate within a dataset to keep only unique texts, MinHashLSH can be used.  

HF example: https://github.com/huggingface/transformers/blob/main/examples/research_projects/codeparrot/scripts/minhash_deduplication.py
Other examples: https://github.com/Cerebras/modelzoo/tree/main/modelzoo/transformers/data_processing/slimpajama

### The plan - Training data

To keep the process scalable, we will use prededuped datasets, or dedupe within datasets that are small enough to be 
deduped on a normal size machine.

Since we are adding high-quality data, but in mower quality, we are essentially in the worst case upsampling
high quality data in the training set.

### The plan - dataset contamination

It is more critical to remove overlap between test and train set.

At the document level, we can use MinHash LSH to flag "dangerous" test set samples.
We build an index of MinHash per document in the training set, and use it to manually post filter the 
test sets (which have a more tractable size).

For tests that are comprised of short paragraphs/single sentences that may not be detected within a larger document
in the train set, we try to rely on:
- Recently released benchmarks with data that could not possibly be in the scraps
- n-gram matching / n-gram matching ratio ? (not tractable I think)
- minHash LSH may be sufficient
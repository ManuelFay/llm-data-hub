from typing import Optional, Tuple
import hashlib
from datasets import Dataset


def get_hash(example):
    """Get hash of content field."""
    return {"hash": hashlib.md5(example["text"].strip().encode("utf-8")).hexdigest()}


def check_uniques(example, uniques):
    """Check if current hash is still in set of unique hashes and remove if true."""
    if example["hash"] in uniques:
        uniques.remove(example["hash"])
        return True
    else:
        return False


def preprocess(example):
    """Chain all preprocessing steps into one function to not fill cache."""
    results = dict()
    results.update(get_hash(example))
    return results


def filter(example, uniques):
    """Filter dataset with heuristics. Config, test and has_no_keywords files are removed with a given probability."""
    if not check_uniques(example, uniques):
        return False
    else:
        return True


def deduplicate_dataset(ds: Dataset,
                        num_workers: Optional[int] = None,
                        blacklist: Optional[set] = None) -> Tuple[Dataset, set]:
    """Deduplicate a dataset."""

    # Run preprocessing
    ds = ds.map(preprocess, num_proc=num_workers, writer_batch_size=100)

    uniques = set(ds.unique("hash"))
    # Deduplicate data and apply heuristics
    ds = ds.filter(filter, fn_kwargs={"uniques": uniques}, num_proc=num_workers, desc="Removing duplicates - internal",
                   writer_batch_size=100)

    if blacklist is not None:
        # Deduplicate hashes
        ds = ds.filter(lambda x: x["hash"] not in blacklist, num_proc=num_workers,
                       desc="Removing duplicates - external", writer_batch_size=100)

    return ds, uniques

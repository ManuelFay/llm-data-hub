from unittest import TestCase
from itertools import islice

from datasets import load_dataset, interleave_datasets, Value


class TestFeatureCompat(TestCase):
    def test_all_datasets_can_merge(self):
        oscar_dataset = load_dataset('./dataset_collection/french/oscar', "unshuffled_deduplicated_fr", split='train',
                                     streaming=True)
        oscar_dataset = oscar_dataset.cast_column("id", Value(dtype="string"))

        wikipedia_dataset = load_dataset('./dataset_collection/french/wikipedia', "20220301.fr", split='train',
                                         streaming=True)
        wikipedia_dataset = wikipedia_dataset.remove_columns(["title", "url"])

        mixed_dataset = interleave_datasets([oscar_dataset, wikipedia_dataset])
        print(list(islice(mixed_dataset, 2)))

        mixed_dataset_with_oversampling = interleave_datasets([oscar_dataset, wikipedia_dataset],
                                                              probabilities=[0.8, 0.2], seed=42)
        print(list(islice(mixed_dataset_with_oversampling, 2)))

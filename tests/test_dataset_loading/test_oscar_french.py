from unittest import TestCase
from datasets import load_dataset


class TestOscar(TestCase):
    def test_load_oscar_local(self):
        dataset = load_dataset('./dataset_collection/french/oscar', "unshuffled_deduplicated_fr", split='train', streaming=True)
        print(next(iter(dataset)))

    def test_load_oscar_remote(self):
        # Remote URL and builder file
        dataset = load_dataset('oscar', "unshuffled_deduplicated_fr", split='train', streaming=True)
        print(next(iter(dataset)))

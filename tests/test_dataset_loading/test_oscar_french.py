from unittest import TestCase
from datasets import load_dataset


class TestOscar(TestCase):
    def test_load_oscar_remote(self):
        # Remote URL and builder file
        dataset = load_dataset('oscar-corpus/OSCAR-2301', "fr", split='train', streaming=True)
        print(next(iter(dataset)))

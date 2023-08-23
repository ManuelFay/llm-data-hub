from unittest import TestCase
from datasets import load_dataset


class TestWikipedia(TestCase):
    def test_load_wikipedia_remote(self):
        # Remote URL and builder file
        dataset = load_dataset('wikipedia', "20220301.fr", split='train', streaming=True)
        print(next(iter(dataset)))

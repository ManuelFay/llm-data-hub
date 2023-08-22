from unittest import TestCase
from datasets import load_dataset, load_from_disk


class TestGutenberg(TestCase):
    def test_load_gutenberg_local(self):
        dataset = load_from_disk('./dataset_collection/french/project_gutenberg/scrapping/data/formatted/')
        print(next(iter(dataset)))

    def test_load_gutenberg_remote(self):
        # Remote URL and builder file
        dataset = load_dataset('manu/ProjectGutenberg_fr', split='train', streaming=True)
        print(next(iter(dataset)))

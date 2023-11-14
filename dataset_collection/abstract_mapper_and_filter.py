"""Templates for mappers and filters to be used in dataset_construction/construct_dataset.py"""

"""To be used to filter from the hf dataset which is not in the correct format"""
from typing import Dict
import abc


class Mapper(abc.ABC):
    def mapper_fn(self, example) -> Dict:
        """Keep only columns programme_id and transcript and rename as id, text"""
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        return self.mapper_fn(*args, **kwargs)


class Filter(abc.ABC):
    def filter_fn(self, example) -> bool:
        """Keep only columns programme_id and transcript and rename as id, text"""
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        return self.filter_fn(*args, **kwargs)

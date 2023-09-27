"""To be used to filter from the hf dataset which is not in the correct format"""
from typing import Dict


class Mapper:
    def mapper_fn(self, example) -> Dict:
        """Keep only columns programme_id and transcript and rename as id, text"""
        return {"text": example["transcript"], "id": example['programme_id']}

    def __call__(self, *args, **kwargs):
        return self.mapper_fn(*args, **kwargs)


class Filter:
    def filter_fn(self, example) -> bool:
        """Keep only columns programme_id and transcript and rename as id, text"""
        return isinstance(example["text"], str) and len(example["text"]) > 100

    def __call__(self, *args, **kwargs):
        return self.filter_fn(*args, **kwargs)

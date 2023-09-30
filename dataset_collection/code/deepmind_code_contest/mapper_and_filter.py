"""To be used to filter from the hf dataset teven/code_contests which is not in the correct format"""
from typing import Dict
from dataset_collection.abstract_mapper_and_filter import Mapper, Filter


class CodeContestMapper(Mapper):
    def mapper_fn(self, example) -> Dict:
        """Keep only columns programme_id and transcript and rename as id, text"""
        return {"text": example["description"] + "\nSolution:\n\n" + example["solution"], "id": example['name']}


class CodeContestFilter(Filter):
    def filter_fn(self, example) -> bool:
        """Keep only columns programme_id and transcript and rename as id, text"""
        return example["language"] == "PYTHON3"

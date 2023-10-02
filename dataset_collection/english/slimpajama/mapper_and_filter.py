"""To be used to filter from the hf dataset which is not in the correct format"""
from typing import Dict
from dataset_collection.abstract_mapper_and_filter import Mapper, Filter


class SlimPajamaMapper(Mapper):
    def mapper_fn(self, example) -> Dict:
        """Keep only columns programme_id and transcript and rename as id, text"""
        return {"text": example["text"], "id": f"{example['meta']['redpajama_set_name']}_{hash(example['text'])}"}


class SlimPajamaFilter(Filter):
    def filter_fn(self, example) -> bool:
        """Remove binary option trading samples"""
        raise NotImplementedError

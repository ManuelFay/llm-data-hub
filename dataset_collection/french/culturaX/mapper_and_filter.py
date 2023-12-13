"""To be used to filter from the hf dataset which is not in the correct format"""
from typing import Dict
from dataset_collection.abstract_mapper_and_filter import Mapper, Filter


class CulturaXMapper(Mapper):
    def mapper_fn(self, example) -> Dict:
        """Keep only columns programme_id and transcript and rename as id, text"""
        # todo: regex transform PI info (IBAN, phone numbers, banks) ?
        return {"text": example["text"], "id": example['source'] + "_" + example["url"]}


class CulturaXFilter(Filter):
    def filter_fn(self, example) -> bool:
        """Remove binary option trading samples"""
        return "binary" not in example["id"]

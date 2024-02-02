"""To be used to filter from the hf dataset which is not in the correct format"""
from typing import Dict
from random import random
from dataset_collection.abstract_mapper_and_filter import Mapper, Filter


class UnbabelFrEnMapper(Mapper):
    def mapper_fn(self, example) -> Dict:
        """Keep only columns programme_id and transcript and rename as id, text"""
        # todo: regex transform PI info (IBAN, phone numbers, banks) ?
        if random() < 0.5:
            return {"text": f"{example['en']}\t{example['fr']}", "id":  hash(example["en"])}
        return {"text": f"{example['fr']}\t{example['en']}", "id":  hash(example["en"])}


class UnbabelFrEnFilter(Filter):
    def filter_fn(self, example) -> bool:
        """Remove binary option trading samples"""
        raise NotImplementedError

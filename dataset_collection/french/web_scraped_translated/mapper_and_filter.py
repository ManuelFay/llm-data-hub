"""To be used to filter from the hf dataset Nicolas-BZRD/Original_Songs_Lyrics_with_French_Translation which is not in the correct format"""
from typing import Dict
from dataset_collection.abstract_mapper_and_filter import Mapper, Filter


class WebPageMapper(Mapper):
    def mapper_fn(self, example) -> Dict:
        """Keep only columns programme_id and transcript and rename as id, text"""
        text = f"{example['en']}\t{example['fr']}" if hash(example["en"]) % 2 == 0 else f"{example['fr']}\t{example['en']}"
        return {"text": text, "id": f"{hash(example['en'])}"}


class WebPageFilter(Filter):
    def filter_fn(self, example) -> bool:
        """Keep only columns programme_id and transcript and rename as id, text"""
        return len(example["text"]) > 20

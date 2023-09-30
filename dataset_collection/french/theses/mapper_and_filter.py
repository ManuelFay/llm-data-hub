"""To be used to filter from the hf dataset Nicolas-BZRD/Original_Songs_Lyrics_with_French_Translation which is not in the correct format"""
from typing import Dict
from dataset_collection.abstract_mapper_and_filter import Mapper, Filter


class ThesisMapper(Mapper):
    def mapper_fn(self, example) -> Dict:
        """Keep only columns programme_id and transcript and rename as id, text"""
        fr_text = f"{example['title_fr']}\n\n{example['abstract_fr']}"
        en_text = f"{example['title_en']}\n\n{example['abstract_en']}"
        text = f"{fr_text}\n\n{en_text}" if hash(fr_text) % 2 == 0 else f"{en_text}\n\n{fr_text}"
        return {"text": text, "id": example['id']}


class ThesisFilter(Filter):
    def filter_fn(self, example) -> bool:
        """Keep only columns programme_id and transcript and rename as id, text"""
        return isinstance(example["abstract_fr"], str) and len(example["abstract_fr"]) > 50

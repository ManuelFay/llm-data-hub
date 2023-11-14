"""To be used to filter from the hf dataset Nicolas-BZRD/Original_Songs_Lyrics_with_French_Translation which is not in the correct format"""
from typing import Dict
from dataset_collection.abstract_mapper_and_filter import Mapper, Filter


class LyricsMapper(Mapper):
    def mapper_fn(self, example) -> Dict:
        """Keep only columns programme_id and transcript and rename as id, text"""
        text = f"{example['title']}\n{example['artist_name']}\n{example['album_name']} - {example['year']}\n\n{example['original_version']}\n\n{example['french_version']}"
        return {"text": text, "id": f"{example['title']}_{example['artist_name']}"}


class LyricsFilter(Filter):
    def filter_fn(self, example) -> bool:
        """Keep only columns programme_id and transcript and rename as id, text"""
        return isinstance(example["language"], str) and example["language"] == "en"

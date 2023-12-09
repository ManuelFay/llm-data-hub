"""To be used to filter from the hf dataset which is not in the correct format"""
from typing import Dict
from dataset_collection.abstract_mapper_and_filter import Mapper, Filter


class SlimPajamaMapper(Mapper):
    def mapper_fn(self, example) -> Dict:
        """Keep only columns programme_id and transcript and rename as id, text"""
         # downloads/extracted/4ad9ba9d1d3de3cd39d79f1bbc8e71ec91c449bf2f82f24e22ba357def3dfd24
        return {"text": example["text"], "id": f"{example['meta']['redpajama_set_name']}_{hash(example['text'])}"}


class SlimPajamaFilter(Filter):
    def filter_fn(self, example) -> bool:
        # todo - filter for books3
        raise NotImplementedError

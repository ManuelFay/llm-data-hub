from typing import Tuple
from dataset_collection.abstract_mapper_and_filter import Filter


class PerplexityFilter(Filter):
    def __init__(self, model, perplexity_bounds: Tuple[float, float] = (10, 1000)):
        self.kenlm_model = model
        self.perplexity_bounds = perplexity_bounds


    def get_perplexity_single(self, sentence):
        return self.kenlm_model.get_perplexity(sentence)

    def filter_fn(self, example) -> bool:
        """Keep only columns programme_id and transcript and rename as id, text"""
        perplexity = self.get_perplexity_single(example["text"])
        return self.perplexity_bounds[0] <= perplexity <= self.perplexity_bounds[1]
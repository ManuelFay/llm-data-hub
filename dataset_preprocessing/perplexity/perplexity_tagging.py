from dataset_preprocessing.perplexity.model import KenlmModel


def get_perplexity_single(sentence, model):
    return model.get_perplexity(sentence)


class PerplexityTagger:
    def __init__(self, kenlm_model: KenlmModel, perplexity_bounds=(10, 1000)):
        self.kenlm_model = kenlm_model
        self.perplexity_bounds = perplexity_bounds

    def get_perplexity_single(self, sentence):
        return self.kenlm_model.get_perplexity(sentence)

    # in-place tagging of the "text" column, to a "perplexity" column
    def tag_hf_dataset(self, dataset):
        # map over dataset
        dataset = dataset.map(
            lambda example: {
                "perplexity": get_perplexity_single(example["text"], self.kenlm_model),
                "text": example["text"],
            },
            batched=False,
            num_proc=4,
        )
        return dataset

    def filter_by_perplexity(self, dataset):
        return dataset.filter(
            lambda example: self.perplexity_bounds[0] <= example["perplexity"] <= self.perplexity_bounds[1])


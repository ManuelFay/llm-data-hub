from dataset_preprocessing.perplexity.model import KenlmModel


def get_perplexity_single(example, model):
    return {
        "perplexity": model.get_perplexity(example["text"]),
        "text": example["text"],
    }


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
            get_perplexity_single,
            batched=False,
            num_proc=4,
            fn_kwargs={"model": self.kenlm_model}
        )
        return dataset

    def filter_by_perplexity(self, dataset):
        return dataset.filter(
            lambda example: self.perplexity_bounds[0] <= example["perplexity"] <= self.perplexity_bounds[1])

from dataset_preprocessing.perplexity.model import KenlmModel


class PerplexityTagger:
    def __init__(self, kenlm_model: KenlmModel):
        self.kenlm_model = kenlm_model

    def get_perplexity_single(self, sentence):
        return self.kenlm_model.get_perplexity(sentence)

    # in-place tagging of the "text" column, to a "perplexity" column
    def tag_hf_dataset(self, dataset):
        # map over dataset
        dataset = dataset.map(
            lambda example: {
                "perplexity": self.get_perplexity_single(example["text"]),
                "text": example["text"],
            },
            batched=True,
            num_proc=4,
            batch_size=1,
        )
        return dataset


if __name__ == "__main__":
    # trained on french wikipedia
    tagger = PerplexityTagger(KenlmModel.from_pretrained(model_dataset="wikipedia", language="fr"))
    print(tagger.get_perplexity_single("Ceci est un test"))
    print(tagger.get_perplexity_single("zer tt ihg oejr"))

    from datasets import load_dataset
    dataset = load_dataset('manu/illuin_youtube_subtitles_text_only', split='train', streaming=False)

    # time it
    import time
    start = time.time()
    dataset = tagger.tag_hf_dataset(dataset)
    end = time.time()

    # print first values
    for sample in dataset[:10]:
        print(sample["perplexity"])
        print(sample["text"])
        print("------------")

    print(f"Tagged {len(dataset)} samples in {end-start} seconds")
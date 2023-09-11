from dataset_preprocessing.perplexity.model import KenlmModel
from dataset_preprocessing.perplexity.perplexity_tagging import PerplexityTagger

if __name__ == "__main__":
    # trained on french wikipedia
    tagger = PerplexityTagger(KenlmModel.from_pretrained(model_dataset="wikipedia", language="fr"),
                              perplexity_bounds=(20, 1000))
    print(tagger.get_perplexity_single("Ceci est un test"))
    print(tagger.get_perplexity_single("zer tt ihg oejr"))

    from datasets import load_dataset

    # dataset = load_dataset('manu/illuin_youtube_subtitles_text_only', split='train', streaming=False)
    # dataset = load_dataset('manu/illuin_layout_dataset_text_only', split='train', streaming=False)
    # dataset = load_dataset('manu/dila_legifrance', split='train', streaming=False)
    dataset = load_dataset('manu/bnf_gallica', split='train', streaming=False)

    # time
    import time

    start = time.time()
    dataset = tagger.tag_hf_dataset(dataset)
    end = time.time()

    print(f"Tagged {len(dataset)} samples in {end - start} seconds")

    # sort dataset by perplexity
    dataset = dataset.sort("perplexity")

    # plot perplexity distribution
    import matplotlib.pyplot as plt

    # show from 0 et 10000
    plt.hist(dataset["perplexity"], bins=100, range=(0, 2000))
    plt.show()

    dataset = tagger.filter_by_perplexity(dataset)
    # print first 5 and last 5 samples
    print(dataset[:5])
    print(dataset[-5:])

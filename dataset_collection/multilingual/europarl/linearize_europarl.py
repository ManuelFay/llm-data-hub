import random
from datasets import load_dataset


def linearize_row(row):
    dict = row["translation"]
    languages = list(dict.keys())
    translation, original = (dict[languages[0]], dict[languages[1]]) if random.random() > 0.5 else (
    dict[languages[1]], dict[languages[0]])
    return {"id": hash(row["translation"][languages[0]]), "text": f"{translation}\t{original}"}


def linearize_dataset(dataset, subset):
    language1, language2 = subset.split("-")
    dataset = load_dataset(dataset, lang1=language1, lang2=language2, streaming=False)
    dataset = dataset.map(linearize_row)
    dataset = dataset.remove_columns(["translation"])
    return dataset


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, default="europarl_bilingual")
    parser.add_argument("--subset", type=str, default="en-fr")
    parser.add_argument("--hub_id", type=str, default="manu/europarl-en-fr")
    args = parser.parse_args()

    ds = linearize_dataset(args.dataset, args.subset)
    ds.push_to_hub(args.hub_id)

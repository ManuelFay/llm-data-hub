import os
from zipfile import ZipFile
import datasets
from tqdm import tqdm


class BNFExtractor:
    def __init__(self, root_dir, save_dir):
        self.root_dir = root_dir
        self.save_dir = save_dir
        # List all files in nested directories
        self.files = []
        for root, dirs, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith('.zip'):
                    self.files.append(os.path.join(root, file))

    def extract(self):
        for file in self.files:
            if file.endswith('.zip'):
                print(f'Extracting {file}')
                with ZipFile(file, 'r') as zipObj:
                    zipObj.extractall(self.save_dir)

    def line_level_filtering(self, textlines):
        # Remove lines with less than 5 characters
        return [line for line in textlines if len(line) > 5]

    def document_level_filtering(self, textlines) -> bool:
        # remove docs with less than 50 lines
        if len(textlines) < 50:
            return False
        text = '\n'.join(textlines)
        # Remove documents with less than 10000 characters
        if len(text) < 10000:
            return False
        # Remove documents with more than 1000000 characters
        if len(text) > 100000:
            return False
        return True

    def convert(self, data_dir, ark_whitelist=None):
        # walk all files in a directory using os.walk
        def gen():
            for root, dirs, files in tqdm(os.walk(data_dir), desc=f"Exploring {data_dir}"):
                for file in files:
                    ark = file[:-4]
                    if ark_whitelist is not None and ark not in ark_whitelist:
                        continue
                    if file.endswith('.txt'):
                        with open(os.path.join(root, file), 'r') as f:
                            text_lines = f.readlines()
                            text_lines = self.line_level_filtering(text_lines)
                            if self.document_level_filtering(text_lines):
                                # Add the text to the dataset
                                yield {'id': ark, 'text': '\n'.join(text_lines)}
                        # Create an empty dataset

        ds = datasets.Dataset.from_generator(gen)
        return ds


if __name__ == '__main__':
    # CLI arguments
    import argparse

    parser = argparse.ArgumentParser(description='Extract raw files from Gallica BNF')
    parser.add_argument('--root_dir', type=str, help='Root directory of the Gallica dataset')
    parser.add_argument('--save_dir', type=str, help='Directory where the extracted files will be saved')
    parser.add_argument('--hub_id', type=str, default=None, help='HF hub id to push the dataset to')
    parser.add_argument('--ark_ref', type=str, help='Path to a csv with metadata about the documents')
    args = parser.parse_args()
    extractor = BNFExtractor(args.root_dir, args.save_dir)
    extractor.extract()

    # ark whitelist
    import pandas as pd
    ark_ref = pd.read_csv(args.ark_ref)
    ark_whitelist = set(ark_ref[ark_ref["mean_nqa"] > 90]["ark"].values)
    print(f"Number of documents with NQA > 90: {len(ark_whitelist)}")

    dataset = extractor.convert(args.save_dir, ark_whitelist=ark_whitelist)

    # combine with csv info file
    # map with column types to string
    dataset = dataset.map(lambda x: {"id": x["id"],
                                     "text": x["text"],
                                     "author": ark_ref[ark_ref["ark"] == x["id"]]["author"].values[0],
                                     "title": ark_ref[ark_ref["ark"] == x["id"]]["title"].values[0],
                                     "mean_nqa": ark_ref[ark_ref["ark"] == x["id"]]["mean_nqa"].values[0],
                                     "date": ark_ref[ark_ref["ark"] == x["id"]]["date"].values[0],
                                     "subject": ark_ref[ark_ref["ark"] == x["id"]]["subject"].values[0],
                                     "rights": ark_ref[ark_ref["ark"] == x["id"]]["rights"].values[0],
                                     "original_folder": ark_ref[ark_ref["ark"] == x["id"]]["original_folder"].values[0],
                                     })


    print("Dataset size:", len(dataset))
    print("Running perplexity tagging")
    # perplexity tagging
    from dataset_preprocessing.perplexity.model import KenlmModel
    from dataset_preprocessing.perplexity.perplexity_tagging import PerplexityTagger

    tagger = PerplexityTagger(KenlmModel(model_dataset="wikipedia", language="fr"), perplexity_bounds=(10, 1000))
    dataset = tagger.tag_hf_dataset(dataset)
    dataset = tagger.filter_by_perplexity(dataset)
    print("Dataset size after filtering:", len(dataset))

    # combine with CSV index document
    if args.hub_id is not None:
        print("Pushing the dataset to the HF hub")
        dataset.push_to_hub(args.hub_id, private=False)

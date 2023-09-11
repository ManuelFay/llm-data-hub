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

    def convert(self, data_dir):
        # walk all files in a directory using os.walk
        def gen():
            for root, dirs, files in tqdm(os.walk(data_dir), desc=f"Exploring {data_dir}"):
                for file in files:
                    if file.endswith('.txt'):
                        with open(os.path.join(root, file), 'r') as f:
                            text = f.read()
                        # Add the text to the dataset
                        yield {'id': file[:-4], 'text': text}
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
    args = parser.parse_args()
    extractor = BNFExtractor(args.root_dir, args.save_dir)
    extractor.extract()
    dataset = extractor.convert(args.save_dir)
    if args.hub_id is not None:
        print("Pushing the dataset to the HF hub")
        dataset.push_to_hub(args.hub_id, private=True)

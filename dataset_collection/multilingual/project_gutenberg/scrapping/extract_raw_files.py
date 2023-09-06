import os
from zipfile import ZipFile
import datasets


class GutenbergExtractor:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        # List all files in nested directories
        self.files = []
        for root, dirs, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith('-8.zip'):
                    self.files.append((os.path.join(root, file), file))

    def extract(self):
        def gen():
            for filepath, file in self.files:
                if file.endswith('.zip'):
                    print(f'Extracting {file}')
                    with ZipFile(filepath, 'r') as zipObj:
                        # to temp directory
                        zipObj.extractall(self.root_dir)

                    # Convert from latin-1 to utf-8
                    if file.endswith('-8.zip'):
                        with open(os.path.join(self.root_dir, file.replace(".zip", ".txt")), 'r', encoding='iso-8859-1') as f:
                            text = f.read()
                    elif file.endswith('-0.zip'):
                        with open(os.path.join(self.root_dir, file.replace(".zip", ".txt")), 'r', encoding='utf-8') as f:
                            text = f.read()
                    else:
                        continue
                    # Add the text to the dataset
                    yield {'id': file[:-4], 'text': text}

        ds = datasets.Dataset.from_generator(gen)
        return ds


if __name__ == '__main__':
    # CLI arguments
    import argparse
    parser = argparse.ArgumentParser(description='Extract raw files from Project Gutenberg')
    parser.add_argument('--root_dir', type=str, help='Root directory of the Project Gutenberg dataset')
    parser.add_argument('--hub_id', type=str, default=None, help='HF hub id to push the dataset to')

    args = parser.parse_args()
    extractor = GutenbergExtractor(args.root_dir)
    ds = extractor.extract()
    if args.hub_id is not None:
        print("Pushing the dataset to the HF hub")
        ds.push_to_hub(args.hub_id, private=False)
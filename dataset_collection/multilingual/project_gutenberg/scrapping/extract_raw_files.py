import os
from zipfile import ZipFile
import datasets
import re


class GutenbergExtractor:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        # List all files in nested directories
        self.dirs = [dir for dir in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, dir))]

    def extract(self, basedir):
        files = [file for file in os.listdir(basedir) if
                 os.path.isfile(os.path.join(basedir, file)) and file.endswith('.zip')]

        def gen():
            processed_files = set()
            for file in files:
                try:
                    if file.endswith('.zip') and file[:-6] not in processed_files:
                        print(f'Extracting {file}')
                        with ZipFile(os.path.join(basedir, file), 'r') as zipObj:
                            # to temp directory
                            zipObj.extractall(self.root_dir)

                        # Convert from latin-1 to utf-8
                        if file.endswith('-8.zip'):
                            with open(os.path.join(self.root_dir, file.replace(".zip", ".txt")), 'r',
                                      encoding='iso-8859-1') as f:
                                text = f.read()
                            yield {'id': file[:-4], 'text': text}
                        elif file.endswith('-0.zip'):
                            with open(os.path.join(self.root_dir, file.replace(".zip", ".txt")), 'r',
                                      encoding='utf-8') as f:
                                text = f.read()
                        else:
                            raise ValueError("Unknown encoding")

                        start_idx = re.search(r'\*\*\*( )?START OF (THE|THIS) PROJECT GUTENBERG EBOOK.*\*\*\*\n{1,6}(Produced by .*\n)(.*?\n)+?\n{3,8}', text)
                        end_idx = re.search(r'\n{3,8}(End of (the)? Project Gutenberg |\*\*\*( )?END OF THIS PROJECT GUTENBERG EBOOK.*\*\*\*\n)', text)
                        # keep only book text
                        text = text[start_idx.end() if start_idx else None: end_idx.start() if end_idx else None]
                        os.remove(os.path.join(self.root_dir, file.replace(".zip", ".txt")))
                        processed_files.add(file[:-6])
                        yield {'id': file[:-4], 'text': text}

                        # Add the text to the dataset
                except UnicodeDecodeError as exception:
                    print(exception)

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

    for dir in extractor.dirs:
        ds = extractor.extract(os.path.join(args.root_dir, dir))
        tries = 0

        while tries < 5:
            try:
                ds.push_to_hub(args.hub_id, split=dir)
                break
            except Exception as e:
                tries += 1
                if tries < 5:
                    print(f"Push to hub failed, retrying for the {tries} time")
                else:
                    raise e

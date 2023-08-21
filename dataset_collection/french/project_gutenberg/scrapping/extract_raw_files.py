import os
from zipfile import ZipFile


class GutenbergExtractor:
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
            print(f'Extracting {file}')
            with ZipFile(file, 'r') as zipObj:
                zipObj.extractall(self.save_dir)


if __name__ == '__main__':
    # CLI arguments
    import argparse
    parser = argparse.ArgumentParser(description='Extract raw files from Project Gutenberg')
    parser.add_argument('--root_dir', type=str, help='Root directory of the Project Gutenberg dataset')
    parser.add_argument('--save_dir', type=str, help='Directory where the extracted files will be saved')
    args = parser.parse_args()
    extractor = GutenbergExtractor(args.root_dir, args.save_dir)
    extractor.extract()

# Scraping Project Gutenberg

Project Gutenberg is a library of over 70,000 free eBooks. The goal of this project is to scrape the website and extract .txt files from the books.

## Usage

To scrape the website (fist page only), run the following command:

```bash
wget -w 2 -m -H https://www.gutenberg.org/robot/harvest?filetypes[]=txt&langs[]=fr
``` 

This will download all the .txt files in the French language to the current directory in ZIP files.

Alternatively, to get all files over all pages, run the following command:

```bash
python scrap_website.py --save_path data/links.txt
wget -i data/links.txt -P data/zipped/
```



To unzip the files, run the following command:

```bash
python extract_raw_files.py --root_dir data/zipped/ --save_dir data/unzipped/
```

To create a dataset, run the following command:

```bash
python convert_extracted_to_hf_dataset.py --data_dir data/unzipped/ --save_dir data/formatted/ --hub_id manu/ProjectGutenberg_fr
```

```bash
sbatch --job-name=cpu --nodes=1 --time=1:00:00 -p cpu_short --cpus-per-task 16 --error=log.err --output=log.out --wrap="python scrap_website.py --save_dir data/"
sbatch --job-name=cpu_wget --nodes=1 --time=1:00:00 -p cpu_short --cpus-per-task 8 --error=wget.err --output=wget.out --wrap="wget -i data/links_de.txt -P data/de/"
```
## Stats

We obtain 2547 books in French, for a total of ~1.1Gb of text and 172.1 million words.
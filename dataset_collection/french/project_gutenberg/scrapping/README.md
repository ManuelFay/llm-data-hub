# Scraping Project Gutenberg

Project Gutenberg is a library of over 70,000 free eBooks. The goal of this project is to scrape the website and extract .txt files from the books.

## Usage

To scrape the website, run the following command:

```bash
wget -w 2 -m -H https://www.gutenberg.org/robot/harvest?filetypes[]=txt&langs[]=fr
``` 

This will download all the .txt files in the French language to the current directory in ZIP files.

To unzip and normalize the files, run the following command:
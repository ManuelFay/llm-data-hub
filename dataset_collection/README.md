# Datasets

This directory contains the datasets gathered for the LLM project.

## Dataset Format

Processed datasets are stored in the HuggingFace Datasets format, and can be loaded using the `load_dataset()` function from the `datasets` library.
They should at least contain the following fields:
- `text`: The text to be used for training (Value: `string`)
- `id`: The id of the text (Value: `string`)

## Dataset List

### French
Sizes are given in the HuggingFace Datasets format, which is the size of the compressed dataset on disk.

- [x] Oscar (french split)
    - Command: `load_dataset('oscar', "unshuffled_deduplicated_fr", split='train', streaming=True)`
    - 430.5 Gb (62.2B words)
- [x] French Wikipedia
    - Command: `load_dataset('wikipedia', '20220301.fr', split='train', streaming=True)`
    - 5.8 Gb (1.1B words)
- [x] French Gutenberg Project
    - Command: `load_dataset('manu/ProjectGutenberg_fr', split='train', streaming=True)`
    - 670 Mb (172M words)
- [x] Illuin Layout Dataset (Text Only)
    - Command: `load_dataset('manu/illuin_layout_dataset_text_only', split='train', streaming=True)`
    - 540 Mb (170M words)
- [x] Illuin Youtube Subtitles (Text Only)
    - Command: `load_dataset('manu/illuin_youtube_subtitles_text_only', split='train', streaming=True)`
    - 400 Mb (120M words)
- [x] OpenSubtitles (french)
    - Command: `load_dataset('manu/french_open_subtitles', split='train', streaming=True)`
    - 130Mb (28M words)
- [x] French Legal Texts (DILA LEGIFRANCE)
    - Command: `load_dataset('manu/dila_legifrance', split='train', streaming=True)`
    - 1.3Gb (200M words)
- [x] French Questions Reponses (DILA)
    - 1 Gb
- [x] French KALI/ CNIL etc  (DILA)
    - 1 - 10Gb depending on what we include
- [x] French BnF (Gallica)
    - Command: `load_dataset('manu/bnf_gallica', split='train', streaming=True)`
    - 1.7 Gb
- [x] French Wikisource
    - Command: `load_dataset('manu/wikisource_fr', split='train', streaming=True)`
    - 11 Gb
- [ ] French Translated Lyrics
    - Command: `load_dataset('manu/french_translated_lyrics', split='train', streaming=True)`
- [ ] ...


### Multi-Lingual

- [x] Project Gutenberg
    - Command: `load_dataset('manu/project_gutenberg', split='<lang_tag>', streaming=True)`
    - 14.6 Gb

To be continued ...


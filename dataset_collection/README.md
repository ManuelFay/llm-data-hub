# Datasets

This directory contains the datasets gathered for the LLM project.

## Dataset Format

Processed datasets are stored in the HuggingFace Datasets format, and can be loaded using the `load_dataset()` function from the `datasets` library.
They should at least contain the following fields:
- `text`: The text to be used for training (Value: `string`)
- `id`: The id of the text (Value: `string`)

## Dataset List

### French

- [x] Oscar (french split)
  - Command: `load_dataset('oscar', "unshuffled_deduplicated_fr", split='train', streaming=True)`
- [x] French Wikipedia
    - Command: `load_dataset('wikipedia', '20220301.fr', split='train', streaming=True)`
- [x] French Gutenberg Project
    - Command: `load_dataset('manu/ProjectGutenberg_fr', split='train', streaming=True)`
- [x] Illuin Layout Dataset (Text Only)
    - Command: `load_dataset('manu/illuin_layout_dataset_text_only', split='train', streaming=True)`
- [x] Illuin Youtube Subtitles (Text Only)
    - Command: `load_dataset('manu/illuin_youtube_subtitles_text_only', split='train', streaming=True)`
- [ ] French Translated Lyrics
    - Command: `load_dataset('manu/french_translated_lyrics', split='train', streaming=True)`
- [ ] ...


To be continued ...


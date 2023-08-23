# Illuin Youtube Subtitles

This dataset contains subtitles from over 62.6k videos from Youtube (over 16k hours of video) in French.
The subtitles are in French and are aligned with the videos.

## Dataset Source

Data is retrieved with a scrapbot from Youtube, that use Tor proxies to avoid being blocked.
Scrapbot ran for over 4 months to retrieve the data.

Data is then cleaned to remove automatically generated subtitles, and subtitles that are not in French.

## Creating the dataset

The dataset is loaded with the following command, from the original dataset stored on Illuin's GCP storage:

```python
 # load_dataset with script: illuin_youtube_subtitles_original_script.py
```

Dataset is then transformed and saved with the following command:

```bash
 python original_dataset_preprocessor.py --raw_dataset_path "manu/illuin_youtube_subtitles_text_only_raw" --hub_id "manu/illuin_youtube_subtitles_text_only"
```

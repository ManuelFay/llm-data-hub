# French Open Subtitles

Subtitle dumps from reddit user u/milahu.

https://www.reddit.com/r/DataHoarder/comments/w7sgcz/5719123_subtitles_from_opensubtitlesorg/
https://archive.org/details/opensubtitles.org.dump.9180519.to.9521948.by.lang.2023.04.26

The torrent file is downloaded, then the subtitles are extracted from the archive using the following command:

```bash
 python db_converter.py -d ~/Downloads/opensubtitles.org.dump.9180519.to.9521948.by.lang.2023.04.26/langs/fre.db  -p ./data/unzipped
```

and then formatted to the HuggingFace Datasets format using the following command:

```bash
python srt_to_hf_dataset.py --data_dir data --save_dir data/formatted --hub_id manu/french_open_subtitles
```

Size is ~130MB from 5479 movies after stripping timestamps and other metadata.
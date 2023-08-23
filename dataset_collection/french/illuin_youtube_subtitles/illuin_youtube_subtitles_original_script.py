# This file is written by Bruno Hays, part of the Whisper team at Illuin Technology.
import csv
import os
from pathlib import Path
from typing import Optional, List, Dict, Tuple

import gcsfs
import datasets

PATH_TO_CSV_TRAIN = \
    Path("randstad-techlab-datasets/yt_french_crawl_csv/yt_ds_csv_15_mai_deduplicated/yt_crawl_dataset_train.csv")
PATH_TO_CSV_TEST = \
    Path("randstad-techlab-datasets/yt_french_crawl_csv/yt_ds_csv_15_mai_deduplicated/yt_crawl_dataset_test.csv")


def get_google_token() -> Optional[str]:
    return os.getenv("GCS_TOKEN")


class YtScrapping(datasets.GeneratorBasedBuilder):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _info(self):
        return datasets.DatasetInfo(
            description="dataset resulting from the scrapping of the French youtube",
            features=datasets.Features(
                {
                    "video_path": datasets.Value("string"),
                    "sentence": datasets.Value("string"),
                    "start_timestamp": datasets.Value("float"),
                    "end_timestamp": datasets.Value("float")
                }
            ),
            supervised_keys=None,
        )

    def _load_split(self, csv_path: str, fs: gcsfs.GCSFileSystem) -> Tuple[List[str], List[List[Dict]]]:
        audio_files: List[str] = []
        samples: List[List[Dict]] = []
        with fs.open(str(csv_path), "r", encoding="utf-8") as r:
            lines = csv.DictReader(r)
            current_file = None
            for sample in lines:
                file = sample["video_path"]
                if current_file != file:
                    current_file = file
                    audio_files.append(sample["video_path"])
                    samples.append([sample])
                    continue
                samples[-1].append(sample)
        return audio_files, samples

    def _split_generators(self, dl_manager):
        fs = gcsfs.GCSFileSystem(token=get_google_token(), access="read_only")
        train_audio_files, train_samples = self._load_split(str(PATH_TO_CSV_TRAIN), fs)
        test_audio_files, test_samples = self._load_split(str(PATH_TO_CSV_TEST), fs)
        return [
            datasets.SplitGenerator(name="train", gen_kwargs={"filepaths": train_audio_files,
                                                              "samples_list": train_samples}),
            datasets.SplitGenerator(name="test", gen_kwargs={"filepaths": test_audio_files,
                                                             "samples_list": test_samples}),
        ]

    def _generate_examples(self, filepaths, samples_list):
        for filepath, samples in zip(filepaths, samples_list):
            for sample in samples:
                start_timestamp = float(sample["start_timestamp"])
                end_timestamp = float(sample["end_timestamp"])
                video_path = sample["video_path"]
                yield f"{video_path}_{start_timestamp}-{end_timestamp}", {
                    "video_path": video_path,
                    "sentence": sample["sentence"],
                    "start_timestamp": start_timestamp,
                    "end_timestamp": end_timestamp}

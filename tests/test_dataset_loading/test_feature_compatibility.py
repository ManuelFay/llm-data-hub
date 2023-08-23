from unittest import TestCase
from itertools import islice

from datasets import load_dataset, interleave_datasets, Value


class TestFeatureCompat(TestCase):
    def test_all_datasets_can_merge(self):
        # oscar
        oscar_dataset = load_dataset('oscar-corpus/OSCAR-2301', "fr", split='train',
                                     streaming=True)
        oscar_dataset = oscar_dataset.cast_column("id", Value(dtype="string"))

        # wikipedia
        wikipedia_dataset = load_dataset('wikipedia', "20220301.fr", split='train',
                                         streaming=True)
        wikipedia_dataset = wikipedia_dataset.remove_columns(["title", "url"])

        # gutenberg
        gutenberg_dataset = load_dataset('manu/ProjectGutenberg_fr', split='train',
                                         streaming=True)

        # youtube subtitles
        youtube_dataset = load_dataset('manu/illuin_youtube_subtitles_text_only', split='train',
                                         streaming=True)

        # layout dataset
        layout_dataset = load_dataset('manu/illuin_layout_dataset_text_only', split='train', streaming=True)

        # OpenSubtitles
        french_opensubtitles = load_dataset('manu/french_open_subtitles', split='train', streaming=True)

        mixed_dataset = interleave_datasets([oscar_dataset, wikipedia_dataset, gutenberg_dataset, youtube_dataset, layout_dataset, french_opensubtitles])

        print(list(islice(mixed_dataset, 6)))

        mixed_dataset_with_oversampling = interleave_datasets([oscar_dataset, wikipedia_dataset],
                                                              probabilities=[0.8, 0.2], seed=42)
        print(list(islice(mixed_dataset_with_oversampling, 2)))

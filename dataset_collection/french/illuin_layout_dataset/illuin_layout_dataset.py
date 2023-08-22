# coding=utf-8
import json
import os

import datasets

# from PIL import Image

logger = datasets.logging.get_logger(__name__)

_CITATION = """\
@misc{Faysse2021XLM,
  title={Illuin Layout Dataset: Layout dataset for pretraining layout models},
  author={Bilel Omrani, Manuel Faysse},
  year={2022},
}
"""
_DESCRIPTION = """\
"""


# def load_image(image_path):
#     image = Image.open(image_path).convert("RGB")
#     w, h = image.size
#     return image, (w, h)


class LayoutDataConfig(datasets.BuilderConfig):
    """BuilderConfig for LayoutData"""

    def __init__(self, **kwargs):
        """BuilderConfig for LayoutData.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(LayoutDataConfig, self).__init__(**kwargs)


class LayoutData(datasets.GeneratorBasedBuilder):
    """Layout dataset."""

    BUILDER_CONFIGS = [
        LayoutDataConfig(name="layoutdata", version=datasets.Version("2.0.0"), description="Layout dataset"),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "text": datasets.Value("string"),
                    # "words": datasets.Sequence(datasets.Value("string")),
                    # "bboxes": datasets.Sequence(datasets.Sequence(datasets.Value("int64"))),
                    # "image_tokens": datasets.Sequence(datasets.Value("int64")),
                    # "image_path": datasets.Value("string"),
                    # "style": datasets.Sequence(feature={'fontname': datasets.Value(dtype='string'),
                    #                                    'fontsize': datasets.Value(dtype='float32')})
                }
            ),
            supervised_keys=None,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        try:
            downloaded_filename = "illuin_layout_dataset.zip"
            downloaded_file = dl_manager.download_and_extract(downloaded_filename)
        except:
            downloaded_filename = "data/illuin_layout_dataset.zip"
            downloaded_file = dl_manager.download_and_extract(downloaded_filename)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": f"{downloaded_file}/train/"}
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION, gen_kwargs={"filepath": f"{downloaded_file}/validation"}
            ),
        ]

    def _generate_examples(self, filepath):
        logger.info("⏳ Generating examples from = %s", filepath)
        ann_dir = os.path.join(filepath, "samples")
        # img_dir = os.path.join(filepath, "images")
        # token_dir = os.path.join(filepath, "image_tokens")
        for guid, file in enumerate(sorted(os.listdir(ann_dir))):
            file_path = os.path.join(ann_dir, file)
            # image_path = os.path.join(img_dir, file)
            # image_path = image_path.replace("json", "jpg")

            # token_path = os.path.join(token_dir, file)
            # token_path = token_path.replace(".json", "_beit_tokens.json")
            try:
                with open(file_path, "r", encoding="utf8") as f:
                    data = json.load(f)
                # with open(token_path, "r", encoding="utf8") as f:
                #     data_tokens = json.load(f)
            except json.decoder.JSONDecodeError:
                logger.warning(f"File {file_path} not read properly.")
                continue

            yield guid, {"id": str(guid),
                         "text": " ".join(data["text"]),
                         # "words": data["text"],
                         # "bboxes": data["normalized_boxes"],
                         # "style": data["style"],
                         # "image_tokens": data_tokens["microsoft/dit-base_image_tokens"],
                         # "image_path": image_path
                         }

import pandas as pd
import requests
import whisper
import numpy as np
import os
from tqdm import tqdm


def download_mp3(url, download_path="data/audio.mp3"):
    try:
        with requests.get(url) as response:
            response.raise_for_status()
            content_type = response.headers.get('content-type')
            if content_type == 'audio/mpeg':
                with open(download_path, 'wb') as file:
                    file.write(response.content)
                return True
    except:
        print("Failed to download audio", url)
    return False


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, default="french_podcast.csv")
    parser.add_argument("--output_file", type=str, default="data/french_podcast_transcribed.csv")
    parser.add_argument("--model_size", type=str, default="large")
    parser.add_argument("--hub_id", type=str, default=None)
    args = parser.parse_args()

    df = pd.read_csv(args.input_file)
    model = whisper.load_model(args.model_size)
    # decoding_options = whisper.DecodingOptions(language="fr")

    for index, row in tqdm(df.iterrows(), total=len(df)):
        if isinstance(row["transcript"], float) and np.isnan(row["transcript"]):
            continue

        if download_mp3(row['audio_podcast_link'], download_path="data/audio.mp3"):
            try:
                df.loc[index, "transcript"] = model.transcribe("data/audio.mp3")["text"]
            except Exception as e:
                print("Failed to transcribe", row['audio_podcast_link'], e)
                df.loc[index, "transcript"] = "FAILED"
            os.remove("data/audio.mp3")

        if index % 10 == 0:
            df.to_csv(args.output_file, index=False)

    df.to_csv(args.output_file, index=False)

    if args.hub_id:
        from datasets import load_dataset
        dataset = load_dataset("csv", data_files=args.output_file)
        dataset.push_to_hub(args.hub_id)

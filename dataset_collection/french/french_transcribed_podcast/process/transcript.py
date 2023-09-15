import pandas as pd
import requests
import whisper
import pickle
import os

df = pd.read_csv('french_podcast.csv')

def download_mp3(url):
    try:
        with requests.get(url) as response:
            response.raise_for_status()
            content_type = response.headers.get('content-type')
            if content_type == 'audio/mpeg':
                with open("audio.mp3", 'wb') as file:
                    file.write(response.content)
                return 1
    except:
        pass
    return -1

number_idx = len(df.index)
model = whisper.load_model("small")

if os.path.exists("index.pickle"):
    with open("index.pickle", "rb") as index_file:
        idx = pickle.load(index_file)
else:
    idx = 0

while idx < number_idx:
    audio = download_mp3(df.loc[idx]['audio_podcast_link'])
    if audio != -1:
        try: df.loc[idx]["transcript"] = model.transcribe("audio.mp3")["text"]
        except:
            pass

    idx += 1

    if idx % 10 == 0:
        df.to_csv("french_podcast.csv", escapechar="§", index=False)
        with open("index.pickle", "wb") as index_file:
            pickle.dump(idx, index_file)

df.to_csv("french_podcast.csv", escapechar="§", index=False)
from datasets import load_dataset

if __name__ == "__main__":
    mls = load_dataset("facebook/multilingual_librispeech", "french", split="train", streaming=False)
    mls = mls.remove_columns(["audio", "file", "speaker_id", "chapter_id"])

    mls.push_to_hub("manu/french_librispeech_text_only")

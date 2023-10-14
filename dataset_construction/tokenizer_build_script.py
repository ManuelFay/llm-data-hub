import argparse
import os
import datasets
from transformers import PreTrainedTokenizerFast, AutoTokenizer, LlamaTokenizerFast
from dataset_construction.fit_tokenizer import fit_tokenizer, build_tokenizer, refit_tokenizer
from huggingface_hub import HfApi

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--hub_id", type=str, default="manu/tok_custom")

    parser.add_argument("--build_from_scratch", action="store_true", default=False)
    parser.add_argument("--sample_size", type=int, default=None)
    parser.add_argument("--upload_corpus_id", type=str, default=None)
    parser.add_argument("--local_save_path", type=str, default="data/tok_all")
    args = parser.parse_args()

    if os.path.exists(args.local_save_path):
        ds = datasets.load_from_disk(args.local_save_path)
    else:
        # concatenate datasets loaded from disks
        ds_fr = datasets.load_from_disk("data/tok_fr")["train"]  # .shuffle()

        ds_code = datasets.load_from_disk("data/tok_code")["train"]  # .shuffle()
        # ds_code = ds_code.select(range(len(ds_code)//2)) # half it

        ds_en = datasets.load_from_disk("data/english_30b")["train"]  # .shuffle()
        print(len(ds_en), ds_en.data.nbytes // 1e9)
        ds_en = ds_en.select(range(len(ds_fr) // 2))
        print(len(ds_en), ds_en.data.nbytes // 1e9)

        print("French")
        print(ds_fr)

        print("Code")
        print(ds_code)

        print("English")
        print(ds_en)

        ds = datasets.concatenate_datasets([ds_code, ds_fr, ds_en])
        print("Shuffling")
        ds = ds.shuffle(seed=42)  # slow

        print(f"Size of Concatenated: {ds.data.nbytes // 1e9} GB")
        print(f"Size of French: {ds_fr.data.nbytes // 1e9} GB, ratio of {ds_fr.data.nbytes / ds.data.nbytes}")
        print(f"Size of Code: {ds_code.data.nbytes // 1e9} GB, ratio of {ds_code.data.nbytes / ds.data.nbytes}")
        print(f"Size of English: {ds_en.data.nbytes // 1e9} GB, ratio of {ds_en.data.nbytes / ds.data.nbytes}")

        ds.save_to_disk(args.local_save_path, max_shard_size="2GB", num_proc=os.cpu_count())

        # ds.save_to_disk("data/tok_all")
        if args.upload_corpus_id:
            for i in range(10):
                try:
                    ds.push_to_hub(args.upload_corpus_id, max_shard_size="2GB")
                    break
                except:
                    print("Failed to push to hub")

    # small scale tests to begin
    if args.sample_size:
        # ds = ds.shuffle(seed=42)
        ds = ds.select(range(args.sample_size))
        print(f"Size of Sampled: {ds.data.nbytes // 1e9} GB")

    example_sentence = "This is a test sentence. On va voir comment elle est gérée .... 123 + 56 = 2567. Let's go! Imagine I have code    4 spaces.\n and a      backslash!! Eléonore est un prénom français. __name__ isInstance"

    build_from_scratch = args.build_from_scratch
    hub_id_suffix = "-scratch" if build_from_scratch else "-refitted"
    if build_from_scratch:
        print("Building from scratch")
        # From scratch
        tok = build_tokenizer()
        tok = fit_tokenizer(tok, ds)

        # Save and upload
        if os.path.exists("data/tokenizer.json"):
            os.remove("data/tokenizer.json")
        tok.save("data/tokenizer.json")
        tok = LlamaTokenizerFast(tokenizer_file="data/tokenizer.json")

        tok.save_pretrained("data/tokenizer_fast")
        tok.push_to_hub(args.hub_id + hub_id_suffix)
        os.remove("data/tokenizer.json")

        # Test
        encoded = tok.encode(example_sentence)
        enc_sent = tok.tokenize(example_sentence)
        print(enc_sent)
        decoded = tok.decode(encoded)
        print(decoded)

    else:
        print("Refitting from pretrained")
        # Refit from pretrained
        tok2 = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")
        tok2 = refit_tokenizer(tok2, ds)
        tok2.save_pretrained("data/tokenizer2_fast")
        tok2.push_to_hub(args.hub_id + hub_id_suffix)

        encoded = tok2.encode(example_sentence)
        enc_sent = tok2.tokenize(example_sentence)
        print(enc_sent)
        decoded = tok2.decode(encoded)
        print(decoded)


    # Dump Pretty readme
    with open("data/tok_config.md", "w") as f:
        # intro
        f.write(f"# Custom Tokenizer\n")
        f.write(f"## Description\n")
        f.write(f"This tokenizer was trained on a concatenation of the following datasets:\n")

        # examples
        f.write(f"## Examples\n")
        f.write(f"Example sentence: {example_sentence}\n")
        f.write(f"Encoded sentence: {enc_sent}\n")
        f.write(f"Decoded sentence: {decoded}\n")

        # usage
        f.write(f"## Usage\n")
        f.write(f"```python\n")
        f.write(f"from transformers import LlamaTokenizerFast\n")
        f.write(f"tok = LlamaTokenizerFast.from_pretrained('<tok_name>')\n")
        f.write(f"tok.tokenize('This is a test sentence')\n")

        # dump dataset stats
        f.write(f"## Dataset Stats\n")
        f.write(f"Samples are trained on dataset `manu/tok-corpus-shuffled`\n")
        f.write(f"The dataset consists of french, english and code samples\n")
        f.write(
            "More info on the dataset can be found [here](https://huggingface.co/datasets/manu/tok-corpus-shuffled)\n")
        if args.sample_size:
            f.write(
                "For speed purposes, the tokenizer was trained on a sample of the dataset. Only the first samples were selected.\n")
            f.write(f"Sample size: {args.sample_size}\n")
            f.write(f"Size of Sampled: {ds.data.nbytes // 1e9} GB\n")

        # dump tokenizer configs
        f.write(f"## Tokenizer Configs\n")
        f.write(f"Build from scratch: {build_from_scratch}\n")
        if not build_from_scratch:
            f.write(f"Pretrained tokenizer: mistralai/Mistral-7B-v0.1\n")
        else:
            f.write(f"Pretrained tokenizer: None\n")

        # tokenizer stats
        f.write(f"Tokenizer is trained with digit separation, whitespaces (for code), byte fallback")

        api = HfApi()
        api.upload_file(
            repo_id=args.hub_id + hub_id_suffix,
            path_or_fileobj=f"data/tok_config.md",
            path_in_repo="tok_information.md",
            repo_type="model",
        )

    os.remove("data/tok_config.md")

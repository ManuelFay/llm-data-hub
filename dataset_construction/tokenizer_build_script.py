import argparse
import datasets
from transformers import PreTrainedTokenizerFast, AutoTokenizer
from dataset_construction.fit_tokenizer import fit_tokenizer, build_tokenizer, refit_tokenizer


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--hub_id", type=str, default="manu/tok_custom")
    parser.add_argument("--build_from_scratch", action="store_true", default=False)
    args = parser.parse_args()

    # concatenate datasets loaded from disks
    ds_fr = datasets.load_from_disk("data/tok_fr")["train"].shuffle()

    ds_code = datasets.load_from_disk("data/tok_code")["train"].shuffle()
    # ds_code = ds_code.select(range(len(ds_code)//2)) # half it

    ds_en = datasets.load_from_disk("data/english_30b")["train"].shuffle()
    ds_en = ds_en.select(range(len(ds_fr)//2))

    print(ds_code)
    print(ds_fr)
    print(ds_en)

    ds = datasets.concatenate_datasets([ds_code,
                                        ds_fr,
                                        ds_en])
    print(ds)

    example_sentence = "This is a test sentence. On va voir comment elle est gérée .... 123 + 56 = 2567. Let's go!"

    build_from_scratch = args.build_from_scratch
    if build_from_scratch:
        print("Building from scratch")
        # From scratch
        tok = build_tokenizer()
        tok = fit_tokenizer(tok, ds)
        tok.save("../data/tokenizer.json")
        tok = PreTrainedTokenizerFast(tokenizer_file="../data/tokenizer.json")
        tok.save_pretrained("../data/tokenizer_fast")
        tok.push_to_hub(args.hub_id + "_scratch")

        encoded = tok.encode(example_sentence)
        print(tok.tokenize(example_sentence))
        decoded = tok.decode(encoded)
        print(decoded)

    else:
        print("Refitting from pretrained")
        # Refit from pretrained
        tok2 = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")
        tok2 = refit_tokenizer(tok2, ds)
        tok2.save_pretrained("../data/tokenizer2_fast")
        tok2.push_to_hub(args.hub_id + "_refitted")

        encoded = tok2.encode(example_sentence)
        print(tok2.tokenize(example_sentence))
        decoded = tok2.decode(encoded)
        print(decoded)

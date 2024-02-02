from typing import Optional
import datasets
from tokenizers import Tokenizer, decoders, models, normalizers, pre_tokenizers, trainers
from transformers import AutoTokenizer, PreTrainedTokenizerFast


def build_tokenizer(
        replacement: str = "▁",
        add_prefix_space: bool = True,
        dropout: Optional[float] = None,
        fuse_unk: Optional[bool] = True,
):
    """
    Build a tokenizer.
    :return: The tokenizer.
    """
    tokenizer = Tokenizer(models.BPE(
        dropout=dropout, unk_token=None, fuse_unk=fuse_unk, byte_fallback=True)
    )
    tokenizer.normalizer = normalizers.NFKC()
    tokenizer.pre_tokenizer = pre_tokenizers.Sequence(
        [pre_tokenizers.Metaspace(replacement=replacement, add_prefix_space=add_prefix_space),
         pre_tokenizers.Digits(individual_digits=True),
         # needs a \n tokenizer
         # pre_tokenizers.Punctuation(),
         # to deal with "......" or "-----" tokens (which might be interesting to have actually)
         ])

    tokenizer.decoder = decoders.Sequence([decoders.ByteFallback(),
                                           decoders.Metaspace(replacement=replacement,
                                                              add_prefix_space=add_prefix_space),
                                           decoders.Fuse(),
                                           decoders.Strip(content=" ", left=1, right=0)])
    return tokenizer


def fit_tokenizer(tokenizer, dataset: datasets.Dataset):
    """
    Fit a tokenizer on a dataset.
    :param tokenizer: The tokenizer to fit.
    :param dataset: The dataset to fit the tokenizer on.
    :return: The fitted tokenizer.
    """

    def batch_iterator(batch_size=1000):
        for i in range(0, len(dataset), batch_size):
            yield dataset[i: i + batch_size]["text"]

    special_tokens = ["<unk>", "<s>", "</s>", "<pad>"]
    special_tokens += [f"<extra_id_{i}>" for i in range(100)]
    bpe_trainer = trainers.BpeTrainer(vocab_size=32000,
                                      min_frequency=2,
                                      show_progress=True,
                                      special_tokens=special_tokens,
                                      limit_alphabet=1000,
                                      initial_alphabet=[],
                                      )
    it = batch_iterator()
    tokenizer.train_from_iterator(it,
                                  trainer=bpe_trainer,
                                  length=len(dataset))
    return tokenizer


def refit_tokenizer(tokenizer: PreTrainedTokenizerFast, dataset: datasets.Dataset):
    """
    Fit a tokenizer on a dataset.
    :param tokenizer: The tokenizer to fit.
    :param dataset: The dataset to fit the tokenizer on.
    :return: The fitted tokenizer.
    """

    def batch_iterator(batch_size=1000):
        for i in range(0, len(dataset), batch_size):
            yield dataset[i: i + batch_size]["text"]

    # is this slowing down everything ?
    ### START OF THE SLOW PART
    new_special_tokens = ["<pad>"]
    # new_special_tokens += [f"<extra_id_{i}>" for i in range(100)]
    it = batch_iterator()

    tokenizer._tokenizer.pre_tokenizer = pre_tokenizers.Sequence(
        [
            # pre_tokenizers.Metaspace(replacement=replacement, add_prefix_space=add_prefix_space),
            pre_tokenizers.Digits(individual_digits=True),
            # pre_tokenizers.Punctuation(),
            # to deal with "......" or "-----" tokens (which might be interesting to have actually)
        ])
    ### END OF THE SLOW PART

    tokenizer = tokenizer.train_new_from_iterator(it,
                                                  vocab_size=32000,
                                                  length=len(dataset),
                                                  new_special_tokens=new_special_tokens,
                                                  )

    return tokenizer


if __name__ == "__main__":
    ds = datasets.load_dataset("manu/illuin_layout_dataset_text_only", split="train")

    example_sentence = "This is a test sentence. On va voir comment elle est gérée .... 123 + 56 = 2567. Let's go!"

    build_from_scratch = False
    if build_from_scratch:
        # From scratch
        tok = build_tokenizer()
        tok = fit_tokenizer(tok, ds)
        tok.save("../data/tokenizer.json")
        tok = PreTrainedTokenizerFast(tokenizer_file="../data/tokenizer.json")
        tok.save_pretrained("../data/tokenizer_fast")
        tok.push_to_hub("manu/tok")

        encoded = tok.encode(example_sentence)
        print(tok.tokenize(example_sentence))
        decoded = tok.decode(encoded)
        print(decoded)

    else:
        # Refit from pretrained
        tok2 = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")
        tok2 = refit_tokenizer(tok2, ds)
        tok2.save_pretrained("../data/tokenizer2_fast")
        tok2.push_to_hub("manu/tok2")

        encoded = tok2.encode(example_sentence)
        print(tok2.tokenize(example_sentence))
        decoded = tok2.decode(encoded)
        print(decoded)

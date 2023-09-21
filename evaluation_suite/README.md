# Evaluation Suite

In order to assess performance given a model checkpoint, we need to be able to run comprehensive evaluation benchmarks.

We aim to evaluate across various axes:

- Languages:
  - Code
  - English
  - French
- Tasks:
  - Language Modeling
  - Few-shot capabilities
  - Instruction following


The objective is to have a target model checkpoint be hosted through TGI, and evaluated for various capabilities.

We will leverage several libraries  and existing benchmarks to achieve so:

- HumanEval (code)
- llm-evaluation-harness (english / language modeling)
- French version of the evaluation harness
- Multilingual: BigBench

Data decontamination will have to be run before training extensively, and verified at evaluation time (13-gram matching).

### Resources

- https://github.com/FastEval/FastEval
- https://github.com/evalplus/evalplus
- https://github.com/EleutherAI/lm-evaluation-harness
- https://github.com/declare-lab/instruct-eval


### Todo

- Set up evaluation pipelines for a HF checkpoint
- Construct data cleaning preprocessing pipelines
- Clean training data


# Usage
### English

```bash
python lm-evaluation-harness/main.py \
    --model hf-causal \
    --model_args pretrained=gpt2 \
    --tasks hellaswag,openbookqa,winogrande,arc_easy,arc_challenge,boolq,piqa \
    --device cuda:0 --batch_size 4 \
    --output_path data/results/gpt2   --limit 100 
    
python instruct-eval/main.py mmlu --model_name llama --model_path chavinlo/alpaca-native
python instruct-eval/main.py bbh --model_name llama --model_path PY007/TinyLlama-1.1B-Chat-v0.1
python instruct-eval/main.py drop --model_name llama --model_path PY007/TinyLlama-1.1B-Chat-v0.1
```

### Code

```bash
python instruct-eval/main.py humaneval  --model_name llama  --n_sample 1 --model_path PY007/TinyLlama-1.1B-Chat-v0.1 --data_path instruct-eval/human_eval/HumanEval.jsonl.gz 
```

### French

```bash
python lm-evaluation-harness/main.py \
    --model hf-causal \
    --model_args pretrained=gpt2 \
    --tasks crows_pairs_french,crows_pairs_french_age,crows_pairs_french_socioeconomic,pawsx_fr,wmt14-fr-en,xnli_fr \
    --device cuda:0 --batch_size 4 \
    --output_path data/results/gpt2_fr   --limit 100 
```

Note: I modified the download script for wm14-fr-en to download the data: unvalid unpacking of args l130 of translation.py.


### Dataset perplexity (per dataset)
```bash
python lm-evaluation-harness/main.py \
    --model hf-causal \
    --model_args pretrained=gpt2 \
    --tasks pile_arxiv,pile_europarl,pile_gutenberg \
    --device cuda:0 --batch_size 4 \
    --output_path data/results/gpt2_fr   --limit 100 
```


## Setup

### Instruct eval

Install dependencies and download data.

```
cd evaluation_suite/instruct-eval
pip install -r requirements.txt
mkdir -p data
wget https://people.eecs.berkeley.edu/~hendrycks/data.tar -O data/mmlu.tar
tar -xf data/mmlu.tar -C data && mv data/data data/mmlu
```

### lm-evaluation-harness

Install dependencies and download data.

```
cd evaluation_suite/lm-evaluation-harness
pip install -e .
```

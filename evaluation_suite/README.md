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
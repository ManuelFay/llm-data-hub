# LLM Data Hub

This repository regroups code related to data gathering, data processing, and data analysis for the CroissantLLM training project.
https://arxiv.org/abs/2402.00786

Organization: https://huggingface.co/croissantllm

## Abstract

We introduce CroissantLLM, a 1.3B language model pretrained on a set of 3T English and French tokens, to bring to the research and industrial community a high-performance, fully open-sourced bilingual model that runs swiftly on consumer-grade local hardware. To that end, we pioneer the approach of training an intrinsically bilingual model with a 1:1 English-to-French pretraining data ratio, a custom tokenizer, and bilingual finetuning datasets. We release the training dataset, notably containing a French split with manually curated, high-quality, and varied data sources. To assess performance outside of English, we craft a novel benchmark, FrenchBench, consisting of an array of classification and generation tasks, covering various orthogonal aspects of model performance in the French Language. Additionally, rooted in transparency and to foster further Large Language Model research, we release codebases, and dozens of checkpoints across various model sizes, training data distributions, and training steps, as well as fine-tuned Chat models, and strong translation models. We evaluate our model through the FMTI framework, and validate 81 % of the transparency criteria, far beyond the scores of even most open initiatives. This work enriches the NLP landscape, breaking away from previous English-centric work in order to strengthen our understanding of multilinguality in language models.

## Installation

Requirements are not all necessary, to install all requirements, run the following command in  a virtual environment:
```bash
make init
```

## More documentation is coming soon

## Citation

```
@misc{faysse2024croissantllm,
      title={CroissantLLM: A Truly Bilingual French-English Language Model}, 
      author={Manuel Faysse and Patrick Fernandes and Nuno Guerreiro and António Loison and Duarte Alves and Caio Corro and Nicolas Boizard and João Alves and Ricardo Rei and Pedro Martins and Antoni Bigata Casademunt and François Yvon and André Martins and Gautier Viaud and Céline Hudelot and Pierre Colombo},
      year={2024},
      eprint={2402.00786},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

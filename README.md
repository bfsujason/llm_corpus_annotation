# LLM Corpus Annotation

## Overview

This repository explores the application of LLMs for annotation tasks in corpus linguistics. It provides tools and experiments for automating three core annotation workflows:

- **POS Tagging** — Part-of-speech tagging guided by established tagsets such as [PKU](http://sighan.cs.uchicago.edu/bakeoff2005/data/pku_spec.pdf) and [CLAWS7](https://ucrel.lancs.ac.uk/claws7tags.html)
- **Dependency Parsing** — Syntactic parsing following [Universal Dependency 2.0](https://universaldependencies.org/u/dep/)
- **Semantic Tagging** — Semantic category annotation based on the [UCREL Semantic Analysis System](https://ucrel.lancs.ac.uk/usas/)

## Installation

- Clone the repository

```bash
git clone https://github.com/bfsujason/llm_corpus_annotation.git
cd llm_corpus_annotation
```

- Install required dependencies for LLM annotation

```bash
pip install openai
pip install diskcache
pip install sentence_splitter
```

- Install optional dependencies for annotation using local models

```bash
pip install hanlp
pip install stanza
pip install pymusas
```

- Apply for an API Key to access LLMs

1. Create a free account on [Aliyun Bailian (阿里云百炼)](https://bailian.console.aliyun.com/)
2. Go to API Key management in the Bailian console and generate a new key (it starts with `sk`)
3. Copy the generated key in the configuration file [config](./config)

## Usage

You can refer to the Jupyter Notebooks in the directory [notebook](./notebook) for more usage

All the prompts used for annotation are stored in the directory [src/prompt](./src/prompt)

```python
# === Import LLM Annotators ===

from src.annotator.pos_tagger import POSTagger
from src.annotator.dep_parser import DEPParser
from src.annotator.sem_tagger import SEMTagger

# === LLM Setting ===

# set tagging mode
# llm | local
mode = "llm"

# specify model name
# deepseek-v3.2 | kimi-k2.5 | glm-4.7 | qwen3-max
llm_model = "deepseek-v3.2"

# turn on/off LLM thinking mode
# True | False
enable_thinking = False

# === Input text to be annotated ===
# Note: Only support Chinese and English

zh_text = "那天晚上我没走掉。陈清扬把我拽住，以伟大友谊的名义叫我留下来。"
en_text = "I did not leave that night - Chen Qingyang caught me and asked me to stay in the name of our great friendship."

# === POS Tagging ===

# --- Chinese POS tagging ---

# choose language and tagset
lang = "chinese"
tagset = "pku"

# load Chinse POS tagger
llm_zh_pku_tagger = POSTagger(
    lang=lang,
    tagset=tagset,
    mode=mode,
    llm_model=llm_model,
    enable_thinking=enable_thinking,
)

# annotate Chinese text
llm_zh_pku_tagger.tag(zh_text)

# --- English POS tagging ---

# choose language and tagset
lang = "english"
tagset = "claws"

# load English POS tagger
llm_en_claws_tagger = POSTagger(
    lang=lang,
    tagset=tagset,
    mode=mode,
    llm_model=llm_model,
    enable_thinking=enable_thinking,
)

# annotate English text
llm_en_claws_tagger.tag(en_text)

# === Dependency Parsing ===

# --- Chinese dependency parsing ---

# choose language and tagset
lang = "chinese"
tagset = "ud"

# load Chinese dependency parser
llm_zh_ud_parer = DEPParser(
    lang=lang,
    tagset=tagset,
    mode=mode,
    llm_model=llm_model,
    enable_thinking=enable_thinking,
)

# annotate Chinese text
llm_zh_ud_parer.tag(zh_text)

# --- English dependency parsing ---

# choose language and tagset
lang = "english"
tagset = "ud"

# load English dependency parser
llm_en_ud_parer = DEPParser(
    lang=lang,
    tagset=tagset,
    mode=mode,
    llm_model=llm_model,
    enable_thinking=enable_thinking,
)

# annotate English text
llm_en_ud_parer.tag(en_text)

# === Semantic Tagging ===

# --- Chinese semantic tagging ---

# choose language and tagset
lang = "chinese"
tagset = "usas"

# load Chinese semantic tagger
llm_zh_usas_tagger = SEMTagger(
    lang=lang,
    tagset=tagset,
    mode=mode,
    llm_model=llm_model,
    enable_thinking=enable_thinking,
)

# annotate Chinese text
llm_zh_usas_tagger.tag(zh_text)

# --- English semantic tagging ---

# choose language and tagset
lang = "english"
tagset = "usas"

# load English semantic tagger
llm_en_usas_tagger = SEMTagger(
    lang=lang,
    tagset=tagset,
    mode=mode,
    llm_model=llm_model,
    enable_thinking=enable_thinking,
)

# annotate English text
llm_en_usas_tagger.tag(en_text)
```

## Acknowledgments & Credits

### Academic Advisors

We are grateful to the following scholars for their valuable insights and suggestions:

- **Dr. Dingjia Liu** - Beijing Foreign Studies University
- **Professor Shuangzi Pang** - Shanghai Jiaotong University

### Excellent NLP Tools
- **[CLAWS7](https://ucrel-api.lancaster.ac.uk/claws/free.html)** - UCREL's highly accurate part-of-speech tagger
- **[HanLP](https://github.com/hankcs/HanLP)** - Multilingual NLP library with strong performance on Chinese text processing
- **[Multilingual-USAS](https://github.com/UCREL/Multilingual-USAS)** - UCREL's Multilingual USAS lexicon
- **[PyMUSAS](https://github.com/UCREL/pymusas)** - Python Multilingual USAS for semantic tagging
- **[spaCy](https://spacy.io/)** - Industrial-strength Natural Language Processing in Python
- **[Stanza](https://stanfordnlp.github.io/stanza/)** - Stanford NLP Group's official Python library with neural network models for many languages

### Important Note on Methodology

**The LLM prompts used in this project are directly informed by and based on the annotation frameworks, methodologies, and linguistic insights developed by the creators of the above tools.** While LLMs may show competitive performance on certain tasks, this success stands on the shoulders of decades of corpus/computational linguistics research embodied in these tools.

The annotation schemas, linguistic categories, and evaluation criteria used in our LLM prompts draw heavily from:
- The part-of-speech tagging systems implemented in CLAWS7, HanLP and spaCy
- The dependency parsing approaches from Stanza
- The semantic tagging framework from UCREL's Multilingual-USAS & PyMUSAS

**This project explores how LLMs can be leveraged for corpus annotation when guided by the expert knowledge encoded in these tools.**

## Limitations and Future Work

This project is ongoing and has several areas that require further development:

### Limitations

- **Prompt Engineering**: The LLM prompts used in experiments need further refinement and optimization. Current prompts may not fully capture the nuances of expert annotation practices.

- **Limited Corpus Diversity**: Experiments have been conducted on a limited range of corpus types. More comprehensive testing is needed.

- **Reproducibility**: LLM outputs can vary between runs. More work is needed to ensure consistency and reproducibility of annotations.

- **Computational Cost**: LLM-based annotation may be more expensive and time-consuming than traditional tools for large-scale corpus annotation.

- **Evaluation Metrics**: Current evaluation metrics may not fully capture the quality differences between LLM and traditional tool outputs.

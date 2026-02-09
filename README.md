# LLM Corpus Annotation

## Overview

This repository explores the application of LLMs for annotation tasks in corpus linguistics.

## Acknowledgments & Credits

### Academic Advisors

We are grateful to the following scholars for their valuable insights and suggestions:

- **Dr. Dingjia Liu** - Beijing Foreign Studies University
- **Professor Shuangzi Pang** - Shanghai Jiaotong University

### Excellent NLP Tools
- **[CLAWS7](https://ucrel.lancs.ac.uk/claws/)** - UCREL's highly accurate part-of-speech tagger
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
- The semantic tagging framework from UCREL's semantic analysis work (PyMUSAS & Multilingual-USAS)

**This project explores how LLMs can be leveraged for corpus annotation when guided by the expert knowledge encoded in these tools.**

## Limitations and Future Work

This project is ongoing and has several areas that require further development:

### Limitations

- **Prompt Engineering**: The LLM prompts used in experiments need further refinement and optimization. Current prompts may not fully capture the nuances of expert annotation practices.

- **Limited Corpus Diversity**: Experiments have been conducted on a limited range of corpus types. More comprehensive testing is needed.

- **Reproducibility**: LLM outputs can vary between runs. More work is needed to ensure consistency and reproducibility of annotations.

- **Computational Cost**: LLM-based annotation may be more expensive and time-consuming than traditional tools for large-scale corpus annotation.

- **Evaluation Metrics**: Current evaluation metrics may not fully capture the quality differences between LLM and traditional tool outputs.

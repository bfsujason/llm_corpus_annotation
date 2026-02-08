# LLM Corpus Annotation

A study of corpus linguistics annotation using Large Language Models (LLMs).

## Overview

This repository explores the application of LLMs for annotation tasks in corpus linguistics. Our experiments demonstrate that LLMs can achieve competitive performance on certain corpus annotation tasks compared to traditional rule-based and statistical NLP tools. However, this work builds directly upon the foundational research and methodologies developed by the creators of these tools.

## Acknowledgments & Credits

### Excellent NLP Tools

- **[HanLP](https://github.com/hankcs/HanLP)** - Multilingual NLP library with strong performance on Chinese text processing
- **[PyMUSAS](https://github.com/UCREL/pymusas)** - Python Multilingual UCREL Semantic Analysis System for semantic tagging
- **[Stanza](https://stanfordnlp.github.io/stanza/)** - Stanford NLP Group's official Python library with neural network models for many languages
- **[spaCy](https://spacy.io/)** - Industrial-strength Natural Language Processing in Python


### Important Note on Methodology

**The LLM prompts used in this project are directly informed by and based on the annotation frameworks, methodologies, and linguistic insights developed by the creators of the above tools.** While LLMs may show strong performance on certain tasks, this success stands on the shoulders of decades of corpus/commputational linguistics research embodied in these tools.

The annotation schemas, linguistic categories, and evaluation criteria used in our LLM prompts draw heavily from:
- The part-of-speech tagging systems implemented in HanLP and spaCy
- The dependency parsing approaches from Stanza
- The semantic tagging framework from UCREL's semantic analysis work (PyMUSAS)

**This project explores how LLMs can be leveraged for corpus annotation when guided by the expert knowledge encoded in these tools.

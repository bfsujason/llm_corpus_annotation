#!/bin/bash

echo "正在安装项目所需模块..."
pip install openai diskcache sentence_splitter hanlp pymusas

echo "正在安装 spaCy 语言模型（离线安装）..."
cd llm_corpus_annotation/res
for file in *.whl; do pip install "$file"; done
cd ..

echo "所有模块安装完成！"
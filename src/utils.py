# bfsujason@163.com

# 单元测试：
# python -m src.utils

import re
import json

import pandas as pd
#from spacy import displacy
from sentence_splitter import SentenceSplitter

'''
from spacy import displacy
from IPython.display import display, HTML
import IPython.core.display as core_display
core_display.display = display
core_display.HTML = HTML

# 自定义依存关系数据
doc = {
    "words": [
        {"text": "我", "tag": ""},
        {"text": "爱", "tag": ""},
        {"text": "自然语言", "tag": ""},
        {"text": "处理", "tag": ""}
    ],
    "arcs": [
        {"start": 0, "end": 1, "label": "nsubj", "dir": "left"},
        {"start": 1, "end": 3, "label": "dobj", "dir": "right"},
        {"start": 2, "end": 3, "label": "compound", "dir": "left"}
    ]
}

# 渲染可视化
displacy.render(doc, style="dep", manual=True)

html = displacy.render(doc, style="dep", manual=True, jupyter=False)

with open("dep.html", "w", encoding="utf-8") as f:
    f.write(html)
'''

def load_data(file_name, limit=None):
    """
    读取 TSV 格式双语语料
    
    :param file_name: .tsv 文件路径
    :param limit: 限定读取数据行数
    :return: DataFrame
    """
    
    try:
        # 读取单个文件
        # on_bad_lines='skip': 跳过格式错误的行
        # quoting=3: 避免引号导致解析错误
        temp_df = pd.read_csv(file_name, sep='\t', header=None, 
                              names=['source', 'target'], 
                              on_bad_lines='skip', quoting=3)
        
        corpus = temp_df.dropna()
        if limit:
            corpus = corpus.head(limit)
        return corpus
    except Exception as e:
       print(f'读取文件 {filename} 失败: {e}')
        
def load_claws_tag(file_name):
    result = []
    with open(file_name, 'rt', encoding='utf-8') as fin:
        for i, line in enumerate(fin):
            record = {}
            record['id'] = f'{i+1:05d}'
            line = line.strip()
            text, tags = line.split('\t')
            tok, pos = [], []
            for tag in tags.split():
               _tok, _pos = tag.split('_')
               tok.append(_tok)
               pos.append(_pos)
            record['text'] = text
            record['tok'] = tok
            record['pos'] = pos
            result.append(record)
    return result
    
def clean_text(text):
    clean_text = []
    text = text.strip()
    lines = text.splitlines()
    for line in lines:
        line = line.strip()
        if line:
            line = re.sub(r'\s+', ' ', line)
            clean_text.append(line)
    return "\n".join(clean_text)

def split_sents(text, lang):
    result = {}
    if lang == 'chinese':
        sents = _split_zh(text)
    elif lang == 'english':
        splitter = SentenceSplitter(language='en')
        sents = splitter.split(text=text) 
        sents = [sent.strip() for sent in sents]
    result['sent'] = sents
    return result
    
def _split_zh(text, limit=1000):
        sent_list = []
        text = re.sub('(?P<quotation_mark>([。？！](?![”’"\'）])))', r'\g<quotation_mark>\n', text)
        text = re.sub('(?P<quotation_mark>([。？！]|…{1,2})[”’"\'）])', r'\g<quotation_mark>\n', text)

        sent_list_ori = text.splitlines()
        for sent in sent_list_ori:
            sent = sent.strip()
            if not sent:
                continue
            else:
                while len(sent) > limit:
                    temp = sent[0:limit]
                    sent_list.append(temp)
                    sent = sent[limit:]
                sent_list.append(sent)

        return sent_list
      
def save_results(results, out_file):
     with open(out_file, "wt", encoding="utf-8") as fout:
        for record in results:
            fout.write(json.dumps(record, ensure_ascii=False) + "\n")
            
if __name__ == '__main__':
    claws_tag_file = 'data/eval/claws7_tag.txt'
    result = load_claws_tag(claws_tag_file)
    print(result)

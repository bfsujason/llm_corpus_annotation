# bfsujason@163.com

# 单元测试：
# python -m src.utils

import os
import glob
import json
import random
import pandas as pd

from collections import defaultdict

def load_data(data_dir, limit=None):
    """
    读取 TSV 格式双语语料
    
    :param data_dir: .tsv 文件目录
    :param limit: 限定读取数据行数
    :return: DataFrame
    """
    
    # 查找指定目录下的 .tsv 文件
    file_pattern = os.path.join(data_dir, '*.tsv')
    all_files = glob.glob(file_pattern)
    
    if not all_files:
        raise FileNotFoundError(f'{data_dir} 下未找到 .tsv 文件')

    df_list = []
    for filename in all_files:
        try:
            # 读取单个文件
            # on_bad_lines='skip': 跳过格式错误的行
            # quoting=3: 避免引号导致解析错误
            temp_df = pd.read_csv(filename, sep='\t', header=None, 
                                  names=['source', 'target'], 
                                  on_bad_lines='skip', quoting=3)
            
            # 添加文件名列
            #temp_df['file_id'] = os.path.basename(filename)
            
            df_list.append(temp_df)
            
        except Exception as e:
           print(f'读取文件 {filename} 失败: {e}')
            
    # 合并所有数据
    if df_list:
        full_corpus = pd.concat(df_list, ignore_index=True)
        
        # 替换空值
        # full_corpus = full_corpus.replace({np.nan: None})
        full_corpus = full_corpus.dropna()
        if limit:
            full_corpus = full_corpus.head(limit)
        return full_corpus
    else:
        return pd.DataFrame()
    
def save_results(results, out_file):
     with open(out_file, "wt", encoding="utf-8") as fout:
        for record in results:
            fout.write(json.dumps(record, ensure_ascii=False) + "\n")
            
if __name__ == '__main__':
    
    
    #conll_file = 'data/eval/en_ewt-ud-test.conllu'
    #jsonl_file = 'data/eval/en_ewt-ud-test.jsonl'
    #conll_file = 'data/eval/zh_gsdsimp-ud-test.conllu'
    #jsonl_file = 'data/eval/zh_gsdsimp-ud-test.jsonl'
    
    #sents = parse_conll(conll_file)
    #save_results(sents, jsonl_file)
    
    #eval_data = load_eval_data(jsonl_file)
    #print(eval_data[:5])
    
    ctb_file = 'data/eval/ctb_5.1_test.tsv'
    jsonl_file = 'data/eval/ctb_5.1_test.jsonl'
    sents = parse_ctb(ctb_file)
    save_results(sents, jsonl_file)

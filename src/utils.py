# bfsujason@163.com

import os
import json
import glob
import logging
import numpy as np
import pandas as pd

# 配置日志
logger = logging.getLogger(__name__)

def load_corpus(data_dir, limit=None):
    """
    读取 TSV 格式双语语料
    
    :param data_dir: .tsv 文件目录
    :param limit: 限定读取数据行数
    :return: DataFrame
    """
    logger.info(f"正在读取语料: {data_dir} ...")
    
    # 查找指定目录下的 .tsv 文件
    file_pattern = os.path.join(data_dir, "*.tsv")
    all_files = glob.glob(file_pattern)
    
    if not all_files:
        raise FileNotFoundError(f"{data_dir} 下未找到 .tsv 文件")

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
           logger.error(f"读取文件 {filename} 失败: {e}")
            
    # 合并所有数据
    if df_list:
        full_corpus = pd.concat(df_list, ignore_index=True)
        
        # 替换空值
        # full_corpus = full_corpus.replace({np.nan: None})
        full_corpus = full_corpus.dropna()
        if limit:
            full_corpus = full_corpus.head(limit)
        logger.info(f"读取成功！共 {len(full_corpus)} 条记录")
        return full_corpus
    else:
        return pd.DataFrame()
        
def load_multiver_corpus(data_file, limit=None):
    """
    读取 JSONL 格式多版本翻译语料
    
    :param data_file: .jsonl 文件路径
    :return: DataFrame
    """
    logger.info(f"正在读取语料: {data_file} ...")
    
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"{data_file} 文件不存在")
    
    try:
        df = pd.read_json(data_file, lines=True)
        
        # 验证数据完整性
        required_cols = ['id', 'source', 'targets']
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"数据格式错误，缺少必要列: {required_cols}")
            
        if limit:
            df = df.head(limit)
        logger.info(f"读取成功！共 {len(df)} 条记录")
        return df
        
    except Exception as e:
        logger.error(f"读取文件 {filename} 失败: {e}")
        return pd.DataFrame()
        
def load_usas_tags(tag_file):
    """
    读取语义标签文件，转换为 Prompt 可用的字符串
    
    :param tag_file: USAS 标签文件路径
    """
    logger.info(f"正在读取标签文件: {tag_file} ...")
    
    if not os.path.exists(tag_file):
        raise FileNotFoundError(f"{tag_file} 文件不存在")
    
    tag_list = []
    with open(tag_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            
            # 文件以 Tab 或 空格 分隔 code 和 description
            parts = line.split(None, 1)
            if len(parts) == 2:
                code, desc = parts
                tag_list.append(f"- {code}: {desc}")
    
    logger.info(f"读取成功！共 {len(tag_list)} 条记录")
    
    # 将列表合并为字符串
    return "\n".join(tag_list)
    
def save_results(results, out_file):
     with open(out_file, "wt", encoding="utf-8") as fout:
        for record in results:
            fout.write(json.dumps(record, ensure_ascii=False) + "\n")
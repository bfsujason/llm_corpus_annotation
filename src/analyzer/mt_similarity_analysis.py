# bfsujason@163.com
# python -m src.analyzer.mt_similarity_analysis

import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

import json
import torch
import logging
import numpy as np
import pandas as pd
from difflib import SequenceMatcher
from sentence_transformers import SentenceTransformer, util

# 配置日志
logger = logging.getLogger(__name__)

class MTSimilarityAnalyzer:
    def __init__(self, jsonl_path, model_name='all-MiniLM-L6-v2'):
        """
        初始化分析器
        :param model_name: 语义向量模型，默认 'all-MiniLM-L6-v2'
            详见 https://www.sbert.net/docs/sentence_transformer/pretrained_models.html
        """
        self.file_path = jsonl_path
        self.data_map = {}      # {version: [list of sentences]}
        self.id_list = []       # [id1, id2, ...]
        self.source_list = []   # [src1, src2, ...]
        self.versions = []
        self.embedding_model = None
        self.model_name = model_name

    def load_data(self, limit=None):
        """加载数据并按版本分组"""
        logger.info(f"正在加载语料: {self.file_path} ...")
        
        # 临时存储数据
        temp_data = {}
        self.id_list = []
        self.source_list = []
        
        count = 0
        with open(self.file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if limit and count >= limit: break
                
                try:
                    record = json.loads(line)
                    targets = record.get('targets', {}) # human, deepseek, qwen
                    source = record.get('source', '')
                    rec_id = record.get('id', '')
                    
                    # 获取译文版本
                    # 初始化数据字典的键值
                    if not temp_data:
                        self.versions = list(targets.keys())
                        for v in self.versions: temp_data[v] = []
                    
                    # 确保所有版本都有译文
                    if all(targets.get(v) for v in self.versions):
                        for v in self.versions:
                            temp_data[v].append(targets[v])
                            
                        # 记录元数据
                        self.id_list.append(rec_id)
                        self.source_list.append(source)
                        
                        count += 1
                        
                except Exception:
                    continue
        
        self.data_map = temp_data
        logger.info(f"数据加载完成: 共 {count} 条数据 (译文版本: {self.versions})")

    def _calc_string_sim(self, text_a, text_b):
        """
        使用 Python 自带的 difflib 计算字符串相似度 (取值范围 0-1)
        https://docs.python.org/3/library/difflib.html#difflib.SequenceMatcher.ratio
        """
        #return SequenceMatcher(None, text_a, text_b).ratio()
        
        # 正向计算
        sim_ab = SequenceMatcher(None, text_a, text_b).ratio()
        # 反向计算
        sim_ba = SequenceMatcher(None, text_b, text_a).ratio()
        
        # 取平均值，保证 Similarity(A, B) == Similarity(B, A)
        return (sim_ab + sim_ba) / 2

    def get_string_similarity_matrix(self):
        """计算基于最长公共子串的相似度矩阵"""
        logger.info("正在计算字符串相似度矩阵 ...")
        n = len(self.versions)
        matrix = np.zeros((n, n))
        
        # 遍历所有译本的两两组合
        for i in range(n):
            for j in range(i, n):
                ver_a = self.versions[i]
                ver_b = self.versions[j]
                
                if i == j:
                    matrix[i][j] = 1.0
                else:
                    # 计算所有句对的平均相似度
                    scores = []
                    for sa, sb in zip(self.data_map[ver_a], self.data_map[ver_b]):
                        scores.append(self._calc_string_sim(sa, sb))
                    avg_score = np.mean(scores)
                    
                    # 填充相似度矩阵
                    matrix[i][j] = avg_score
                    matrix[j][i] = avg_score
        return pd.DataFrame(matrix, index=self.versions, columns=self.versions)

    def get_embedding_similarity_matrix(self):
        """计算基于语义向量的相似度矩阵"""
        logger.info("正在加载向量模型 (可能需要下载) ...")
        if not self.embedding_model:
            self.embedding_model = SentenceTransformer(self.model_name, local_files_only=True)
            
        logger.info("正在计算语义相似度矩阵 ...")
        n = len(self.versions)
        matrix = np.zeros((n, n))
        
        # 将译文文本转换成向量
        embeddings = {}
        for ver in self.versions:
            logger.info(f"  Encoding {ver}...")
            embeddings[ver] = self.embedding_model.encode(self.data_map[ver], convert_to_tensor=True)
            
        # 遍历所有译本的两两组合
        for i in range(n):
            for j in range(i, n):
                ver_a = self.versions[i]
                ver_b = self.versions[j]
                
                if i == j:
                    matrix[i][j] = 1.0
                else:
                    # 获取各版本句子的向量表征
                    vecs_a = embeddings[ver_a]
                    vecs_b = embeddings[ver_b]
                    
                    # 计算所有句对的平均相似度
                    sims = util.pairwise_cos_sim(vecs_a, vecs_b)
                    avg_sim = torch.mean(sims).item()
                    
                    # 填充相似度矩阵
                    matrix[i][j] = avg_sim
                    matrix[j][i] = avg_sim
                    
        return pd.DataFrame(matrix, index=self.versions, columns=self.versions)
        
    def get_divergent_examples(self, ver_a, ver_b, metric='string', top_n=5):
        """
        查找两个版本之间相似度最低的例句
        
        :param ver_a: 译文版本 A
        :param ver_b: 译文版本 B
        :param metric: 'string' (编辑距离) 或 'semantic' (语义向量)
        :param top_n: 返回相似度最低的 n 个例句
        :return: List[Dict]
        """
        if ver_a not in self.data_map or ver_b not in self.data_map:
            logger.error(f"版本 {ver_a} 或 {ver_b} 不存在")
            return []

        logger.info(f"正在检索例句 ({metric}): {ver_a} vs {ver_b} ...")
        
        texts_a = self.data_map[ver_a]
        texts_b = self.data_map[ver_b]
        scores = []

        # 逐句计算相似度
        if metric == 'string':
            for i, (ta, tb) in enumerate(zip(texts_a, texts_b)):
                score = self._calc_string_sim(ta, tb)
                scores.append((i, score))
                
        elif metric == 'semantic':
            # 加载模型
            if not self.embedding_model:
                logger.info("正在加载向量模型...")
                self.embedding_model = SentenceTransformer(self.model_name)
            
            # 文本批量向量化
            vecs_a = self.embedding_model.encode(texts_a, convert_to_tensor=True)
            vecs_b = self.embedding_model.encode(texts_b, convert_to_tensor=True)
            # 计算成对余弦相似度
            cosine_scores = util.pairwise_cos_sim(vecs_a, vecs_b)
            
            for i, score in enumerate(cosine_scores):
                scores.append((i, float(score)))

        # 相似度排序：分数越低，差异越大
        scores.sort(key=lambda x: x[1]) # 升序排列

        # 提取相似度差异最大的 N 个句对
        results = []
        for idx, score in scores[:top_n]:
            results.append({
                "id": self.id_list[idx],
                "source": self.source_list[idx],
                "ver_a": texts_a[idx],
                "ver_b": texts_b[idx],
                "score": score
            })
            
        return results
    
    @staticmethod
    def print_divergence(examples, metric_name, ver_a, ver_b):
        print(f"\n=== {metric_name} 相似度最低的例句  Top 3 ===")
        for i, ex in enumerate(examples[:3]):
            print(f"\n[{i+1}] ID: {ex['id']} | Sim Score: {ex['score']:.4f}")
            print(f"原文: {ex['source']}")
            print("-" * 60)
            print(f"{ver_a.capitalize()}: {ex['ver_a']}")
            print(f"{ver_b.capitalize()}: {ex['ver_b']}")
            print("=" * 60)    
        
# === 单元测试 ===
if __name__ == "__main__":

    # 打印日志信息
    logging.basicConfig(level=logging.INFO)
    
    # 加载数据
    data_file = 'data/output/0_mt_generation.jsonl'
    analyzer = MTSimilarityAnalyzer(data_file)
    analyzer.load_data(limit=10)
    
    # 计算字符串相似度矩阵
    df_str_sim = analyzer.get_string_similarity_matrix()
    print(f"\n计算完成，结果如下：\n{df_str_sim}\n")
    
    # 计算语义相似度矩阵
    df_sem_sim = analyzer.get_embedding_similarity_matrix()
    print(f"\n计算完成，结果如下：\n{df_sem_sim}")
    
    # 查找典型例句
    ver_a = 'human'
    ver_b = 'deepseek-v3.2'
    
    metric = 'string'
    diffs_str = analyzer.get_divergent_examples(ver_a, ver_b, metric)
    analyzer.print_divergence(diffs_str, "表层形式 (String)", ver_a, ver_b)
    
    metric = 'semantic'
    diffs_sem = analyzer.get_divergent_examples(ver_a, ver_b, metric)
    analyzer.print_divergence(diffs_sem, "深层语义 (Semantic)", ver_a, ver_b)
    
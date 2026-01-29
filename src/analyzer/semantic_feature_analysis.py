# bfsujason@163.com
# python -m src.analyzer.semantic_feature_analysis

import json
import logging
import pandas as pd
from collections import Counter, defaultdict

# 配置日志
logger = logging.getLogger(__name__)

class SemanticFeatureAnalyzer:
    def __init__(self, jsonl_path):
        self.file_path = jsonl_path
        # 格式: self.stats[version]['usas'][tag] = count
        self.stats = defaultdict(lambda: {
            "usas": Counter(),
            "total_tags": 0,
        })
        self.versions = set()

    def load_and_count(self, limit=None):
        """统计所有标签频次"""
        logger.info(f"正在加载数据: {self.file_path} ...")

        count = 0
        with open(self.file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if limit and count >= limit: break
                
                try:
                    record = json.loads(line)
                    #print(record)
                    
                    # 统计中文
                    # if annotations.get('source_zh'):
                    #    self._process_version('source', annotations['source_zh'])
                    
                    # 统计各版本英文
                    targets = record.get('targets', {})
                    for ver, anno in targets.items():
                        if anno: 
                            self._process_version(ver, anno)
                    count += 1
                    
                except Exception as e:
                    logger.error(f"加载数据错误：{e}")
                    return None
        
        logger.info(f"加载完成！")

    def _process_version(self, version, anno):
        """统计单个版本的 USAS"""
        self.versions.add(version)
        tags_list = anno.get('usas_tags', [])
        if not tags_list: tags_list = []
        
        for item in tags_list:
            tag_code = item.get('tag', '')
            desc = item.get('desc', '')
            if not tag_code: continue
            tag = tag_code.strip()
            major_cat = tag[0].upper()
            self.stats[version]['usas'][major_cat] += 1
            self.stats[version]['total_tags'] += 1

    def get_feature_report(self, target_tags, versions=None):
        """
        根据指定的特征列表生成统计报表 (DataFrame)
        
        :param feature_type: 'pos' 或 'dep'
        :param target_tags_map: 字典
               - 字典: {'被动': ['pass'], '名词': ['NN', 'compound']} (支持归类)
        :param versions: 指定要对比的版本列表 (默认对比所有英文译本)
        :return: DataFrame (含 Version, Feature, Count, Percentage)
        """
        logger.info(f"正在统计 USAS 特征频率 ...")
        
        if versions is None:
            # 默认排除 source，只看英文译本
            versions = [v for v in self.versions if v != 'source']
            
        data = []
        search_dict = target_tags

        for ver in versions:
            if ver not in self.stats: continue
            
            # 获取分母 (总词数或总关系数)
            total = self.stats[ver]['total_tags']
            if total == 0: continue
            
            # 获取该版本的计数器
            counter = self.stats[ver]['usas']
            
            for label, search_keys in search_dict.items():
                hits = 0
                for recorded_tag, count in counter.items():
                    if recorded_tag in search_keys:
                        hits += count
                
                percentage = (hits / total) * 100
                
                data.append({
                    "Version": ver,
                    "Feature Label": label,
                    "Count": hits,
                    "Percentage": percentage
                })
                
        logger.info(f"统计完成！")      
        return pd.DataFrame(data)
        
    @staticmethod
    def get_examples(
        data_file,
        target_tag='S', 
        ver_a='human', 
        ver_b='deepseek-v3.2',
        min_diff=2
    ):
        divergent_examples = []
        
        with open(data_file, 'r', encoding='utf-8') as f:
            for line_no, line in enumerate(f):
                try:
                    rec = json.loads(line)
                    targets = rec.get('targets', {})
                    if not targets: continue
                    
                    data_a = targets.get(ver_a)
                    data_b = targets.get(ver_b)
                    if not data_a or not data_b: continue
                    
                    # === 内部函数：统计句法特征数量 ===
                    def analyze_semantic(ver_data):
                        count = 0
                        keywords = []
                        
                        tags_list = ver_data.get('usas_tags', [])
                        if not tags_list: tags_list = []
                        
                        for i, item in enumerate(tags_list):
                            is_match = False
                            tag_code = item.get('tag', '')
                            text = item.get('text', '')
                            
                            if not tag_code: continue
                            tag = tag_code.strip()
                            major_cat = tag[0].upper()
                            if  major_cat == target_tag:
                                is_match = True
                                
                            if is_match:
                                count += 1
                                keywords.append(f"{text}({tag})")   
                         
                        return count, keywords

                    # --- 执行分析 ---
                    count_a, keys_a = analyze_semantic(data_a)
                    count_b, keys_b = analyze_semantic(data_b)
                    
                    diff = count_a - count_b
                    
                    if diff >= min_diff:
                        text_a = data_a.get('raw_text', [])
                        text_b = data_b.get('raw_text', [])
                        
                        divergent_examples.append({
                            "id": rec['id'],
                            "source": rec['source']['raw_text'],
                            "ver_a_text": text_a,
                            "ver_a_count": count_a,
                            "ver_a_keys": keys_a,
                            "ver_b_text": text_b,
                            "ver_b_count": count_b,
                            "ver_b_keys": keys_b,
                            "diff": diff
                        })
                        
                except Exception as e:
                    logger.error(f"加载数据错误：{e}")
                    return None

        divergent_examples.sort(key=lambda x: x['diff'], reverse=True)
        return divergent_examples
 
    @staticmethod
    def print_examples(examples, target_tags, ver_a, ver_b, top_n=3):
        print(f"\n=== {target_tags} 类差异最大的例句 Top {top_n} ===\n")
        for i, res in enumerate(examples[:top_n]):
            print(f"[{i+1}] ID: {res['id']} | Diff: +{res['diff']}")
            print(f"[source]: {res['source']}")
            print("-" * 60)
            print(f"[{ver_a}] (Count: {res['ver_a_count']}):")
            print(f"Text: {res['ver_a_text']}")
            print(f"Keywords: {res['ver_a_keys']}")
            print("-" * 60)
            print(f"[{ver_b}] (Count: {res['ver_b_count']}):")
            print(f"Text: {res['ver_b_text']}")
            print(f"Keywords: {res['ver_b_keys']}")
            print("=" * 60 + "\n")
            
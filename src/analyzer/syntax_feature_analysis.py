# bfsujason@163.com
# python -m src.analyzer.syntax_feature_analysis

import json
import logging
import pandas as pd
from collections import Counter, defaultdict

# 配置日志
logger = logging.getLogger(__name__)

class SyntaxFeatureAnalyzer:
    def __init__(self, jsonl_path):
        self.file_path = jsonl_path
        # 格式: self.stats[version]['pos'/'dep'][tag] = count
        self.stats = defaultdict(lambda: {
            "pos": Counter(),
            "dep": Counter(),
            "total_tokens": 0,
            "total_deps": 0
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
        """统计单个版本的 POS 和 Dep"""
        self.versions.add(version)
        
        # --- 统计 POS ---
        # anno_data['pos'] 是 List[List[str]] (多句)
        for sent_pos in anno.get('pos', []):
            self.stats[version]['total_tokens'] += len(sent_pos)
            self.stats[version]['pos'].update(sent_pos)
            
        # --- 统计 Dependency ---
        # anno_data['dep'] 是 List[List[List[head, rel]]]
        for sent_dep in anno.get('dep', []):
            # 过滤掉标点关系 (可选)
            rels = [rel for head, rel in sent_dep if rel != 'punct']
            
            self.stats[version]['total_deps'] += len(rels)
            self.stats[version]['dep'].update(rels)

    def get_feature_report(self, feature_type, target_tags, versions=None):
        """
        根据指定的特征列表生成统计报表 (DataFrame)
        
        :param feature_type: 'pos' 或 'dep'
        :param target_tags_map: 字典或列表
               - 字典: {'被动': ['pass'], '名词': ['NN', 'compound']} (支持归类)
        :param versions: 指定要对比的版本列表 (默认对比所有英文译本)
        :return: DataFrame (含 Version, Feature, Count, Percentage)
        """
        logger.info(f"正在统计 {feature_type} 特征频率 ...")
        
        if versions is None:
            # 默认排除 source，只看英文译本
            versions = [v for v in self.versions if v != 'source']
            
        data = []
        search_dict = target_tags

        for ver in versions:
            if ver not in self.stats: continue
            
            # 获取分母 (总词数或总关系数)
            total = self.stats[ver]['total_tokens'] if feature_type == 'pos' else self.stats[ver]['total_deps']
            if total == 0: continue
            
            # 获取该版本的计数器
            counter = self.stats[ver][feature_type]
            
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
        feature_type='pos',
        target_tags=["NN", "NNS", "NNP", "NNPS"], 
        ver_a='deepseek-v3.2', 
        ver_b='human',
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
                    def analyze_syntax(ver_data):
                        count = 0
                        keywords = []
                        
                        tokens_list = ver_data.get('tokens', [])
                        #dep_list = ver_data.get('dep', [])
                        feature_list = ver_data.get(feature_type, [])
                        for tokens, sent_feature in zip(tokens_list, feature_list):
                            #for i, (head, rel) in enumerate(sent_dep):
                            for i, feature in enumerate(sent_feature):
                                
                                is_match = False
                                if feature_type == 'dep':
                                    feature = feature[1]
                                if feature in target_tags:
                                    is_match = True
                                
                                if is_match:
                                    count += 1
                                    if i < len(tokens):
                                        # 记录单词和对应的句法标签
                                        keywords.append(f"{tokens[i]}({feature})")   
                         
                        return count, keywords

                    # --- 执行分析 ---
                    count_a, keys_a = analyze_syntax(data_a)
                    count_b, keys_b = analyze_syntax(data_b)
                    
                    diff = count_a - count_b
                    
                    if diff >= min_diff:
                        text_a = data_a.get('raw_text', "")
                        text_b = data_b.get('raw_text', "")
                        
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
        print(f"\n=== {target_tags} 差异最大的例句 Top {top_n} ===\n")
        for i, res in enumerate(examples[:3]):
            print(f"[{i+1}] ID: {res['id']} (Diff: +{res['diff']})")
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
  
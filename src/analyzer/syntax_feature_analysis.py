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
        # 数据结构: self.stats[version]['pos'/'dep'][tag] = count
        self.stats = defaultdict(lambda: {
            "pos": Counter(),
            "dep": Counter(),
            "total_tokens": 0,
            "total_deps": 0
        })
        self.versions = set()

    def load_data(self, limit=None):
        """统计所有标签频次"""
        logger.info(f"正在加载数据: {self.file_path} ...")
        
        count = 0
        with open(self.file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if limit and count >= limit: break
                
                try:
                    record = json.loads(line)
                    annotations = record.get('annotations', {})
                    
                    # 统计中文
                    if annotations.get('source_zh'):
                        self._count_single_version('source', annotations['source_zh'])
                    
                    # 统计各版本英文
                    targets = annotations.get('targets_en', {})
                    for ver, anno in targets.items():
                        if anno:
                            self._count_single_version(ver, anno)
                    count += 1
                            
                except Exception as e:
                    continue
        
        logger.info(f"加载完成！")

    def _count_single_version(self, version, anno_data):
        """统计单个版本的 POS 和 Dep"""
        self.versions.add(version)
        
        # --- 统计 POS ---
        # anno_data['pos'] 是 List[List[str]] (多句)
        for sent_pos in anno_data.get('pos', []):
            self.stats[version]['total_tokens'] += len(sent_pos)
            self.stats[version]['pos'].update(sent_pos)
            
        # --- 统计 Dependency ---
        # anno_data['dep'] 是 List[List[List[head, rel]]]
        for sent_dep in anno_data.get('dep', []):
            # 过滤掉标点关系 (可选)
            rels = [rel for head, rel in sent_dep if rel != 'punct']
            
            self.stats[version]['total_deps'] += len(rels)
            self.stats[version]['dep'].update(rels)

    def get_feature_report(self, feature_type, target_tags_map, versions=None):
        """
        根据指定的特征列表生成统计报表 (DataFrame)
        
        :param feature_type: 'pos' 或 'dep'
        :param target_tags_map: 字典或列表
               - 字典: {'被动': ['pass'], '名词': ['NN', 'compound']} (支持归类)
               - 列表: ['NN', 'VB'] (直接匹配)
        :param versions: 指定要对比的版本列表 (默认对比所有英文译本)
        :return: DataFrame (含 Version, Feature, Count, Percentage)
        """
        logger.info(f"正在统计 {feature_type} 特征频率 ...")
        
        if versions is None:
            # 默认排除 source，只看英文译本
            versions = [v for v in self.versions if v != 'source']
            
        data = []
        
        # 统一将 target_tags_map 转为字典格式: {Label: [substrings]}
        if isinstance(target_tags_map, list):
            search_dict = {tag: [tag] for tag in target_tags_map}
        else:
            search_dict = target_tags_map

        for ver in versions:
            if ver not in self.stats: continue
            
            # 获取分母 (总词数或总关系数)
            total = self.stats[ver]['total_tokens'] if feature_type == 'pos' else self.stats[ver]['total_deps']
            if total == 0: continue
            
            # 获取该版本的计数器
            counter = self.stats[ver][feature_type]
            
            for label, search_keys in search_dict.items():
                # 模糊匹配求和 (例如搜索 'NN'，匹配 'NN', 'NNS', 'NNP')
                # 或者搜索 'pass', 匹配 'nsubj:pass', 'aux:pass'
                hits = 0
                for recorded_tag, count in counter.items():
                    # 只要 recorded_tag 包含 search_keys 中的任意一个字符串
                    if any(k in recorded_tag for k in search_keys):
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
    def get_divergent_examples(
        data_file,
        feature_type='pos',
        target_tags=['conj', 'cc'], 
        ver_a='deepseek-v3.2', 
        ver_b='human',
        min_diff=2
    ):
        divergent_examples = []
        
        with open(data_file, 'r', encoding='utf-8') as f:
            for line_no, line in enumerate(f):
                try:
                    rec = json.loads(line)
                    targets = rec.get('annotations', {}).get('targets_en', {})
                    if not targets: continue
                    
                    data_a = targets.get(ver_a)
                    data_b = targets.get(ver_b)
                    
                    if not data_a or not data_b: continue
                    
                    # === 内部函数：统计句法特征数量 ===
                    def analyze_syntax(ver_data):
                        count = 0
                        keywords = []
                        
                        tokens_list = ver_data.get('tokens', [])
                        
                        if feature_type == 'dep':
                            dep_list = ver_data.get('dep', [])
                            for tokens, sent_dep in zip(tokens_list, dep_list):
                                for i, (head, rel) in enumerate(sent_dep):
                                    
                                    is_match = False
                                    for tag in target_tags:
                                        # 完全相等 (例如 rel='cc', tag='cc') -> 命中
                                        if rel == tag:
                                            is_match = True
                                            break
                                        # 子类型 (例如 rel='cc:preconj', tag='cc') -> 命中
                                        # 注意：加冒号，防止 'cc' 匹配到 'ccomp'
                                        if rel.startswith(tag + ":"):
                                            is_match = True
                                            break
                                    
                                    if is_match:
                                        count += 1
                                        if i < len(tokens):
                                            # 记录单词和对应的句法标签
                                            keywords.append(f"{tokens[i]}({rel})")   
                        elif feature_type == 'pos':
                            pos_list = ver_data.get('pos', [])
                            for tokens, sent_pos in zip(tokens_list, pos_list):
                                for i, pos in enumerate(sent_pos):
                                    
                                    is_match = False
                                    for tag in target_tags:
                                        # 完全相等 (例如 rel='cc', tag='cc') -> 命中
                                        if pos.startswith(tag):
                                            is_match = True
                                            break
                                    if is_match:
                                        count += 1
                                        if i < len(tokens):
                                            # 记录单词和对应的词性标签
                                            keywords.append(f"{tokens[i]}({pos})")   
                         
                        return count, keywords

                    # --- 执行分析 ---
                    count_a, keys_a = analyze_syntax(data_a)
                    count_b, keys_b = analyze_syntax(data_b)
                    
                    diff = count_a - count_b
                    
                    if diff >= min_diff:
                        text_a = " ".join(data_a.get('sentences', []))
                        text_b = " ".join(data_b.get('sentences', []))
                        
                        divergent_examples.append({
                            "id": rec['id'],
                            "source": rec['annotations']['source_zh'].get('sentences', [""])[0],
                            "ver_a_text": text_a,
                            "ver_a_count": count_a,
                            "ver_a_keys": keys_a,
                            "ver_b_text": text_b,
                            "ver_b_count": count_b,
                            "ver_b_keys": keys_b,
                            "diff": diff
                        })
                        
                except Exception as e:
                    continue

        divergent_examples.sort(key=lambda x: x['diff'], reverse=True)
        return divergent_examples
    
# === 单元测试 ===
if __name__ == "__main__":

    # 打印日志信息
    logging.basicConfig(level=logging.INFO)
    
    # 加载数据
    data_file = 'data/output/1_syntax_annotation.jsonl'
    analyzer = SyntaxFeatureAnalyzer(data_file)
    analyzer.load_and_count(limit=None)
    print(analyzer.stats)
    
    # === 分析数据: 词性赋码统计 ===
    pos_config = {
        "名词 (NN)": ["NN"],   # 匹配 NN, NNS, NNP...
        "动词 (VB)": ["VB"],
        "形容词 (JJ)": ["JJ"],
        "代词 (PRP)": ["PRP"],
        "介词 (IN)": ["IN"],
        "限定词 (DT)": ["DT"]
    }

    df_pos = analyzer.get_feature_report(
        feature_type='pos', 
        target_tags_map=pos_config,
    )
    print(df_pos)
    print("\n")
    
    # === 分析数据: 句法关系统计 ===
    dep_config = {
        "被动语态 (Passive)": ["pass"],                   # 匹配 nsubj:pass, aux:pass
        "名词修饰/复合 (Compound)": ["compound", "flat"],
        "从句结构 (Clause)": ["advcl", "ccomp", "acl"],
        "并列结构 (Coordination)": ["conj", "cc"],
        "定语/修饰 (Modifier)": ["amod", "advmod"]
    }

    # 获取报表
    df_dep = analyzer.get_feature_report(
        feature_type='dep', 
        target_tags_map=dep_config,
        versions=['human', 'deepseek-v3.2', 'qwen3-max']
    )
    print(df_dep)
    

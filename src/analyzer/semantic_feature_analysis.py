import json
import pandas as pd
from collections import Counter, defaultdict
from tqdm import tqdm

class SemanticFeatureAnalyzer:
    # USAS 主类定义 (用于图表显示)
    USAS_MAP = {
        'A': 'General & Abstract (A)',
        'B': 'Body & Individual (B)',
        'C': 'Arts & Crafts (C)',
        'E': 'Emotion (E)',
        'F': 'Food & Farming (F)',
        'G': 'Govt & Public (G)',
        'H': 'Architecture (H)',
        'I': 'Money & Commerce (I)',
        'K': 'Entertainment (K)',
        'L': 'Life & Living (L)',
        'M': 'Movement/Trans (M)',
        'N': 'Numbers (N)',
        'O': 'Substances (O)',
        'P': 'Education (P)',
        'Q': 'Linguistic (Q)',
        'S': 'Social (S)',
        'T': 'Time (T)',
        'W': 'World & Env (W)',
        'X': 'Psychological (X)',
        'Y': 'Science & Tech (Y)',
        'Z': 'Grammatical (Z)'
    }

    def __init__(self, jsonl_path):
        self.file_path = jsonl_path
        # 数据结构: stats[version][category_char] = count
        self.stats = defaultdict(Counter)
        self.totals = defaultdict(int)
        self.versions = set()

    def load_and_count(self):
        """扫描文件并统计主类频次"""
        print(f"正在统计语义主类分布: {self.file_path} ...")
        
        with open(self.file_path, 'r', encoding='utf-8') as f:
            for line in tqdm(f, desc="Scanning Semantics"):
                try:
                    record = json.loads(line)
                    annotations = record.get('annotations', {})
                    
                    # 1. 统计 Source (中文)
                    if annotations.get('source_zh'):
                        self._process_version('source', annotations['source_zh'])
                    
                    # 2. 统计 Targets (英文)
                    targets = annotations.get('targets_en', {})
                    for ver, data in targets.items():
                        if data: # 排除 null
                            self._process_version(ver, data)
                            
                except Exception:
                    continue
        
        print("统计完成！版本:", list(self.versions))

    def _process_version(self, version, data):
        """处理单个版本的数据"""
        self.versions.add(version)
        tags_list = data.get('usas_tags', [])
        
        for item in tags_list:
            tag_code = item.get('tag', '')
            if not tag_code: continue
            
            # === 核心逻辑：只取首字母作为主类 ===
            # 例如 "E4.1" -> "E"
            major_cat = tag_code[0].upper()
            
            # 过滤掉非字母的异常标签 (如果有)
            if major_cat.isalpha():
                self.stats[version][major_cat] += 1
                self.totals[version] += 1

    def get_distribution_df(self, target_categories=None, versions=None):
        """
        生成统计报表
        :param target_categories: list, 用户想看的主类列表 (如 ['A', 'E', 'Z'])。为 None 则返回所有。
        :param versions: list, 指定版本
        """
        if versions is None:
            # 默认不显示 source，只对比译本
            versions = [v for v in self.versions if v != 'source']
            
        rows = []
        for ver in versions:
            total_count = self.totals[ver]
            if total_count == 0: continue
            
            # 如果用户没指定类别，就统计所有出现过的类别
            cats_to_scan = target_categories if target_categories else self.stats[ver].keys()
            
            for cat in cats_to_scan:
                count = self.stats[ver][cat]
                percentage = (count / total_count) * 100
                
                # 获取可读名称
                readable_name = self.USAS_MAP.get(cat, cat)
                
                rows.append({
                    "Version": ver,
                    "Category Code": cat,
                    "Category Name": readable_name,
                    "Count": count,
                    "Percentage": percentage
                })
                
        # 排序：按 Category Code 字母顺序
        df = pd.DataFrame(rows)
        if not df.empty:
            df = df.sort_values(by="Category Code")
            
        return df
# bfsujason@163.com

import json
import logging
from tqdm import tqdm
from collections import defaultdict
from src.llm_client import LLMClient
from src.prompt import mt_generation_prompt

# 配置日志
logger = logging.getLogger(__name__)

class MTGenerator:
    def __init__(
        self,
        src_lang="Chinese",
        tgt_lang="English",
        model=None,
    ):
        """
        初始化翻译引擎
        
        :param src_lang: 原文语种
        :param tgt_lang: 译文语种
        :param model: 模型名称
            若为 None，使用默认模型 qwen-flash
        """
        logger.info("加载翻译引擎...")
        
        self.llm = LLMClient(model=model)
        self.model = self.llm.default_model
        
        self.src_lang = src_lang
        self.tgt_lang = tgt_lang
        
        logger.info(f"翻译引擎就绪！原文语种：{src_lang} 译文语种：{tgt_lang}")

    def translate(self, text):
        """
        调用大模型翻译文本
        
        :param text: 待翻译文本
        :return: JSON Object
        """
        user_template = mt_generation_prompt.PROMPT
        prompt = user_template.format(
            src_lang=self.src_lang,
            tgt_lang=self.tgt_lang,
            text=text,
        )
        
        try:
            return self.llm.get_json_response(
                prompt=prompt, 
            )
        except Exception as e:
            logger.error(f"翻译引擎错误：{e}")
            return None

# === 核心函数：translate_data ===
# 调用大模型 API 批量翻译原文

# 参数 data：DataFrame 格式的数据
# 参数 models：大模型 API 接口
def translate_data(data, models):
    results = []

    # 逐行遍历所有数据
    for index, row in tqdm(data.iterrows(), total=len(data), desc="Translating"):

        # 提取汉语原文和人类译文
        src_text = row["source"]
        human_trans = row["target"]

        # 初始化 record 字典
        record = defaultdict(lambda: defaultdict(dict))

        record["id"] = f"{index:06d}"
        record["source"]["raw_text"] = src_text
        record["targets"]["human"]["raw_text"] = human_trans
        
        # 调用大模型 API 翻译原文
        try:
            # 按所选模型
            # 依次生成不同版本的机器译文
            for model in models.keys():
                model_trans = models[model].translate(src_text)
                record["targets"][model]["raw_text"] = model_trans['target_text']
            # 将翻译结果保存于 results 列表
            results.append(record)
        except Exception as e:
            print(f"Error at index {index}: {e}")
            continue
                
    return results

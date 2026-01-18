# bfsujason@163.com
# python -m src.annotator.semantic_annotation

import json
import logging

from src.config import Config
from src.utils import load_usas_tags
from src.llm_client import LLMClient
from src.prompt import usas_prompt_en, usas_prompt_zh

# 配置日志
logger = logging.getLogger(__name__)

class SemanticAnnotator:
    def __init__(self, lang, model=None):
        """
        初始化语义标注器
        :param lang: 待标注文本语种
        :param model: 指定模型名称
                      若为 None，使用默认模型 qwen-flash
        """
        logger.info("初始化标注引擎...")
        
        self.llm = LLMClient(model=model)
        self.model = self.llm.default_model
        
        logger.info(f"引擎就绪：{self.model}")
        
        # 根据语种选择标签集
        self.lang = lang
        
        logger.info("Loading USAS tagsets...")
        if lang == "English":
            sem_tag_path = Config.EN_SEMTAG_PATH
        elif lang == "Chinese":
            sem_tag_path = Config.ZH_SEMTAG_PATH
            
        try:
            self.tags_str = load_usas_tags(sem_tag_path)
        except FileNotFoundError as e:
            logger.error(f"Tag file not found: {e}")
            raise
            
        # 根据语种选择提示词模板
        logger.info("Loading USAS prompt ...")
        if lang == 'Chinese':
            # 使用中文模块
            #sys_template = usas_prompt_zh.SYSTEM_PROMPT
            self.user_template = usas_prompt_zh.PROMPT
        elif lang == 'English':
            # 使用英文模版
            #sys_template = usas_prompt_zh.SYSTEM_PROMPT
            self.user_template = usas_prompt_en.PROMPT
        else:
            raise ValueError("Unsupported language. Use 'zh' or 'en'.")

    def annotate(self, text):
        """
        执行标注
        :param text: 待标注文本
        :return: JSON List
        """
        if not text:
            return []
            
        # 构造 Prompt
        final_prompt = self.user_template.format(
            tag_list=self.tags_str,
            text=text,
        )
        
        # 调用大模型
        try:
            return self.llm.get_json_response(
                prompt=final_prompt, 
            )
        except Exception as e:
            logging.error(f"Semantic tagging error: {e}")
            return ()

# === 简单的测试入口 ===
if __name__ == "__main__":
    
    # 打印日志信息
    logging.basicConfig(level=logging.INFO)
    
    # 测试英文语义标注
    lang = 'English'
    model = 'glm-4.7'
    annotator = SemanticAnnotator(lang=lang, model=model)
    result = annotator.annotate("This is a test.")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # 测试中文语义标注
    lang = 'Chinese'
    annotator = SemanticAnnotator(lang=lang, model=model)
    result = annotator.annotate("这是一个测试。")
    print(json.dumps(result, indent=2, ensure_ascii=False))

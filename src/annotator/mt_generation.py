# bfsujason@163.com
# python -m src.annotator.mt_generation

import json
import logging
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
            
# === 单元测试 ===
if __name__ == "__main__":

    # 打印日志信息
    logging.basicConfig(level=logging.INFO)
    
    # 初始化翻译模型
    src_lang = "Chinese"
    tgt_lang = "English"
    model = "qwen-plus" 
    translator = MTGenerator(
        src_lang=src_lang,
        tgt_lang=tgt_lang,
        model=model,
    )
    
    # 输入原文
    src_text = "女婴啼哭不休。她母亲温言相呵，女婴只是大哭。"
    print(f"\n[原文]：{src_text}\n")
    
    # 调用大模型生成译文
    result = translator.translate(src_text)
    
    # 输出翻译结果
    if result:
        print("测试成功！模型返回译文：")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("测试失败，请查看日志信息调试程序")

# bfsujason@163.com
# python -m src.config

import os
from dotenv import load_dotenv

# 加载根目录下的 .env 配置文件
load_dotenv()

class Config:
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # === 大模型设置 ===
    
    # 阿里云百炼大模型：https://bailian.console.aliyun.com/
    LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
    LLM_API_KEY = os.getenv("LLM_API_KEY", "EMPTY")
    LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "qwen-flash")
    
    # 缓存目录设置
    _LLM_CACHE_DIR = os.getenv("LLM_CACHE_DIR", "data/llm_cache")
    LLM_CACHE_DIR = os.path.join(PROJECT_ROOT, _LLM_CACHE_DIR)
    
    # === 语义标注设置 ===
    
    # 英文语义标签
    _EN_SEMTAG_PATH = os.getenv("EN_SEMTAG_PATH", "data/res/en_semtag.txt")
    EN_SEMTAG_PATH = os.path.join(PROJECT_ROOT, _EN_SEMTAG_PATH)
    
    # 中文语义标签
    _ZH_SEMTAG_PATH = os.getenv("ZH_SEMTAG_PATH", "data/res/zh_semtag.txt")
    ZH_SEMTAG_PATH = os.path.join(PROJECT_ROOT, _ZH_SEMTAG_PATH)
      
# === 单元测试 ===
if __name__ == "__main__":

    print("\n=== 大模型设置 ===\n")
    print(f"Base URL:    {Config.LLM_BASE_URL}")
    print(f"API Key:     {Config.LLM_API_KEY[:5]}******")
    print(f"Model Name:  {Config.LLM_MODEL_NAME}")
    print(f"Cache Dir:   {Config.LLM_CACHE_DIR.replace('\\', '/')}")
    
    print("\n=== 语义标注设置 ===\n")
    print(f"EN Semtag:   {Config.EN_SEMTAG_PATH.replace('\\', '/')}")
    print(f"ZH Semtag:   {Config.ZH_SEMTAG_PATH.replace('\\', '/')}")

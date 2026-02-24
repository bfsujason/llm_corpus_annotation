# bfsujason@163.com
# python -m src.config

import os
from dotenv import load_dotenv

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 加载根目录下的 config 配置文件
load_dotenv(os.path.join(PROJECT_ROOT, 'config'))

class Config:
    # === 大模型设置 ===
    
    # 阿里云百炼大模型：https://bailian.console.aliyun.com/
    LLM_BASE_URL = os.getenv('LLM_BASE_URL', 'https://dashscope.aliyuncs.com/compatible-mode/v1')
    LLM_API_KEY = os.getenv('LLM_API_KEY', 'EMPTY')
    LLM_MODEL_NAME = os.getenv('LLM_MODEL_NAME', 'kimi-k2.5')
    
    # 缓存目录设置
    _LLM_CACHE_DIR = os.getenv('LLM_CACHE_DIR', 'data/llm_cache')
    LLM_CACHE_DIR = os.path.join(PROJECT_ROOT, _LLM_CACHE_DIR)
      
# === 单元测试 ===
if __name__ == '__main__':

    print('\n=== 大模型设置 ===\n')
    print(f'Base URL:    {Config.LLM_BASE_URL}')
    print(f'API Key:     {Config.LLM_API_KEY[:5]}******')
    print(f'Model Name:  {Config.LLM_MODEL_NAME}')
    cache_dir = Config.LLM_CACHE_DIR.replace("\\", "/")
    print(f'Cache Dir:   {cache_dir}')

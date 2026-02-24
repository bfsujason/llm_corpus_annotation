# bfsujason@163.com
# python -m src.llm_client

import re
import json
import logging

import openai
import diskcache

from src.config import Config

# 配置日志
logger = logging.getLogger(__name__)

class LLMClient:
    """
    实时调用大模型 API (非 Batch 模式)
    """

    def __init__(self,
        model=None,
        temperature=0.1,
        enable_thinking=False,
    ):
        """
        初始化客户端
        从 Config 中读取 API_KEY, BASE_URL 和 CACHE_DIR
        
        :param model: 模型名称 (默认为 kimi-k2.5)
        :param temperature: 采样温度系数 (默认为 0.1)
        :param enable_thinking: 思考模式 (默认为关闭)
        """
        logger.info('初始化大模型客户端 ...')
        
        self.client = openai.OpenAI(
            api_key=Config.LLM_API_KEY,
            base_url=Config.LLM_BASE_URL,
        )

        self.default_model = model or Config.LLM_MODEL_NAME
        self.temperature = temperature
        self.enable_thinking = enable_thinking
        self.cache = diskcache.Cache(Config.LLM_CACHE_DIR)
        #self.cache_new = diskcache.Cache('C:/llm_annotation_v9/data/llm_cache_new')
        
        # 验证配置
        logger.info(f'初始化完毕！Base URL：{Config.LLM_BASE_URL} Model：{self.default_model}')

    def get_response(
        self,
        prompt,
        system_prompt=None,
        model=None,
        temperature=0.1,
        #top_p=0.8,
        max_tokens=4096,
        stream=True,
        enable_thinking=False,
        thinking_budget=4096,
        json_output=False,
    ):
        """
        发送请求并获取生成内容
        
        :param prompt: 用户 Prompt (User Message)
        :param system_prompt: 系统 Prompt (System Message)
        :param model: 大模型名称
        :param temperature: 采样温度系数
        :param max_tokens: 最大输出长度
        :param stream: 流式输出 (用于思考类模型)
        :enable_thinking: 思考模式
        :thinking_budget: 思考过程的最大程度
        :json_output: JSON 格式输出
        :return: 解析后的 Python 字典或列表 (JSON 模式)
                 字符串 (非 JSON 模式)
                 如果失败则返回 None
        """
        model = self.default_model
        temperature = self.temperature
        enable_thinking = self.enable_thinking
        
        # 构建消息
        messages = []
        if system_prompt:
            messages.append({'role': 'system', 'content': system_prompt})
        messages.append({'role': 'user', 'content': prompt})
        
        # 读取缓存
        cache_key = '|||'.join([message['content'] for message in messages])
        cache_key = model + '|||' + cache_key
        
        if enable_thinking:
            cache_key = 'THINK'+ '|||' + cache_key
        
        if cache_key in self.cache:
            logger.info('Found in cache!')
            #self.cache_new[cache_key] = self.cache[cache_key]
            return self.cache[cache_key]
        
        # 设置参数
        request_kwargs = {
            'model': model,
            'messages': messages,
            'temperature': temperature,
            'max_tokens': max_tokens,
            'stream': stream,
            'extra_body': {
                'enable_thinking': enable_thinking,
                'thinking_budget': thinking_budget,
            },
        }
        
        # 强制输出 JSON 格式
        # 注意：deepseek-v3.2 和 kimi-k2.5 不支持此参数
        if json_output:
            if model.startswith(('qwen', 'glm')):
                request_kwargs['response_format'] = {'type': 'json_object'}

        try:
            # 调用 API
            response = self.client.chat.completions.create(**request_kwargs)

            # 获取生成内容
            content = ''
            for chunk in response:
                delta = chunk.choices[0].delta
                # 收到content，开始进行回复
                if hasattr(delta, 'content') and delta.content:
                    content += delta.content
            result = content.strip()
            
            # 解析 JSON
            if json_output:
                result = self._parse_json(content)
            
            # 写入缓存
            self.cache[cache_key] = result
            
            return result

        except openai.APIError as e:
            logger.error(f'LLM API 错误: {e}')
            return None
            
        except Exception as e:
            logger.error(f'LLM 调用错误: {e}')
            return None
        
    def _parse_json(self, content):
        """
        解析大模型生成内容 (JSON 格式)
        
        :param content: JSON 字符串
        :return: Python 字典或列表
        """
        if not content:
            return None
            
        try:
            # 尝试直接解析
            return json.loads(content)
        except json.JSONDecodeError:
            # 如果失败，尝试去除 Markdown 代码块标记
            # 匹配 ```json ... ``` 或 ``` ... ``` 中的内容
            pattern = r'```(?:json)?\s*(.*?)\s*```'
            match = re.search(pattern, content, re.DOTALL)
            
            if match:
                clean_content = match.group(1)
                try:
                    return json.loads(clean_content)
                except json.JSONDecodeError:
                    pass # 继续尝试其他解析方式
            
            logger.warning(f'JSON 解析失败：{content[:100]}...')
            return None

if __name__ == '__main__':

    # 打印日志信息
    logging.basicConfig(level=logging.INFO)
    
    # 初始化模型
    #model = 'deepseek-v3.2'
    model = 'kimi-k2.5'
    temperature = 0.1
    enable_thinking = False
    client = LLMClient(
        model=model,
        temperature=temperature,
        enable_thinking=enable_thinking,
    )
    
    # === 测试普通输出 ===
    
    print(f'\n测试 1: 普通输出')
    print(f'{"=" * 30}')
    
    # 编写提示词
    user_p = """You are a professional corpus linguist specialized in multilingual tokenization.

Your task is to tokenize the given text for downstream NLP tasks including POS tagging, dependency parsing, and semantic tagging.

Text: 陈清扬把我拽住，以伟大友谊的名义叫我留下来。
"""
    result = client.get_response(prompt=user_p, json_output=False)
    
    # 输出生成内容
    if result:
        print('测试成功！模型返回结果：')
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print('测试失败，请查看日志信息调试程序')
        
    # === 测试结构化输出 ===
    
    print(f'\n测试 2: 结构化输出')
    print(f'{"=" * 30}')
    
    # 编写提示词
    user_p = """You are a professional corpus linguist specialized in multilingual tokenization.

Your task is to tokenize the given text for downstream NLP tasks including POS tagging, dependency parsing, and semantic tagging.
    
Return result in JSON format with the tokens as a flat and ordered list.

Text: 陈清扬把我拽住，以伟大友谊的名义叫我留下来。
"""
    result = client.get_response(prompt=user_p, json_output=True)
    
    # 输出生成内容
    if result:
        print('测试成功！模型返回结果：')
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print('测试失败，请查看日志信息调试程序')
 
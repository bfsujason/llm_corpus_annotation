# bfsujason@163.com
# python -m src.llm_client

import os
import re
import json
import openai
import logging
import diskcache
from src.config import Config

# 配置日志
logger = logging.getLogger(__name__)

class LLMClient:
    """
    实时调用大模型 API (非 Batch 模式)
    """

    def __init__(self, model=None):
        """
        初始化客户端
        从 Config 中读取 API_KEY, BASE_URL 和 CACHE_DIR
        
        :param model: 模型名称 (默认为 qwen-plus)
        """
        logger.info("初始化大模型客户端 ...")
        
        self.client = openai.OpenAI(
            api_key=Config.LLM_API_KEY,
            base_url=Config.LLM_BASE_URL,
        )
        self.default_model = model or Config.LLM_MODEL_NAME
        self.cache = diskcache.Cache(Config.LLM_CACHE_DIR)
        
        # 验证配置
        logger.info(f"初始化完毕！Base URL：{Config.LLM_BASE_URL} Model：{self.default_model}")
        
    def get_text_response(
        self,
        prompt,
        system_prompt=None,
        json_output=True,
        temperature=0.1,
        #top_p=0.8,
        max_tokens=4096,
        stream=False,
        enable_thinking=False,
        thinking_budget=200,
    ):
        """
        发送请求并获取生成内容 (TEXT 格式)
        注意：暂不支持流式输出和思考模式
        
        :param prompt: 用户 Prompt (User Message)
        :param system_prompt: 系统 Prompt (System Message)
        :param temperature: 采样温度系数
        :param max_tokens: 最大输出长度
        :param stream: 流式输出 (用于思考类模型)
        :enable_thinking: 思考模式
        :thinking_budget: 思考过程的最大程度
        :return: 字符串；如果失败则返回 None
        """
        target_model = self.default_model
        
        # 构建消息
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        # 读取缓存
        cache_key = '|||'.join([message['content'] for message in messages])
        cache_key = target_model + '|||' + cache_key
        
        if cache_key in self.cache:
            logger.info('Found in cache!')
            return self.cache[cache_key]
        
        # 设置参数
        request_kwargs = {
            "model": target_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream,
            "extra_body": {
                "enable_thinking": enable_thinking,
                "thinking_budget": thinking_budget,
            },
        }

        try:
            # 调用 API
            response = self.client.chat.completions.create(**request_kwargs)

            # 获取生成内容
            content = response.choices[0].message.content
            result = content.strip()
            # 写入缓存
            self.cache[cache_key] = result
            
            return result
            
        except openai.APIError as e:
            logger.error(f"LLM API 错误: {e}")
            return None
            
        except Exception as e:
            logger.error(f"LLM 调用错误: {e}")
            return None

    def get_json_response(
        self,
        prompt,
        system_prompt=None,
        temperature=0.1,
        #top_p=0.8,
        max_tokens=4096,
        stream=False,
        enable_thinking=False,
        thinking_budget=200,
    ):
        """
        发送请求并获取生成内容 (JSON 格式)
        注意：暂不支持流式输出和思考模式
        
        :param prompt: 用户 Prompt (User Message)
        :param system_prompt: 系统 Prompt (System Message)
        :param temperature: 采样温度系数
        :param max_tokens: 最大输出长度
        :param stream: 流式输出 (用于思考类模型)
        :enable_thinking: 思考模式
        :thinking_budget: 思考过程的最大程度
        :return: 解析后的 Python 字典或列表；如果失败则返回 None
        """
        target_model = self.default_model
        
        # 构建消息
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        # 读取缓存
        cache_key = '|||'.join([message['content'] for message in messages])
        cache_key = target_model + '|||' + cache_key
        
        if cache_key in self.cache:
            logger.info('Found in cache!')
            return self.cache[cache_key]
        
        # 设置参数
        request_kwargs = {
            "model": target_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream,
            "extra_body": {
                "enable_thinking": enable_thinking,
                "thinking_budget": thinking_budget,
            },
        }
        
        # 强制输出 JSON 格式
        # 注意：DeepSeek 不支持此参数
        if target_model.startswith(("qwen", "glm")):
            request_kwargs["response_format"] = {"type": "json_object"}

        try:
            # 调用 API
            response = self.client.chat.completions.create(**request_kwargs)

            # 获取生成内容
            content = response.choices[0].message.content
            #print(content)
            
            # 解析 JSON
            result = self._parse_json(content)
            
            # 写入缓存
            self.cache[cache_key] = result
            
            return self._parse_json(content)
            
        except openai.APIError as e:
            logger.error(f"LLM API 错误: {e}")
            return None
            
        except Exception as e:
            logger.error(f"LLM 调用错误: {e}")
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
            pattern = r"```(?:json)?\s*(.*?)\s*```"
            match = re.search(pattern, content, re.DOTALL)
            
            if match:
                clean_content = match.group(1)
                try:
                    return json.loads(clean_content)
                except json.JSONDecodeError:
                    pass # 继续尝试其他解析方式
            
            logger.warning(f"JSON 解析失败：{content[:100]}...")
            return None

# === 单元测试 ===
if __name__ == "__main__":

    # 打印日志信息
    logging.basicConfig(level=logging.INFO)
    
    # 初始化模型
    model = "qwen-plus"
    client = LLMClient(model)
    

    # 调用模型 API
    user_p = """You are an expert translator. Translate the following Chinese into English:
    Chinese: 江南近海滨的一条大路上，一队清兵手执刀枪，押着七辆囚车，冲风冒寒，向北而行。
    
    Output your translation in JSON format with a 'target_text' key.
    """
    result = client.get_json_response(prompt=user_p)
    
    # 输出生成内容
    if result:
        print("测试成功！模型返回结果：")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("测试失败，请查看日志信息调试程序")
    
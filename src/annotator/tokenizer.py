# bfsujason@163.com
# python -m src.annotator.tokenizer

import json
import logging
from collections import defaultdict

from tqdm import tqdm

from src.utils import clean_text, split_sents

# 配置日志
logger = logging.getLogger(__name__)

class Tokenizer:
    def __init__(self,
        lang,
        mode='local',
        llm_model=None,
        enable_thinking=False,
    ):
        """
        :param lang:            语种 str
                                [chinese]:  中文
                                [english]:  英文
        :param mode:            标注模式 str
                                [local]:    本地预训练模型
                                [llm]:      大模型 API
        :param llm_model:       大模型名称 str | None
                                [kimi-k2.5]:      Kimi-k2.5
                                https://bailian.console.aliyun.com/console?tab=api#/api/?type=model&url=2948482
                                [deepseek-v3.2]:  DeepSeek V3.2
                                https://bailian.console.aliyun.com/console?tab=api#/api/?type=model&url=2868565
                                [glm-4.7]:        GLM-4.7
                                https://bailian.console.aliyun.com/console?tab=api#/api/?type=model&url=2974045
                                [qwen3-max]:      Qwen3-Max
                                https://bailian.console.aliyun.com/console?tab=api#/api/?type=model&url=3016807
                                [None]:           DeepSeek V3.2
        :param enable_thinking: 思考模式 | Boolean
                                [True]:     开启
                                [False]:    关闭                        
        :return:                Tokenizer Pipeline 实例
        """
        
        # 参数校验
        SUPPORTED = {'chinese', 'english'}
        
        if lang not in SUPPORTED:
            raise ValueError(
                f'暂不支持 {lang}\n'
                f'支持语种: {list(SUPPORTED)}'
            )
            
        self.lang = lang
        self.mode = mode
        
        if mode == 'local':
            import hanlp
            if lang == 'chinese':
                # === 加载中文分词模型 ===
                # FINE_ELECTRA_SMALL_ZH
                # 模型介绍：https://hanlp.hankcs.com/docs/api/hanlp/pretrained/tok.html
                # 下载地址：https://file.hankcs.com/hanlp/tok/fine_electra_small_20220615_231803.zip
                # 使用方法：https://github.com/hankcs/HanLP/blob/doc-zh/plugins/hanlp_demo/hanlp_demo/zh/tok_stl.ipynb
                logger.info('加载 HanLP 中文分词模型 ...')
                tokenizer = hanlp.load(hanlp.pretrained.tok.FINE_ELECTRA_SMALL_ZH)
                self.pipeline = hanlp.pipeline() \
                    .append(tokenizer, input_key='sent', output_key='tok')
                logger.info('HanLP 中文分词模型加载完毕！')
            elif lang == 'english':
                # === 加载英文分词模型 ===
                # 使用方法：https://github.com/hankcs/HanLP/blob/doc-zh/plugins/hanlp_demo/hanlp_demo/en/demo_tok.py
                
                from hanlp.utils.lang.en.english_tokenizer import tokenize_english
                
                logger.info('加载 HanLP 英文分词模型 ...')
                tokenizer = tokenize_english
                self.pipeline = hanlp.pipeline() \
                    .append(tokenizer, input_key='sent', output_key='tok')
                logger.info('HanLP 英文分词模型加载完毕！')
        elif mode == 'llm':
            from src.llm_client import LLMClient
            from src.prompt import tok_prompt
            
            logger.info('加载 LLM 分词模型 ...')
            self.pipeline = LLMClient(model=llm_model, enable_thinking=enable_thinking)
            self.llm_model = self.pipeline.default_model
            self.prompt = tok_prompt
            logger.info('LLM 分词模型加载完毕！')
       
    def tokenize(self, text):
        """
        :param text:    输入文本 str | dict
        :return:        标注结果 dict
                        [text]:  输入文本 str
                        [sent]:  分句结果 [list]
                        [tok]:   分词结果 [list[list]]
        """
        if self.mode == 'llm':
            return self._llm_tok(text)
        elif self.mode == 'local':
            return self._local_tok(text)
            
    def _llm_tok(self, text):
        if self.lang == 'english':
            prompt_name = f'EN_TOK_PROMPT'
        elif self.lang == 'chinese':
            prompt_name = f'ZH_TOK_PROMPT'
        
        prompt_tmpl = getattr(self.prompt, prompt_name)
        
        result = defaultdict(list)
        text = clean_text(text)
        sents = split_sents(text, lang=self.lang)
        result['text'] = text
        result['sent'] = sents['sent']
        
        for sent in sents['sent']:
            # 构造 Prompt
            prompt = prompt_tmpl.format(
                text=json.dumps(sent, ensure_ascii=False),
            )
            
            # 调用大模型
            try:
                response = self.pipeline.get_response(
                    prompt=prompt,
                    json_output=True,
                )
                
                tokens = self._convert_llm_response(response)
                result['tok'].append(tokens)
                
            except Exception as e:
                logging.error(f'LLM tokenizing error: {e}')
                    
        return result
        
    def _local_tok(self, text):
        result = {}
        text = clean_text(text)
        sents = split_sents(text, lang=self.lang)
        doc = self.pipeline(sents)
        result['text'] = text
        result['sent'] = sents['sent']
        result['tok'] = doc['tok']
        return result
        
    @staticmethod
    def _convert_llm_response(response):
        tokens = response
        return tokens
        
def annotate_data(data, annotator):
    annos = []
    
    # 逐行遍历所有数据
    for index, text in tqdm(data.items(), total=len(data), desc="Tokenizing"):
        try:
            record = defaultdict(list)
            record['id'] = f'{index:05d}'
            
            # 标注文本
            anno = annotator.tokenize(text)
        
            # 提取标注结果
            record['text'] = anno['text']
            record['sent'] = anno['sent']
            record['tok'] = anno['tok']
            annos.append(record)
        except Exception as e:
            print(f'Error at index {index}: {e}')
            continue
            
    return annos
    
def display_anno(anno):
    print(f'\n[ID]: {anno["id"]}')
    print(f'{anno["text"]}')
    print(f'{'-' * 80}')
    tags = [tok for sent_tok in anno['tok'] for tok in sent_tok]
    print(tags)
    print(f'{'=' * 80}')
    
def compare_annos(
    annos_1,
    annos_2,
    annos_1_name,
    annos_2_name,
    show_diff=True,
):
    intersections, unions = 0, 0
    for anno_1, anno_2 in zip(annos_1, annos_2):
        print(f'\n[ID]: {anno_1["id"]}')
        print(f'{anno_1["text"]}')
        print(f'{"-" * 80}')
        
        anno_1_tok = anno_1['tok']
        anno_1_tags = [tok for sent_tok in anno_1_tok for tok in sent_tok]
        
        anno_2_tok = anno_2['tok']
        anno_2_tags = [tok for sent_tok in anno_2_tok  for tok in sent_tok]
        
        set_1 = set(anno_1_tags)
        set_2 = set(anno_2_tags)
        
        intersection = set_1 & set_2
        union = set_1 | set_2
        jac = len(intersection) / len(union)
        print(f'Jaccard: {jac:.3f}')
        
        intersections += len(intersection)
        unions += len(union)
        
        if show_diff:
            only_in_1 = set_1 - set_2
            only_in_2 = set_2 - set_1
            print(f"{annos_1_name}: {only_in_1}")
            print(f"{annos_2_name}: {only_in_2}")
            
        print(f'{"=" * 80}')
        
    macro_jac = intersections / unions
    print(f'Macro Jaccard: {macro_jac:.3f}')
   
if __name__ == '__main__':

    # 打印日志信息
    logging.basicConfig(level=logging.INFO)
    
    llm_model = 'deepseek-v3.2'
    enable_thinking=False
    
    # === 测试中文 ===
    
    lang = 'chinese'
    zh_text = '那天晚上我没走掉。 陈清扬把我拽住，以伟大友谊的名义叫我留下来。'
    
    print(f'\n[中文文本]：{zh_text}')
    print(f'{"=" * 30}')
    
    print(f'\n测试 1: HanLP 中文分词')
    print(f'{"=" * 30}')
    zh_tokenizer = Tokenizer(lang=lang, mode='local')
    zh_doc = zh_tokenizer.tokenize(zh_text)
    print(f'[分词结果]:{zh_doc}')
    
    print(f'\n测试 2: LLM 中文分词')
    print(f'{"=" * 30}')
    zh_tokenizer = Tokenizer(
        lang=lang,
        mode='llm',
        llm_model=llm_model,
        enable_thinking=enable_thinking,
    )
    zh_doc = zh_tokenizer.tokenize(zh_text)
    print(f'[分词结果]:{zh_doc}')
    
    # === 测试英文 ===
    
    lang = 'english'
    en_text = "Chen Qingyang caught me and asked me to stay in the name of our great friendship."
    print(f'\n[英文文本]：{en_text}')
    print(f'{"=" * 30}')
    
    print('\n测试 3: HanLP 英文分词')
    print(f'{"=" * 30}')  
    en_tokenizer = Tokenizer(lang=lang, mode='local')
    en_doc = en_tokenizer.tokenize(en_text)
    print(f'[分词结果]{en_doc}')
    
    print('\n测试 4: LLM 英文分词')
    print(f'{"=" * 30}')  
    en_tokenizer = Tokenizer(
        lang=lang,
        mode='llm',
        llm_model=llm_model,
        enable_thinking=enable_thinking,
    )
    en_doc = en_tokenizer.tokenize(en_text)
    print(f'[分词结果]{en_doc}')

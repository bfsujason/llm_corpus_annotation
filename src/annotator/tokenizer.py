# bfsujason@163.com
# python -m src.annotator.tokenizer

import logging

import hanlp
from hanlp.utils.rules import split_sentence

# 配置日志
logger = logging.getLogger(__name__)

class Tokenizer:
    def __init__(self, lang, device=None):
        """
        :param lang:    语种 str
                        [chinese]:  中文
                        [english]:  英文
        :param device:  设备 int | None
                        [-1]:       CPU
                        [0]:        GPU
                        [None]:     自动选择  
        :return:        HanLP Pipeline 实例: hanlp.components.pipeline
                        https://hanlp.hankcs.com/docs/api/hanlp/components/pipeline.html
                        https://github.com/hankcs/HanLP/blob/doc-zh/plugins/hanlp_demo/hanlp_demo/zh/demo_pipeline.py
                        https://github.com/hankcs/HanLP/blob/doc-zh/plugins/hanlp_demo/hanlp_demo/en/demo_pipeline.py
        """
        # 参数校验
        SUPPORTED = {'chinese', 'english'}
        
        if lang not in SUPPORTED:
            raise ValueError(
                f'暂不支持 {lang}\n'
                f'支持语种: {list(SUPPORTED)}'
            )
            
        self.lang = lang
        
        if lang == 'chinese':
            # === 加载中文分词模型 ===
            # FINE_ELECTRA_SMALL_ZH
            # 模型介绍：https://hanlp.hankcs.com/docs/api/hanlp/pretrained/tok.html
            # 下载地址：https://file.hankcs.com/hanlp/tok/fine_electra_small_20220615_231803.zip
            # 使用方法：https://github.com/hankcs/HanLP/blob/doc-zh/plugins/hanlp_demo/hanlp_demo/zh/tok_stl.ipynb
            logger.info('加载 HanLP 中文分词模型 ...')
            tokenizer = hanlp.load(hanlp.pretrained.tok.FINE_ELECTRA_SMALL_ZH, devices=device)
            self.pipeline = hanlp.pipeline() \
                .append(split_sentence, output_key='sent') \
                .append(tokenizer, output_key='tok')
            logger.info('HanLP 中文分词模型加载完毕！')
        elif lang == 'english':
            # === 加载英文分词模型 ===
            # 使用方法：https://github.com/hankcs/HanLP/blob/doc-zh/plugins/hanlp_demo/hanlp_demo/en/demo_tok.py
            
            from hanlp.utils.lang.en.english_tokenizer import tokenize_english
            
            logger.info('加载 HanLP 英文分词模型 ...')
            tokenizer = tokenize_english
            self.pipeline = hanlp.pipeline() \
                .append(split_sentence, output_key='sent') \
                .append(tokenizer, output_key='tok')
            logger.info('HanLP 英文分词模型加载完毕！')
       
    def tokenize(self, text):
        """
        :param text:    输入文本 str | dict
        :return:        标注结果 dict
                        [sent]:  分句结果 [list]
                        [tok]:   分词结果 [list[list]]
        """
        result = {}
        if isinstance(text, str):
            doc = self.pipeline(text)   
            result['sent'] = doc['sent']
            result['tok'] = doc['tok']
        elif isinstance(text, dict):
            result = text
        return result
        
if __name__ == '__main__':

    # 打印日志信息
    logging.basicConfig(level=logging.INFO)

    # === 测试中文 ===
    lang = 'chinese'
    zh_text = '那天晚上我没走掉。 陈清扬把我拽住，以伟大友谊的名义叫我留下来。'
    
    print(f'\n[中文文本]：{zh_text}')
    print(f'{"=" * 30}')
    
    print(f'\n测试 1: HanLP 中文分词')
    print(f'{"=" * 30}')
    zh_tokenizer = Tokenizer(lang=lang)
    zh_doc = zh_tokenizer.tokenize(zh_text)
    print(f'[分词结果]:{zh_doc}')
    
    # === 测试英文 ===
    lang = 'english'
    en_text = 'Chen Qingyang caught me and asked me to stay in the name of our great friendship.'
    print(f'\n[英文文本]：{en_text}')
    print(f'{"=" * 30}')
    
    print('\n测试 2: HanLP 英文分词')
    print(f'{"=" * 30}')  
    en_tokenizer = Tokenizer(lang=lang)
    en_doc = en_tokenizer.tokenize(en_text)
    print(f'[分词结果]{en_doc}')

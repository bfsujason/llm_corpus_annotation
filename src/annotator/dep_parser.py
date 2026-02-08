# bfsujason@163.com

# 单元测试：
# python -m src.annotator.dep_parser

import json
import logging
import pandas as pd
from tqdm import tqdm
from collections import defaultdict

import stanza
from src.annotator.tokenizer import Tokenizer

# 配置日志
logger = logging.getLogger(__name__)

class DEPParser:
    def __init__(
        self,
        lang,
        tagset='ud',
        mode='local',
        llm_model=None,
        device=None,
    ):
        """
        :param lang:        语种 str
                            [chinese]:  中文
                            [english]:  英文
        :param tagset:      标注集 str
                            [ud]:       通用依存关系标注集 2.0
                            https://universaldependencies.org/u/dep/
                            --- 英语 EWT 依存树库标注集 ---
                            https://universaldependencies.org/treebanks/en_ewt/index.html
                            --- 汉语 GSD 依存树库标注集 ---
                            https://universaldependencies.org/treebanks/zh_gsd/index.html
        :param mode:        标注模式 str
                            [local]:    本地预训练模型
                            [llm]:      大模型 API
        :param llm_model:   大模型名称 str | None
                            [deepseek-v3.2]:  DeepSeek V3.2
                            https://bailian.console.aliyun.com/console?tab=api#/api/?type=model&url=2868565
                            [glm-4.7]:        GLM-4.7
                            https://bailian.console.aliyun.com/console?tab=api#/api/?type=model&url=2974045
                            [qwen3-max]:      Qwen3-Max
                            https://bailian.console.aliyun.com/console?tab=api#/api/?type=model&url=3016807
                            [None]:           DeepSeek V3.2
        :param device:      设备 int | None
                            [-1]:     CPU
                            [0]:      GPU
                            [None]:   自动选择  
        :return:            DEPParser Pipeline 实例
        """
        
        # 参数校验
        SUPPORTED = {
            'chinese': {
                'local': {'ud'},
                'llm':   {'ud'},
            },
            'english': {
                'local': {'ud'},
                'llm':   {'ud'},
            },
        }
        
        if lang not in SUPPORTED:
            raise ValueError(
                f'暂不支持 {lang}\n'
                f'支持语种: {list(SUPPORTED.keys())}'
            )
            
        if tagset not in SUPPORTED[lang][mode]:
            raise ValueError(
                f'暂不支持 {mode} {lang}\n'
                f'支持标注集: {list(SUPPORTED[lang][mode])}'
            )
        
        self.lang = lang
        self.tagset = tagset
        self.mode = mode
        self.tokenizer = Tokenizer(lang=lang)
        
        if mode == 'local':
            if lang == 'chinese':
                # === 加载中文句法标注模型 ===
                # gsdsimp_charlm 
                # 模型介绍: https://stanfordnlp.github.io/stanza/depparse.html
                # 下载地址：https://huggingface.co/stanfordnlp/stanza-zh-hans/tree/main/models/depparse

                logger.info('加载 Stanza 中文句法标注模型 ...')
                self.pipeline = stanza.Pipeline('zh', processors='tokenize,pos,lemma,depparse', tokenize_pretokenized=True, download_method=None)
                logger.info('Stanza 中文句法标注模型加载完毕！')
            elif lang == 'english':
                # === 加载英文句法标注模型 ===
                # combined_charlm
                # 模型介绍：https://stanfordnlp.github.io/stanza/depparse.html
                # 下载地址：https://huggingface.co/stanfordnlp/stanza-en/tree/main/models/depparse
                
                logger.info('加载 Stanza 英文句法标注模型 ...')
                self.pipeline = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse', tokenize_pretokenized=True, download_method=None)
                logger.info('Stanza 英文句法标注模型加载完毕！')
            
        elif mode == 'llm':
            from src.llm_client import LLMClient
            from src.prompt import dep_parse_prompt
            
            logger.info('加载 LLM 句法标注模型 ...')
            self.pipeline = LLMClient(model=llm_model)
            self.llm_model = self.pipeline.default_model
            self.prompt = dep_parse_prompt
            logger.info(f'LLM 句法标注模型加载完毕！')
    
    # A wrapper for _local_tag() and _llm_tag()
    def tag(self, text):
        """
        :param text:    输入文本 str 
        :return:        标注结果 dict
                        [sent]:     分句结果 [list]
                        [tok]:      分词结果 [list[list]]
                        [dep]:      依存关系 [list[list]]
                        [dep_head]: 中心词汇 [list[list]]
                        注意: 依存句法切分必须以句子为单位
        """
        if self.mode == 'llm':
            return self._llm_tag(text)
        elif self.mode == 'local':
            return self._local_tag(text)
            
    def _llm_tag(self, text):
        tagset = self.tagset.upper()
        if self.lang == 'english':
            scheme_name = f'EN_{tagset}_NAME'
            example_name = f'EN_{tagset}_EXAMPLE'
            deprel_name = f'EN_{tagset}_DEPREL'
        elif self.lang == 'chinese':
            scheme_name = f'ZH_{tagset}_NAME'
            example_name = f'ZH_{tagset}_EXAMPLE'
            deprel_name = f'ZH_{tagset}_DEPREL'
            
        scheme = getattr(self.prompt, scheme_name)
        example = getattr(self.prompt, example_name)
        deprel = getattr(self.prompt, deprel_name)
        
        tok_sents = self.tokenizer.tokenize(text)
        #print(tok_sents)
        result = defaultdict(list)
        result['sent'] = tok_sents['sent']
        for sent, tokens in zip(tok_sents['sent'], tok_sents['tok']):
            
            # 构造 Prompt
            prompt = self.prompt.PROMPT.format(
                lang=self.lang,
                scheme=scheme,
                deprel=deprel,
                example=example,
                text=json.dumps(sent, ensure_ascii=False),
                tokens=json.dumps(tokens, ensure_ascii=False),
            )
            #print(prompt)
            
            # 调用大模型
            try:
                response = self.pipeline.get_json_response(
                    prompt=prompt, 
                )
                #print(response)
                tokens, heads, rels = self._convert_llm_response(response)
                result['tok'].append(tokens)
                result['dep_head'].append(heads)
                result['dep'].append(rels)
                
            except Exception as e:
                logging.error(f'LLM tagging error: {e}')
                
        return result
        
    def _local_tag(self, text):
        
        result = defaultdict(list)
        tok_sents = self.tokenizer.tokenize(text)
        result['sent'] = tok_sents['sent']
        doc = self.pipeline(tok_sents['tok'])
        for sent in doc.sentences:
            result['tok'].append([token.text for token in sent.words])
            result['lemma'].append([token.lemma for token in sent.words])
            result['pos'].append([token.xpos for token in sent.words])
            
            '''
            result['dep_'].append([
                (token.text, 
                 sent.words[token.head - 1].text if token.head > 0 else 'ROOT',
                 token.deprel)
                for token in sent.words
            ])
            '''
            
            result['dep'].append([token.deprel for token in sent.words])
            result['dep_head_id'].append([token.head for token in sent.words])
            result['dep_head'].append([
                sent.words[token.head - 1].text if token.head > 0 else 'ROOT'
                for token in sent.words
            ])
        return result
        
    @staticmethod
    def _convert_llm_response(response):
        tokens, heads, rels = [], [], []
        for item in response:
            tokens.append(item['token'])
            #rels.append((item['token'], item['head'], item['rel']))
            heads.append(item['head'])
            rels.append(item['rel'])
        return tokens, heads, rels
    
def save_annos(annos, out_file):
    rows = []
    for anno in annos:
        sents = anno['sent']
        for i, sent in enumerate(sents):
            tags = [f'{tok}_{head}_{dep}' for tok, head, dep in zip(anno['tok'][i], anno['dep_head'][i], anno['dep'][i])]
            text_with_tag = ' '.join(tags)
            rows.append({'text': sent, 'text_with_tag': text_with_tag})

    df = pd.DataFrame(rows)
    df.to_csv(out_file, sep='\t', index=False, header=False, encoding='utf-8')
        
def annotate_data(data, annotator):
    annos = []

    # 逐行遍历所有数据
    for index, text in tqdm(data.items(), total=len(data), desc="Dependency Parsing"):
        try:
            record = defaultdict(list)
            record['id'] = f'{index:05d}'
            
            # 提取待标注文本
            record['text'] = text
            
            # 标注选定文本
            anno = annotator.tag(text)
        
            # 提取标注结果
            record['sent'] = anno['sent']
            record['tok'] = anno['tok']
            record['dep'] = anno['dep']
            record['dep_head'] = anno['dep_head']
            annos.append(record)
        except Exception as e:
            print(f'Error at index {index}: {e}')
            continue
    
    return annos
    
def display_anno(anno):
    print(f'\n[ID]: {anno["id"]}')
    for i, sent in enumerate(anno['sent']):
        print(f'{sent}')
        print(f'{"-" * 80}')
        tags = [(tok, head, dep) for tok, head, dep in zip(anno['tok'][i], anno['dep_head'][i], anno['dep'][i])]
        print(tags)
        #print(f'{"-" * 80}')
    print(f'{"=" * 80}')
    
def compare_annos(
    annos_1,
    annos_2,
    annos_1_name,
    annos_2_name,
    show_diff=True,
):
    #intersections, unions = 0, 0
    for anno_1, anno_2 in zip(annos_1, annos_2):
        print(f"\n[ID]: {anno_1['id']}")

        for i, sent in enumerate(anno_1['sent']):
            print(f'{sent}')
            print(f'{"-" * 80}')
            anno_1_tok = anno_1['tok'][i]
            anno_1_head = anno_1['dep_head'][i]
            anno_1_dep = anno_1['dep'][i]
            anno_1_tags = [(tok, head, dep) for tok, head, dep in zip(anno_1_tok, anno_1_head, anno_1_dep) if dep != 'punct']
            
            anno_2_tok = anno_2['tok'][i]
            anno_2_head = anno_2['dep_head'][i]
            anno_2_dep = anno_2['dep'][i]
            anno_2_tags = [(tok, head, dep) for tok, head, dep in zip(anno_2_tok, anno_2_head, anno_2_dep) if dep != 'punct']
            
            set_1 = set(anno_1_tags)
            set_2 = set(anno_2_tags)
            
            intersection = set_1 & set_2
            union = set_1 | set_2
            #jac = len(intersection) / len(union)
            #print(f"Jaccard: {jac:.3f}")
            
            #intersections += len(intersection)
            #unions += len(union)
            
            if show_diff:
                only_in_1 = set_1 - set_2
                only_in_2 = set_2 - set_1
                print(f"{annos_1_name}: {only_in_1}")
                print(f"{annos_2_name}: {only_in_2}")
            
        print("=" * 60)
        
    #macro_jac = intersections / unions
    #print(f"Macro Jaccard: {macro_jac:.3f}")    
    
if __name__ == '__main__':

    # 打印日志信息
    logging.basicConfig(level=logging.INFO)

    # === 测试中文 ===
    
    lang = 'chinese'
    tagset = 'ud'
    zh_text = '那天晚上我没走掉。 陈清扬把我拽住，以伟大友谊的名义叫我留下来。'
    print(f'\n[中文赋码集]：{tagset}')
    print(f'[中文文本]：{zh_text}')
    print(f'{"=" * 30}')
    
    print(f'\n测试 1: Stanza 中文句法标注')
    print(f'{"=" * 30}')
    zh_dep_parser = DEPParser(lang=lang, tagset=tagset, mode='local')
    zh_doc = zh_dep_parser.tag(zh_text)
    print(f'[标注结果]:{zh_doc}')

    print(f'\n测试 2: LLM 中文句法标注')
    print(f'{"=" * 30}')
    zh_dep_parser = DEPParser(lang=lang, tagset=tagset, mode='llm')
    zh_doc = zh_dep_parser.tag(zh_text)
    print(f'[标注结果]:{zh_doc}')
    
    # === 测试英文 ===
    
    lang = 'english'
    tagset = 'ud'
    en_text = 'Chen Qingyang caught me and asked me to stay in the name of our great friendship.'
    print(f'\n[英文赋码集]：{tagset}')
    print(f'[英文文本]：{en_text}')
    print(f'{"=" * 30}')
    
    print(f'\n测试 3: Stanza 英文句法标注')
    print(f'{"=" * 30}')
    en_dep_parser = DEPParser(lang=lang, tagset=tagset, mode='local')
    en_doc = en_dep_parser.tag(en_text)
    print(f'[标注结果]:{en_doc}')

    print(f'\n测试 4: LLM 英文句法标注')
    print(f'{"=" * 30}')
    en_dep_parser = DEPParser(lang=lang, tagset=tagset, mode='llm')
    en_doc = en_dep_parser.tag(en_text)
    print(f'[标注结果]:{en_doc}')
    
# bfsujason@163.com

# 单元测试：
# python -m src.annotator.sem_tagger

import re
import json
import logging
import warnings
warnings.filterwarnings("ignore")

from tqdm import tqdm
from collections import defaultdict

from src.utils import clean_text, split_sents

# 配置日志
logger = logging.getLogger(__name__)

class SEMTagger:
    def __init__(
        self,
        lang,
        tagset='usas',
        mode='local',
        llm_model=None,
        enable_thinking=False,
    ):
        """
        :param lang:            语种 str
                                [chinese]:  中文
                                [english]:  英文
        :param tagset:          标注集 str
                                [usas]:     兰卡斯特语义标注集
                                https://ucrel.lancs.ac.uk/usas/
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
        :return:                SEMTagger Pipeline 实例
        """
        
        # 参数校验
        SUPPORTED = {
            'chinese': {
                'local': {'usas'},
                'llm':   {'usas'},
            },
            'english': {
                'local': {'usas'},
                'llm':   {'usas'},
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
        self.enable_thinking = enable_thinking
        
        if mode == 'local':
            import spacy
            from spacy.tokens import Doc
            from src.annotator.tokenizer import Tokenizer
            
            self.doc = Doc
            self.tokenizer = Tokenizer(lang=lang, mode='local')
            
            if lang == 'chinese':
                # === 加载中文语义标注模型 ===
                # 模型介绍: https://ucrel.github.io/pymusas/usage/how_to/tag_text_with/rule_based_tagger
                # 语义词表：https://github.com/UCREL/Multilingual-USAS/tree/master/Chinese

                logger.info('加载 PyMUSAS 中文语义标注模型 ...')
                self.pipeline = spacy.load('zh_core_web_sm', exclude=['parser', 'ner'])
                chinese_tagger_pipeline = spacy.load('cmn_dual_upos2usas_contextual_none')
                self.pipeline.add_pipe('pymusas_rule_based_tagger', source=chinese_tagger_pipeline)
                logger.info('PyMUSAS 中文语义标注模型加载完毕！')
            elif lang == 'english':
                # === 加载英文语义标注模型 ===
                # 模型介绍：https://ucrel.github.io/pymusas/usage/how_to/tag_text_with/rule_based_tagger
                # 语义词表：https://github.com/UCREL/Multilingual-USAS/tree/master/English
                
                logger.info('加载 PyMUSAS 英文句法标注模型 ...')
                self.pipeline = spacy.load('en_core_web_sm', exclude=['parser', 'ner'])
                english_tagger_pipeline = spacy.load('en_dual_none_contextual_none')
                self.pipeline.add_pipe('pymusas_rule_based_tagger', source=english_tagger_pipeline)
                logger.info('PyMUSAS 英文语义标注模型加载完毕！')
            
        elif mode == 'llm':
            from src.llm_client import LLMClient
            from src.prompt import sem_tag_prompt
            
            logger.info('加载 LLM 语义标注模型 ...')
            self.pipeline = LLMClient(model=llm_model)
            self.llm_model = self.pipeline.default_model
            self.prompt = sem_tag_prompt
            logger.info(f'LLM 语义标注模型加载完毕！')
            
    # A wrapper for _local_tag() and _llm_tag()
    def tag(self, text):
        """
        :param text:    输入文本 str
        :return:        标注结果 dict
                        [text]:     输入文本 str
                        [sent]:     分句结果 [list]
                        [tok]:      分词结果 [list]
                        [usas]:     语义赋码 [list]
        """
        if self.mode == 'llm':
            return self._llm_tag(text)
        elif self.mode == 'local':
            return self._local_tag(text)
            
    def _llm_tag(self, text):
        tagset = self.tagset.upper()
        
        if self.lang == 'english':
            prompt_name = f'EN_{tagset}_PROMPT'
            example_name = f'EN_{tagset}_EXAMPLE'
            tagset_name = f'EN_{tagset}_TAGSET'
        elif self.lang == 'chinese':
            prompt_name = f'ZH_{tagset}_PROMPT'
            example_name = f'ZH_{tagset}_EXAMPLE'
            tagset_name = f'ZH_{tagset}_TAGSET'
        
        prompt_tmpl = getattr(self.prompt, prompt_name)
        example = getattr(self.prompt, example_name)
        tagset = getattr(self.prompt, tagset_name)
        
        result = {}
        text = clean_text(text)
        sents = split_sents(text, lang=self.lang)
        
        result['text'] = text
        result['sent'] = sents['sent']
        
        # 构造 Prompt
        prompt = prompt_tmpl.format(
            tagset=tagset,
            example=example,
            text=json.dumps(text, ensure_ascii=False),
            #tokens=json.dumps(toks, ensure_ascii=False),
        )
        #print(prompt)
        
        # 调用大模型
        try:
            response = self.pipeline.get_response(
                prompt=prompt,
                json_output=True,
            )
            #print(response)
            tokens, tags = self._convert_llm_response(response)
            result['tok'] = tokens
            result['usas'] = tags
            
        except Exception as e:
            logging.error(f'LLM tagging error: {e}')
                
        return result
        
    def _local_tag(self, text):
        if not text or not isinstance(text, str):
            return None
        
        result = {}
        tok_sents = self.tokenizer.tokenize(text)
        result['text'] = tok_sents['text']
        result['sent'] = tok_sents['sent']
        
        toks = [tok for sent in tok_sents['tok'] for tok in sent]
        doc = self.doc(self.pipeline.vocab, words=toks)
        doc = self.pipeline(doc)
        
        '''
        results['tok'] = [token.text for token in doc]
        results['lemma'] = [token.lemma_ for token in doc]
        results['pos'] = [token.tag_ for token in doc]
        results['sem'] = [token._.pymusas_tags for token in doc]
        '''
        
        tokens, tags = self._convert_usas_results(doc)
        result['tok'] = tokens
        result['usas'] = tags

        return result
    
    def _convert_usas_results(self, doc):
        tokens, tags = [], []
        processed_mwe = []
        for i, token in enumerate(doc):
            #print(token.text, token.i)
            start, end = token._.pymusas_mwe_indexes[0]
            if (end - start) > 1:
                if start not in processed_mwe:
                    #print(token.text, token.i)
                    mwe = []
                    for _token in doc[start:end]:
                        mwe.append(_token.text)
                    if self.lang == 'english':
                        tokens.append(' '.join(mwe))
                    elif self.lang == 'chinese':
                        tokens.append(''.join(mwe))
                    #tags.append('/'.join(token._.pymusas_tags))
                    #tags.append(token._.pymusas_tags)
                    
                    # only keep highest-rank tag without suffix
                    tag = token._.pymusas_tags[0]
                    tag = self._process_usas_tag(tag)
                    tags.append(tag)
                    processed_mwe.append(start)
            else:
                tokens.append(token.text)
                #tags.append('/'.join(token._.pymusas_tags))
                #tags.append(token._.pymusas_tags)
                
                # only keep highest-rank tag without suffix
                tag = token._.pymusas_tags[0]
                tag = self._process_usas_tag(tag)
                tags.append(tag)
                
                #tags.append(token._.pymusas_tags[0])
        return tokens, tags
    
    @staticmethod
    def _process_usas_tag(tag):
        simple_tag = re.sub(r'[@%mfcni]', '', tag)
        return simple_tag
    
    def _convert_llm_response(self, response):
        tokens, tags = [], []
        for item in response:
            tokens.append(item['text'])
            tag = self._process_usas_tag(item['tag'])
            tags.append(tag)
        return tokens, tags
        
def save_annos(annos, out_file):
    rows = []
    for anno in annos:
        sents = anno['sent']
        tags = [f'{tok}_{pos}' for tok, pos in zip(anno['tok'], anno['pos'])]
        text = ' '.join(sents)
        text_with_tag = ' '.join(tags)
        rows.append({'text': text, 'text_with_tag': text_with_tag})

    df = pd.DataFrame(rows)
    df.to_csv(out_file, sep='\t', index=False, header=False, encoding='utf-8')
        
def annotate_data(data, annotator):
    annos = []

    # 逐行遍历所有数据
    for index, text in tqdm(data.items(), total=len(data), desc="Semantic Tagging"):
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
            record['usas'] = anno['usas']
            annos.append(record)
        except Exception as e:
            print(f'Error at index {index}: {e}')
            continue
    
    return annos
    
def display_anno(anno):
    print(f'\n[ID]: {anno["id"]}')
    print(f'{anno["text"]}')
    print(f'{'-' * 80}')
    tags = [(tok, usas) for tok, usas in zip (anno['tok'], anno['usas'])]
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
        anno_1_pos = anno_1['usas']
        anno_1_tags = [(tok, usas) for tok, usas in zip (anno_1['tok'], anno_1['usas'])]
        
        anno_2_tok = anno_2['tok']
        anno_2_tag = anno_2['usas']
        anno_2_tags = [(tok, usas) for tok, usas in zip (anno_2['tok'], anno_2['usas'])]
        
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

# === 单元测试 ===
if __name__ == '__main__':

    # 打印日志信息
    logging.basicConfig(level=logging.INFO)
    
    llm_model = 'deepseek-v3.2'
    enable_thinking = False

    # === 测试中文 ===

    lang = 'chinese'
    tagset = 'usas'
    zh_text = '那天晚上我没走掉。 陈清扬把我拽住，以伟大友谊的名义叫我留下来。'
    print(f'\n[中文赋码集]：{tagset}')
    print(f'[中文文本]：{zh_text}')
    print(f'{"=" * 30}')
    
    print(f'\n测试 1: PyMUSAS 中文语义标注')
    print(f'{"=" * 30}')
    zh_sem_tagger = SEMTagger(lang=lang, tagset=tagset, mode='local')
    zh_doc = zh_sem_tagger.tag(zh_text)
    print(f'[标注结果]:{zh_doc}')

    print(f'\n测试 2: LLM 中文语义标注')
    print(f'{"=" * 30}')
    zh_sem_tagger = SEMTagger(
        lang=lang,
        tagset=tagset,
        mode='llm',
        llm_model=llm_model,
        enable_thinking=enable_thinking,
    )
    zh_doc = zh_sem_tagger.tag(zh_text)
    print(f'[标注结果]:{zh_doc}')

    # === 测试英文 ===
    
    lang = 'english'
    tagset = 'usas'
    en_text = 'Chen Qingyang caught me and asked me to stay in the name of our great friendship.'
    print(f'\n英文语义标注赋码集：{tagset}')
    print(f'[英文文本]：{en_text}')
    print(f'{"=" * 30}')

    print(f'\n测试 3: PyMUSAS 英文语义标注')
    print(f'{"=" * 30}')
    en_sem_tagger = SEMTagger(lang=lang, tagset=tagset, mode='local')
    en_doc = en_sem_tagger.tag(en_text)
    print(f'[标注结果]:{en_doc}')
    
    print(f'\n测试 4: LLM 英文语义标注')
    print(f'{"=" * 30}')
    en_sem_tagger = SEMTagger(
        lang=lang,
        tagset=tagset,
        mode='llm',
        llm_model=llm_model,
        enable_thinking=enable_thinking,
    )
    en_doc = en_sem_tagger.tag(en_text)
    print(f'[标注结果]:{en_doc}')

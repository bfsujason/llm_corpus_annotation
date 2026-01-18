# bfsujason@163.com
# python -m src.annotator.syntax_annotation

import logging
import hanlp
from hanlp.utils.rules import split_sentence

# 配置日志
logger = logging.getLogger(__name__)

class SyntaxAnnotator:
    def __init__(self, lang, device=None):
        """
        :param lang: 指定语种，目前仅支持中文和英文
        :param device: 指定CPU或GPU (如 'cuda:0', 'cpu')
                       若为 None，自动选择设备
        """
        # 加载模型
        # 详见：https://hanlp.hankcs.com/docs/api/hanlp/pretrained/mtl.html
        # 中文：Electra Base
        # 英文：ModernBERT Base
        logger.info("初始化 HanLP 处理器...")
        if lang == "Chinese":
            logger.info(f"Loading Chinese Model: Electra Base...")
            MODEL_URI = hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_BASE_ZH
            self.pipeline = hanlp.load(MODEL_URI, devices=device)
            self.model_name = 'Electra Base'
        elif lang == "English":
            logger.info(f"Loading English Model: ModernBERT Base...")
            MODEL_URI = hanlp.pretrained.mtl.EN_TOK_LEM_POS_NER_SRL_UDEP_SDP_CON_MODERNBERT_BASE
            self.pipeline = hanlp.load(MODEL_URI, devices=device)
            self.model_name = 'ModernBERT Base'
        logger.info("模型加载完毕！")
        
        self.lang = lang

    def annotate(self, text, mode='light'):
        """
        :param text: 输入文本 (字符串)
        :param mode: 
            - 'light': 轻量模式 (仅分词、词性、依存句法标注)，速度快，适合大规模统计
            - 'full':  全量模式 (包含 NER、 SRL、 SDP 等标注)，速度较慢，适合深度分析
        :return: Document 对象 (类似字典)
        """
        if not text or not isinstance(text, str):
            return None

        # 自动分句
        sentences = split_sentence(text)
        
        # 可能返回字符串，保险起见转为列表
        if isinstance(sentences, str):
            sentences = [sentences]
            
        # 过滤空字符串
        sentences = [s for s in sentences if s.strip()]
        
        if not sentences:
            return None

        if self.lang == 'Chinese':
            return self._annotate_zh(sentences, mode)
        elif self.lang == 'English':
            return self._annotate_en(sentences, mode)
        else:
            raise ValueError(f"不支持语种: {self.lang}，请使用 'Chinese' 或 'English'")

    def _annotate_zh(self, sentences, mode):
        """处理中文文本"""
        
        tasks = None
        if mode == 'light':
            # 中文核心任务：细粒度分词 + PKU 词性 + SD 依存
            tasks = ['tok/fine', 'pos/pku', 'dep']
        
        # 调用 pipeline
        doc = self.pipeline(sentences, tasks=tasks)
        
        # 添加分句结果
        doc['sentences'] = sentences
        
        # 为便于调用，将复杂任务名称映射为简单名称
        if mode == 'light':
            doc['tokens'] = doc.get('tok/fine')
            doc['pos'] = doc.get('pos/pku')
             
        return doc

    def _annotate_en(self, sentences, mode):
        """处理英文文本"""

        tasks = None
        if mode == 'light':
            # 英文核心任务：分词 + 词形还原 + PTB 词性 + UD 依存
            tasks = ['tok', 'lem', 'pos', 'dep']
        
        # 调用 pipeline
        doc = self.pipeline(sentences, tasks=tasks)
        
        # 添加分句结果
        doc['sentences'] = sentences
        
        # 使用 tokens 字段访问分词结果，确保接口一致
        if mode == 'light':
            doc['tokens'] = doc['tok']
            
        return doc

    def print_model_capabilities(self):
        """
        显示模型支持的所有标注任务
        """
        if self.lang == 'Chinese':
            lang_trans = '中文'
        elif self.lang == 'English':
            lang_trans = '英文'
            
        print(f"\n[{lang_trans}模型支持的标注任务]")
        print("详见：https://hanlp.hankcs.com/docs/annotations/index.html")
        print(f"[{lang_trans}模型支持]: {list(self.pipeline.tasks.keys())}")

# === 单元测试 ===
if __name__ == "__main__":

    # 打印日志信息
    logging.basicConfig(level=logging.INFO)

    # 初始化模型
    zh_annotator = SyntaxAnnotator(lang='Chinese')
    en_annotator = SyntaxAnnotator(lang='English')
    
    # 打印模型支持的标注任务
    zh_annotator.print_model_capabilities()
    en_annotator.print_model_capabilities()
    
    print("\n" + "=" * 70)
    print("测试 1: 中文多句处理 (自动分句 + POS/PKU + DEP/SD 标注)")
    print("=" * 70)

    # --- 测试中文 ---
    zh_text = "那天晚上我没走掉。 陈清扬把我拽住，以伟大友谊的名义叫我留下来。"
    print(f"[ZH Input]: {zh_text}")
    
    zh_doc = zh_annotator.annotate(zh_text, mode='light')
    
    # 遍历结果
    if zh_doc:
        for i, sent_text in enumerate(zh_doc['sentences']):
            print(f"\n>> [句子 {i+1}]: {sent_text}")
            print(f"   Tokens:  {zh_doc['tokens'][i]}")
            print(f"   POS:     {zh_doc['pos'][i]}")
            dep_sample = zh_doc['dep'][i][:3] 
            print(f"   Dep(Top3): {dep_sample} ...")
    else:
        print("测试失败，请查看日志信息调试程序。")

    print("\n" + "=" * 70)
    print("测试 2: 英文多句处理 (自动分句 + POS/PTB + LEMMA + DEP/UD 标注)")
    print("=" * 70)

    # --- 测试英文 ---
    en_text = "I did not leave that night—Chen Qingyang caught me and asked me to stay in the name of our great friendship."
    print(f"[EN Input]: {en_text}")
    
    en_doc = en_annotator.annotate(en_text, mode='light')
    
    # 遍历结果
    if en_doc:
        for i, sent_text in enumerate(en_doc['sentences']):
            print(f"\n>> [Sentence {i+1}]: {sent_text}")
            print(f"   Tokens:  {en_doc['tokens'][i]}")
            print(f"   Lemma:   {en_doc['lem'][i]}") 
            print(f"   POS:     {en_doc['pos'][i]}")
            print(f"   Dep(Top3): {en_doc['dep'][i][:3]} ...")
    else:
        print("测试失败，请查看日志信息调试程序。")

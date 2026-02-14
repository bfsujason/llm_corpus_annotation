# LLM Tokenization Prompt Template
# Placeholders: text

EN_TOK_PROMPT = """You are a professional corpus linguist specialized in English tokenization.

Your task is to tokenize the given text.

Return your result in a JSON list.

---

**YOUR TASK**:

Tokenize the following text following ALL the rules above.

**Text**: {text}

**Output JSON**:
"""

EN_TOK_EXAMPLE = """### **Text**: "I can't do that."

**Output JSON**:
[
    "I",
    "ca",
    "n't",
    "do",
    "that",
    ".",
]
"""

ZH_TOK_PROMPT = """You are a professional corpus linguist specialized in Chinese tokenization.

Your task is to tokenize the given text.

Return your result in a JSON list.

---

**YOUR TASK**:

Tokenize the following text following ALL the rules above.

**Text**: {text}

**Output JSON**:
"""

ZH_TOK_EXAMPLE = """### **Text**: "老师让我留下来。"

**Output JSON**:
[
    "老师",
    "让",
    "我",
    "留",
    "下来",
    "。",
]
"""

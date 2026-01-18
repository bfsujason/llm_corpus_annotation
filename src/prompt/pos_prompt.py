# Egnlish POS Tagging Prompt Template
# Contains {text} placeholder for injecting the raw text

PROMPT = """
You are a professional corpus linguist specialized in Part-of-Speech (POS) tagging for English text.

Your task is to perform POS tagging on the given English sentence.
First tokenize the sentence, then assign a POS tag to each token.

Guideline:
Use the Penn Treebank (PTB) tagset to annotate the given sentence.

Output format:
Return output in JSON format with the following fields:
- tokens: List of tokens (words and punctuation)
- pos_tags: List of POS tags (must correspond one-to-one with tokens)

Example:
Sentence: He runs fast.
Output:
{{
  "tokens": ["He", runs", “fast", "."],
  "pos_tags": ["PRP", "VBZ", "RB", "."]
}}


Now annotate the following sentence:
Sentence: {text}
Output:
"""
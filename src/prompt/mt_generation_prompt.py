# Machine Translation Template

PROMPT = """You are an expert linguist specializing in {src_lang} to {tgt_lang} translation.
Your task is to translate the given {src_lang} text into {tgt_lang}.

### 1. Guidelines
-   Accuracy: Preserve the original meaning accurately.
-   Fluency: Ensure the translation reads smoothly and naturally.
-   Style: Maintain the style and tone of the original text.

### 2. Output Format
-   Return your translation in JSON format with a 'target_text' key.

Translate the following text according to the guidelines.

Text: {text}

Output JSON:
"""

# English Semantic Tagging Prompt Templates
# Contains {tag_list} placeholder for injecting the loaded tagset

PROMPT = """You are an expert linguist specializing in the **UCREL Semantic Analysis System (USAS)**.
Task: Semantic tagging for ENGLISH text.

### 1. The USAS Tagset Reference
Here is the complete list of USAS semantic tags. You MUST interpret the text based on these definitions:

{tag_list}

### 2. Annotation Rules (CRITICAL)
**Multi-Word Expressions (MWEs)**: 
-   Identify idioms, phrasal verbs, proper names, and fixed expressions as a **SINGLE unit**.
-   Example (idiom): "kicked the bucket" -> Tag as one unit (L1: Death), NOT separate words.
-   Example (proper name): "United States of America" -> Tag as one unit (Z2: Geographical names).

**Specificity Principle**: 
-   Always use the **most specific sub-category** available.
-   Example: If a word means "Happy", use `E4.1` (Happy) instead of the main category `E4` (Happy/sad). 
-   Use the Main Category (e.g., `A1`) ONLY if no sub-category fits exactly.

**Context Disambiguation**:
-   Choose the tag that fits the specific context of the sentence.
-   E.g., "Bank" in "river bank" is `W3` (Geographical), but in "bank account" is `I1.1` (Money: Affluence).

### 3. Output Format
Return a JSON list. Each item must be an object with:
- `text`: The word or MWE phrase.
- `tag`: The USAS tag code (e.g., "E4.1").
- `desc`: The definition of that tag from the reference list.

Analyze the following text. Split it into semantic units (words/MWEs) and assign USAS tags.

Text: {text}

Output JSON:
"""

# LLM POS Tagging Prompt Template
# Placeholders: tagset, example, text

EN_CLAWS_PROMPT = """You are a professional corpus linguist specialized in Part-of-Speech (POS) tagging.

Your task is to annotate English text following the annotation scheme of UCREL's CLAWS7 POS Tagset.
First segment the given text into tokens. Then assign a POS tag to each token.

## 1. ANNOTATION RULES

**YOU MUST**:
- **Keep all original text exactly as they appear - do NOT modify, correct, or rephrase any words**
- Tag each token individually by DEFAULT
- Ensure every token is covered in your output
- Keep punctuation tags as-is: punctuation marks are tagged with themselves (e.g., ',' → ',', '.' → '.', etc.)
- Apply ditto tags (see section 3) for multiword expressions where appropriate

## 2. Ditto tags
**Ditto tags** mark multiword expressions that function as a single grammatical unit. They are formed by adding a two-digit suffix to the base tag:
**Format**: `TAG##` where:

- First digit = total number of words in the multiword expression
- Second digit = position of this word in the sequence

**Examples**:

"in terms of" (single preposition): in_II31 terms_II32 of_II33
"at length" (single adverb): at_RR21 length_RR22
"a lot" (can be determiner or adverb): a_DD21 lot_DD22 OR a_RR21 lot_RR22
"in that" (can be conjunction or preposition+determiner): in_CS21 that_CS22 OR in_II that_DD1

**Common multiword expressions** that may use ditto tags include:

- Compound prepositions: in spite of, in front of, in terms of, because of, due to
- Compound conjunctions: in order that, so that
- Compound adverbs: at least, at most, at length
- Fixed expressions: a lot (of), a bit (of), kind of, sort of

**Note**: Only use ditto tags for established multiword expressions in the CLAWS idiomlist, not for arbitrary word combinations.

## 3. THE COMPLETE TAGSET

{tagset}

## 4. OUTPUT FORMAT

Return a JSON list. Each object must contain:

- `token`: The individual token.
- `tag`: The POS tag code for that token.
- `desc`: The description of that tag from the reference table.

## 5. EXAMPLES

{example}

---

**YOUR TASK**:

Annotate the following tokens. Tag each token following ALL the rules above, applying ditto tags to recognized multiword expressions.

**Text**: {text}

**Output JSON**:
"""

# === CLAWS 英语词性赋码集 ===

# 137 tags
# https://ucrel.lancs.ac.uk/claws7tags.html
EN_CLAWS_TAGSET = """
| Label | Description | Explanation |
|-------|-------------|-------------|
| APPGE | Possessive pronoun, pre-nominal | Marks possessive pronouns before nouns (my, your, our) |
| AT | Article | General article tag (the, no) |
| AT1 | Singular article | Identifies singular articles (a, an, every) |
| BCL | Before-clause marker | Marks subordinating expressions before clauses (in order that, in order to) |
| CC | Coordinating conjunction | Links words or clauses of equal status (and, or) |
| CCB | Adversative coordinating conjunction | Specifically marks contrastive conjunction (but) |
| CS | Subordinating conjunction | Introduces dependent clauses (if, because, unless, so, for) |
| CSA | As (conjunction) | Specifically tags "as" when used as conjunction |
| CSN | Than (conjunction) | Specifically tags "than" in comparative constructions |
| CST | That (conjunction) | Specifically tags "that" when introducing clauses |
| CSW | Whether (conjunction) | Specifically tags "whether" in subordinate clauses |
| DA | After-determiner with pronominal function | Post-determiners that can function as pronouns (such, former, same) |
| DA1 | Singular after-determiner | Singular post-determiners (little, much) |
| DA2 | Plural after-determiner | Plural post-determiners (few, several, many) |
| DAR | Comparative after-determiner | Comparative forms of post-determiners (more, less, fewer) |
| DAT | Superlative after-determiner | Superlative forms of post-determiners (most, least, fewest) |
| DB | Before-determiner with pronominal function | Pre-determiners that can function as pronouns (all, half) |
| DB2 | Plural before-determiner | Specifically marks plural pre-determiner (both) |
| DD | Determiner with pronominal function | General determiners that can stand alone (any, some) |
| DD1 | Singular determiner | Singular demonstrative/distributive determiners (this, that, another) |
| DD2 | Plural determiner | Plural demonstrative determiners (these, those) |
| DDQ | Wh-determiner | Interrogative determiners (which, what) |
| DDQGE | Wh-determiner, genitive | Possessive interrogative determiner (whose) |
| DDQV | Wh-ever determiner | Universal determiners (whichever, whatever) |
| EX | Existential there | Marks "there" in existential constructions (There is...) |
| FO | Formula | Identifies formulaic expressions or mathematical formulas |
| FU | Unclassified word | Tags words that don't fit standard categories |
| FW | Foreign word | Marks words from other languages not naturalized in English |
| GE | Germanic genitive marker | Marks possessive markers (' or 's) |
| IF | For (preposition) | Specifically tags "for" when used as preposition |
| II | General preposition | Standard prepositions not otherwise specified |
| IO | Of (preposition) | Specifically tags "of" as preposition |
| IW | With/without (prepositions) | Specifically tags "with" or "without" |
| JJ | General adjective | Standard adjectives in base form |
| JJR | General comparative adjective | Comparative adjectives (older, better, stronger) |
| JJT | General superlative adjective | Superlative adjectives (oldest, best, strongest) |
| JK | Catenative adjective | Adjectives in verb-like constructions (able in "be able to") |
| MC | Cardinal number (neutral) | Number words without number specification (two, three) |
| MC1 | Singular cardinal number | Specifically marks "one" |
| MC2 | Plural cardinal number | Pluralized numbers (sixes, sevens) |
| MCGE | Genitive cardinal number | Possessive forms of numbers (two's, 100's) |
| MCMC | Hyphenated number | Number ranges or spans (40-50, 1770-1827) |
| MD | Ordinal number | Sequential numbers (first, second, next, last) |
| MF | Fraction | Fractional expressions (quarters, two-thirds) |
| ND1 | Singular noun of direction | Directional nouns, singular (north, southeast) |
| NN | Common noun (neutral for number) | Nouns same in singular/plural (sheep, cod, headquarters) |
| NN1 | Singular common noun | Standard singular nouns (book, girl) |
| NN2 | Plural common noun | Standard plural nouns (books, girls) |
| NNA | Following noun of title | Academic/professional titles after names (M.A., Ph.D.) |
| NNB | Preceding noun of title | Titles before names (Mr., Prof., Dr.) |
| NNL1 | Singular locative noun | Geographic location nouns, singular (Island, Street) |
| NNL2 | Plural locative noun | Geographic location nouns, plural (Islands, Streets) |
| NNO | Numeral noun (neutral) | Quantity nouns (dozen, hundred) |
| NNO2 | Numeral noun, plural | Plural quantity nouns (hundreds, thousands) |
| NNT1 | Temporal noun, singular | Time-related nouns, singular (day, week, year) |
| NNT2 | Temporal noun, plural | Time-related nouns, plural (days, weeks, years) |
| NNU | Unit of measurement (neutral) | Measurement units (in, cc) |
| NNU1 | Singular unit of measurement | Singular measurement units (inch, centimetre) |
| NNU2 | Plural unit of measurement | Plural measurement units (ins., feet) |
| NP | Proper noun (neutral) | Named entities neutral for number (IBM, Andes) |
| NP1 | Singular proper noun | Single named entities (London, Jane, Frederick) |
| NP2 | Plural proper noun | Plural named entities (Browns, Reagans, Koreas) |
| NPD1 | Singular weekday noun | Individual day names (Sunday) |
| NPD2 | Plural weekday noun | Plural day names (Sundays) |
| NPM1 | Singular month noun | Individual month names (October) |
| NPM2 | Plural month noun | Plural month names (Octobers) |
| PN | Indefinite pronoun (neutral) | Indefinite pronoun neutral for number (none) |
| PN1 | Indefinite pronoun, singular | Singular indefinite pronouns (anyone, everything, nobody, one) |
| PNQO | Objective wh-pronoun | Interrogative pronoun, object form (whom) |
| PNQS | Subjective wh-pronoun | Interrogative pronoun, subject form (who) |
| PNQV | Wh-ever pronoun | Universal pronouns (whoever) |
| PNX1 | Reflexive indefinite pronoun | Reflexive form of indefinite pronoun (oneself) |
| PPGE | Nominal possessive personal pronoun | Independent possessive pronouns (mine, yours, hers) |
| PPH1 | 3rd person singular neuter pronoun | Neuter singular pronoun (it) |
| PPHO1 | 3rd person singular objective pronoun | Object form, he/she (him, her) |
| PPHO2 | 3rd person plural objective pronoun | Object form, they (them) |
| PPHS1 | 3rd person singular subjective pronoun | Subject form, singular (he, she) |
| PPHS2 | 3rd person plural subjective pronoun | Subject form, plural (they) |
| PPIO1 | 1st person singular objective pronoun | Object form, I (me) |
| PPIO2 | 1st person plural objective pronoun | Object form, we (us) |
| PPIS1 | 1st person singular subjective pronoun | Subject form, singular (I) |
| PPIS2 | 1st person plural subjective pronoun | Subject form, plural (we) |
| PPX1 | Singular reflexive personal pronoun | Reflexive forms, singular (yourself, itself, himself) |
| PPX2 | Plural reflexive personal pronoun | Reflexive forms, plural (yourselves, themselves) |
| PPY | 2nd person personal pronoun | Second person pronoun, all forms (you) |
| RA | Adverb after nominal head | Post-nominal modifying adverbs (else, galore) |
| REX | Adverb introducing apposition | Adverbs that introduce explanatory phrases (namely, e.g.) |
| RG | Degree adverb | Intensifying adverbs (very, so, too) |
| RGQ | Wh-degree adverb | Interrogative degree adverb (how) |
| RGQV | Wh-ever degree adverb | Universal degree adverb (however) |
| RGR | Comparative degree adverb | Comparative intensifiers (more, less) |
| RGT | Superlative degree adverb | Superlative intensifiers (most, least) |
| RL | Locative adverb | Location/direction adverbs (alongside, forward) |
| RP | Prepositional adverb/particle | Particles in phrasal verbs (about, in, up) |
| RPK | Prepositional adverb, catenative | Particles in catenative constructions (about in "be about to") |
| RR | General adverb | Standard manner/time/place adverbs |
| RRQ | Wh-general adverb | Interrogative adverbs (where, when, why, how) |
| RRQV | Wh-ever general adverb | Universal adverbs (wherever, whenever) |
| RRR | Comparative general adverb | Comparative adverbs (better, longer, faster) |
| RRT | Superlative general adverb | Superlative adverbs (best, longest, fastest) |
| RT | Quasi-nominal adverb of time | Time adverbs used nominally (now, tomorrow, today) |
| TO | Infinitive marker | Infinitive particle (to) |
| UH | Interjection | Exclamations and discourse markers (oh, yes, um, well) |
| VB0 | Be, base form | Base/imperative/subjunctive forms of "be" |
| VBDR | Were | Past tense plural/subjunctive of "be" |
| VBDZ | Was | Past tense singular of "be" |
| VBG | Being | Present participle of "be" |
| VBI | Be, infinitive | Infinitive form (to be, will be) |
| VBM | Am | First person singular present of "be" |
| VBN | Been | Past participle of "be" |
| VBR | Are | Present tense plural/second person of "be" |
| VBZ | Is | Third person singular present of "be" |
| VD0 | Do, base form | Base/imperative/subjunctive forms of "do" |
| VDD | Did | Past tense of "do" |
| VDG | Doing | Present participle of "do" |
| VDI | Do, infinitive | Infinitive form (to do, will do) |
| VDN | Done | Past participle of "do" |
| VDZ | Does | Third person singular present of "do" |
| VH0 | Have, base form | Base/imperative/subjunctive forms of "have" |
| VHD | Had (past tense) | Past tense of "have" |
| VHG | Having | Present participle of "have" |
| VHI | Have, infinitive | Infinitive form (to have, will have) |
| VHN | Had (past participle) | Past participle of "have" |
| VHZ | Has | Third person singular present of "have" |
| VM | Modal auxiliary | Modal verbs (can, will, would, should, may, must) |
| VMK | Modal catenative | Semi-modal verbs (ought, used in "ought to"/"used to") |
| VV0 | Base form of lexical verb | Base/imperative/subjunctive of main verbs (give, work) |
| VVD | Past tense of lexical verb | Simple past of main verbs (gave, worked) |
| VVG | -ing participle of lexical verb | Present participle of main verbs (giving, working) |
| VVGK | -ing participle catenative | -ing form in catenative use (going in "be going to") |
| VVI | Infinitive of lexical verb | Infinitive of main verbs (to give, will work) |
| VVN | Past participle of lexical verb | Past participle of main verbs (given, worked) |
| VVNK | Past participle catenative | Past participle in catenative use (bound in "be bound to") |
| VVZ | -s form of lexical verb | Third person singular present (gives, works) |
| XX | Not/n't | Negative particle in all forms |
| ZZ1 | Singular letter of alphabet | Single letters (A, b, c) |
| ZZ2 | Plural letter of alphabet | Plural letters (A's, b's, ABCs) |
"""

EN_CLAWS_EXAMPLE = """### Example 1:

**Text**: "As for me, I can't wait to see what this city looks like."

**Output JSON**:
[
    {{'token': 'As', 'tag': 'II21', 'desc': 'General preposition'}},
    {{'token': 'for', 'tag': 'II22', 'desc': 'General preposition'}},
    {{'token': 'me', 'tag': 'PPIO1', 'desc': '1st person singular objective pronoun'}},
    {{'token': ',', 'tag': ',', 'desc': 'Punctuation'}},
    {{'token': 'I', 'tag': 'PPIS1', 'desc': '1st person singular subjective pronoun'}},
    {{'token': 'ca', 'tag': 'VM', 'desc': 'Modal auxiliary'}},
    {{'token': "n't", 'tag': 'XX', 'desc': "Not/n't"}},
    {{'token': 'wait', 'tag': 'VVI', 'desc': 'Infinitive of lexical verb'}},
    {{'token': 'to', 'tag': 'TO', 'desc': 'Infinitive marker'}},
    {{'token': 'see', 'tag': 'VVI', 'desc': 'Infinitive of lexical verb'}},
    {{'token': 'what', 'tag': 'DDQ', 'desc': 'Wh-determiner'}},
    {{'token': 'this', 'tag': 'DD1', 'desc': 'Singular determiner'}},
    {{'token': 'city', 'tag': 'NN1', 'desc': 'Singular common noun'}},
    {{'token': 'looks', 'tag': 'VVZ', 'desc': '-s form of lexical verb'}},
    {{'token': 'like', 'tag': 'II', 'desc': 'General preposition'}},
    {{'token': '.', 'tag': '.', 'desc': 'Punctuation'}},
]

### Example 2:

**Text**: "He is lying in order to reduce his prison time."

**Output JSON**:
[
    {{'token': 'He', 'tag': 'PPHS1', 'desc': '3rd person singular subjective pronoun'}},
    {{'token': 'is', 'tag': 'VBZ', 'desc': 'Third person singular present of "be"'}},
    {{'token': 'lying', 'tag': 'VVG', 'desc': '-ing participle of lexical verb'}},
    {{'token': 'in', 'tag': 'BCL21', 'desc': 'Before-clause marker'}},
    {{'token': 'order', 'tag': 'BCL22', 'desc': 'Before-clause marker'}},
    {{'token': 'to', 'tag': 'TO', 'desc': 'Infinitive marker'}},
    {{'token': 'reduce', 'tag': 'VVI', 'desc': 'Infinitive of lexical verb'}},
    {{'token': 'his', 'tag': 'APPGE', 'desc': 'Possessive pronoun, pre-nominal'}},
    {{'token': 'prison', 'tag': 'NN1', 'desc': 'Singular common noun'}},
    {{'token': 'time', 'tag': 'NNT1', 'desc': 'Temporal noun, singular}},
    {{'token': '.', 'tag': '.', 'desc': 'Punctuation'}},
]

### Example 3:

**Text**: "People do all kinds of things in the name of family."

**Output JSON**:
[
    {{'token': 'People', 'tag': 'NN', 'desc': 'Common noun (neutral for number)'}},
    {{'token': 'do', 'tag': 'VD0', 'desc': 'Do, base form'}},
    {{'token': 'all', 'tag': 'DB', 'desc': 'Before-determiner with pronominal function'}},
    {{'token': 'kinds', 'tag': 'NN2', 'desc': 'Plural common noun'}},
    {{'token': 'of', 'tag': 'IO', 'desc': 'Of (preposition)'}},
    {{'token': 'things', 'tag': 'NN2', 'desc': 'Plural common noun'}},
    {{'token': 'in', 'tag': 'II41', 'desc': 'General preposition'}},
    {{'token': 'the', 'tag': 'II42', 'desc': 'General preposition'}},
    {{'token': 'name', 'tag': 'II43', 'desc': 'General preposition'}},
    {{'token': 'of', 'tag': 'II44', 'desc': 'General preposition'}},
    {{'token': 'family', 'tag': 'NN1', 'desc': 'Singular common noun'}},
    {{'token': '.', 'tag': '.', 'desc': 'Punctuation'}},
]
"""

ZH_PKU_PROMPT = """You are a professional corpus linguist specialized in Part-of-Speech (POS) tagging.

Your task is to annotate Chinese text following the annotation scheme of HanLP's PKU POS Tagset (北大计算语言学研究所词性标注集).
First segment the given text into tokens. Then assign a POS tag to each token.

## 1. ANNOTATION RULES

**YOU MUST**:
- **Keep all original text exactly as they appear - do NOT modify, correct, or rephrase any words**
- Tag each token individually by DEFAULT
- Ensure every token is covered in your output

## 2. THE COMPLETE TAGSET

{tagset}

## 3. OUTPUT FORMAT

Return a JSON list. Each object must contain:

- `token`: The individual token.
- `tag`: The POS tag code for that token.
- `desc`: The description of that tag from the reference table.

## 4. EXAMPLES

{example}

---

**YOUR TASK**:

Annotate the following tokens. Tag each token following ALL the rules above.

**Text**: {text}

**Output JSON**:
"""

# === PKU 汉语词性赋码集 ===

# 43 tags
# https://github.com/lancopku/pkuseg-python/blob/master/tags.txt
# https://github.com/hankcs/HanLP/blob/ddb1299bddff079e447af52ec12549c50636bfa8/docs/annotations/pos/pku.md

ZH_PKU_TAGSET = """
| Label | Description | Explanation |
|-------|-------------|-------------|
| **a** | Adjective | General adjectives describing qualities or states. Functions to modify nouns or serve as predicates. Example: 重要/a 步伐/n, 做/v 稳/a |
| **ad** | Adjective as adverbial | Adjectives functioning as adverbials. Functions to modify verbs. Example: 积极/ad 谋求/v, 及时/ad 报告/v |
| **Ag** | Adjectival morpheme | Bound morphemes with adjectival function. Functions as components in compound words that contribute adjectival meaning. Example: 绿色/n 似/d 锦/Ag |
| **an** | Adjective as noun | Adjectives that can function as nouns. Functions to describe entities that can stand alone as nominals. Example: 外交/n 和/c 安全/an |
| **b** | Distinguishing word | Words expressing distinction or classification, often modifying nouns. Functions to differentiate categories. Example: 女/b 司机/n, 金/b 手镯/n |
| **Bg** | Distinguishing word morpheme | Bound morphemes with distinguishing/classification function. Functions as morphemic components for words expressing distinction or differentiation. Example: 赤/Ag 橙/Bg 黄/a 绿/a 青/a 蓝/a 紫/a |
| **c** | Conjunction | Connectives linking words, phrases, or clauses. Functions to express logical relationships. Example: 合作/vn 与/c 伙伴/n |
| **d** | Adverb | Words modifying verbs, adjectives, or other adverbs. Functions to express manner, degree, time, scope, or negation. Example: 进一步/d 发展, 约/d 一百/m 个/q |
| **Dg** | Adverb morpheme | Bound morphemes with adverbial function. Functions as components contributing adverbial meaning in compounds. Example: 了解/v 甚/Dg 深/a |
| **e** | Interjection | Exclamations expressing emotion or response. Functions as standalone utterances showing feeling. Example: 啊/e ，/w 那/r 金灿灿/z 的/u 麦穗/n |
| **f** | Directional/Localizer | Direction words and location markers. Functions to indicate spatial or directional relationships. Example: 床/n 下/f, 军人/n 的/u 眼睛/n 里/f 不/d 是/v 没有/v 风景/n |
| **h** | Prefix | Prefixes attached to word beginnings. Functions to modify or specify word meanins. Example: 许多/m 非/h 主角/n 人物/n |
| **i** | Idiom | Fixed idiomatic expressions and set phrases. Functions as lexical units with non-compositional meanings. Example: 义无反顾/i, 其他四字成语 |
| **j** | Abbreviation | Shortened forms of longer expressions. Functions to represent organizations, concepts, or phrases concisely. Example: 德/j 外长/n, 文教/j |
| **k** | Suffix | Suffixes attached to word endings. Functions to derive new words or indicate grammatical features. Example: 少年儿童/l 朋友/n 们/k, 身体/n 健康/a 者/k |
| **l** | Idiom or fixed phrase | Idiomatic expressions have not yet become set idioms; they have a somewhat "temporary" nature. Example: 少年儿童/l 朋友/n 们/k, 由此可见/l |
| **m** | Numeral | Numbers and numerical expressions. Functions to express quantity or amount.  Case 1: Quantifier phrases should be segmented into numerals and measure words. Example: 三/m 个/q, 10/m 公斤/q, 一/m 盒/q 点心/n But a few quantity words are already registered entries in the dictionary, so they should not be further segmented. Example: 一个/m, 一些/m Case 2: Cardinal numbers, ordinal numbers, decimals, fractions, and percentages should not be segmented and are treated as one segmentation unit, marked as m. Example: 一百二十三/m, 20万/m, 123.54/m, 一个/m, 第一/m, 第三十五/m, 20%/m, 三分之二/m, 千分之三十/m, 几十/m 人/n, 十几万/m 元/q, 第一百零一/m 个/q  Case 3: Approximate numbers, when preceded by adverbs or adjectives, or followed by "来", "多", "左右" and other number-assisting words, should be separated. Example: 约/d 一百/m 多/m 万/m, 仅/d 一百/m 个/q, 四十/m 来/m 个/q, 二十/m 余/m 只/q, 十几/m 个/q, 三十/m 左右/m. Case 4: Two consecutive numerals, as well as expressions like "成百" and "上千”, should not be segmented. Example: 五六/m 年/q, 七八/m 天/q, 十七八/m 岁/q, 成百/m 学生/n, 上千/m 人/n Case 5: "Numeral + noun" structures expressing sequential relationships should be segmented. Example: 二/m 连/n, 三/m 部/n |
| **Mg** | Numeral morpheme | Bound morphemes with numerical meaning. Functions as numerical components in compounds. Example: 甲/Mg 减下/v 的/u 人/n 让/v 乙/Mg 背上/v, 凡/d “/w 寅/Mg 年/n ”/w 中/f 出生/v 的/u 人/n 生肖/n 都/d 属/v 虎/n |
| **n** | Common noun | General nouns for ordinary entities and concepts. Functions as heads of noun phrases. Example: 岗位/n, 城市/n, 机会/n, 她/r 是/v 责任/n 编辑/n |
| **Ng** | Noun morpheme | Bound morphemes with nominal function. Functions as noun-like components in compounds. Example: 出/v 过/u 两/m 天/q 差/Ng, 理/v 了/u 一/m 次/q 发/Ng |
| **nr** | Personal name | Names of people. Functions to identify individuals. Case 1: Surnames and given names of Han Chinese people, as well as those of non-Han people who use the same naming conventions as the Han, are segmented separately and each is tagged as nr. Example: 张/nr 仁伟/nr, 欧阳/nr 修/nr, 阮/nr 志雄/nr, 朴/nr 贞爱/nr Case 2: In addition to single-character and compound surnames, Han Chinese people also have double surnames; that is, some women, after marriage, add their husband’s surname to their original surname. In this situation, both surnames should be segmented and labeled as nr. Example: 陈/nr 方/nr 安生/nr, 唐/nr 鲁氏/nr Case 3: Job titles, honorifics, or titles after surnames should be separated. Example: 江/nr 主席/n, 小平/nr 同志/n, 江/nr 总书记/n, 张/nr 教授/n, 王/nr 部长/n, 陈/nr 老总/n, 李/nr 大娘/n, 刘/nr 阿姨/n, 龙/nr 姑姑/n Case 4: If a person’s abbreviation, honorific, or similar form consists of two characters, it is treated as a single segmentation unit and tagged as nr. Example: 老张/nr, 大李/nr, 小郝/nr, 郭老/nr, 陈总/nr Case 5: Clearly ranked kinship titles should be segmented; those not clearly ranked should not be segmented. Example: 三/m 哥/n, 大嫂/n, 大/a 女儿/n, 大哥/n, 小弟/n, 老爸/n Case 6: Some famous writers whose names or pen names are not easily distinguishable by surname and given name should be treated as one segmentation unit. Example: 鲁迅/nr, 茅盾/nr, 巴金/nr, 三毛/nr, 琼瑶/nr, 白桦/nr Case 7: For foreign names or the transliterated names of ethnic minority people (including the surnames of Japanese people) should not be segmented and should be labeled as nr. Example: 克林顿/nr, 叶利钦/nr, 才旦卓玛/nr, 小林多喜二/nr, 北研二/nr, 华盛顿/nr, 爱因斯坦/nr. Case 8: For some Western people's surnames that have a middle dot, do not segment. Example: 卡尔·马克思/nr |
| **ns** | Place name | Geographic locations and place names. Functions to identify locations. General example: 安徽/ns, 深圳/ns, 杭州/ns, 拉萨/ns, 哈尔滨/ns, 呼和浩特/ns, 乌鲁木齐/ns, 长江/ns, 黄海/ns, 太平洋/ns, 泰山/ns, 华山/ns, 亚洲/ns, 海南岛/ns, 太湖/ns, 白洋淀/ns, 俄罗斯/ns, 哈萨克斯坦/ns, 彼得堡/ns, 伏尔加格勒/ns Case 1: Country names regardless of length should be treated as one segmentation unit. Example: 中国/ns, 中华人民共和国/ns, 日本国/ns, 美利坚合众国/ns, 美国/ns Case 2: Place names with "省", "市", "县", "区", "乡", "镇", "村", "旗", "州", "都", "府", "道" and other single-character administrative division name suffixes should not be segmented and should be treated as one segmentation unit. Example: 四川省/ns, 天津市/ns, 景德镇/ns 沙市市/ns, 牡丹江市/ns, 正定县/ns, 海淀区/ns, 通州区/ns, 东井乡/ns, 双桥镇/ns 南化村/ns, 华盛顿州/ns, 俄亥俄州/ns, 东京都/ns, 大阪府/ns, 北海道/ns, 长野县/ns, 开封府/ns, 宣城县/ns Case 3: If a place name is followed by a one-character common noun indicating terrain or landform—such as “江, 河, 山, 洋, 海, 岛, 峰, 湖,” etc.—it should not be segmented. Example: 鸭绿江/ns，亚马逊河/ns， 喜马拉雅山/ns， 珠穆朗玛峰/ns，地中海/ns，大西洋/ns，洞庭湖/ns， 塞普路斯岛/n Case 4: When a place name is followed by a naturally formed common noun for a character like "街, 路, 道, 巷, 里, 町, 庄, 村, 弄, 堡", etc., it should not be segmented. Example: 中关村/ns, 长安街/ns, 学院路/ns, 景德镇/ns, 吴家堡/ns, 庞各庄/ns, 三元里/ns, 彼得堡/ns, 北京市巷/ns. |
| **nt** | Organization name | Names of organizations, companies, and institutions. Functions to identify organizational entities. General example: 联合国/nt, 中共中央/nt, 国务院/nt, 北京大学/nt 外交部/nt, 财政部/nt，教育部/nt, 国防部/nt |
| **nx** | Non-Chinese name/Transliteration | Foreign names or transliterated words. Functions to mark non-Chinese proper nouns. Example: A/nx 公司/n, B/nx 先生/n, X/nx 君/Ng, 24/m K/nx 镀金/n, C/nx 是/v 光速/n, Windows98/nx, PentiumIV/nx, I LOVE THIS GAME/nx, HanLP/nx |
| **nz** | Other proper noun | Proper nouns not classified as nr, ns, or nt. Functions for miscellaneous named entities and brands. General example: 满族/nz, 俄罗斯族/nz, 汉语/nz, 罗马利亚语/nz, 捷克语/nz, 中文/nz, 英文/nz, 满人/nz, 哈萨克人/nz, 诺贝尔奖/nz, 茅盾奖/nz Case 1: Transportation lines containing proper names (or abbreviations) are labeled as nz. Example: 津浦路/nz, 石太线/nz Case 2: When a proper name is followed by a polysyllabic noun such as "语言", "文学", "文化", "方式", "精神", etc., and loses its specificity, it should be segmented. Example: 欧洲/ns 语言/n, 法国/ns 文学/n, 西方/ns 文化/n, 贝多芬/nr 交响乐/n, 雷锋/nr 精神/n, 美国/ns 方式/n, 日本/ns 料理/n, 宋朝/t 古董/n Case 3: Trademarks (including proper names and words like "牌", "型", etc. that follow them) have specific reference and are labeled as nz, but the products that follow them are still labeled as common nouns n. Example: 康师傅/nr 方便面/n, 中华牌/nz 香烟/n, 牡丹III型/nz 电视机/n, 联想/nz 电脑/n， 鳄鱼/nz 衬衣/n, 耐克/nz 鞋/n Case 4: Names designated by serial numbers are generally not considered as proper names. Example: 2/m 号/q 国道/n Case 5: The titles of books, newspapers, magazines, documents, reports, agreements, contracts, etc. are typically identified by book title marks (《》) and are not considered proper nouns. Since these titles are often lengthy, the titles themselves are handled following standard processing rules. Example: 《/w 宁波/ns 日报/n 》/w,《/w 鲁迅/nr 全集/n 》/w, 中华/nz 读书/vn 报/n, 杜甫/nr 诗选/n Case 6: A small number of book titles, newspaper and magazine names, and other proper names should not be segmented. Example: 红楼梦/nz, 人民日报/nz, 儒林外史/nz Case 7: When it's impossible to determine whether certain proper names are personal names, place names, or institutional names, they are provisionally marked as nz. |
| **o** | Onomatopoeia | Sound-imitating words. Functions to represent auditory impressions. Example:哈哈/o 一/m 笑/v, 装载机/n 隆隆/o 推进/v |
| **p** | Preposition | Words governing nouns to show relationships. Functions to indicate location, direction, time, or manner. Example: 对/p 子孙后代/n 负责/v , 以/p 煤/n 养/v 农/Ng, 为/p 治理/v 荒山/n 服务/v, 把/p 青年/n 推/v 上/v 了/u 领导/vn 岗位/n |
| **q** | Classifier/Measure word (see m: Numeral)| Classifiers used with nouns and numbers. Functions to specify countable units. Example: 首/m 批/q, 一/m 年/q |
| **r** | Pronoun | Words substituting for nouns or noun phrases. Functions to refer anaphorically or deictically. When the single-syllable pronouns "本," "每," "各," "诸" are followed by single-syllable nouns, they merge with the following noun to form a pronoun; when followed by two-syllable nouns, they should be separated. Example: 本报/r, 每人/r, 本社/r, 本/r 地区/n, 各/r 部门/n |
| **Rg** | Pronominal morpheme | Bound morphemes with pronominal function. Functions as pronoun-like components in compounds. Example: 读者/n 就/d 是/v 这/r 两/m 棵/q 小树/n 扎根/v 于/p 斯/Rg 、/w, 成长/v 于/p 斯/Rg 的/u 肥田/n 沃土/n |
| **s** | Space word/Locative | Spatial words and location expressions. Functions to denote places or spaces. Example: 家里/s 的/u 电脑/n 都/d 联通/v 了/u 国际/n 互联网/n, 西部/s 交通/n 咽喉/n |
| **t** | Time word/Temporal noun | Words expressing time or temporal concepts. Functions to indicate time points or periods. Case 1: Year, month, day, hour, minute, and second should be segmented by year, month, day, hour, minute, and second, and labeled as t. Example: 1997年/t 3月/t 19日/t 下午/t 2时/t 18分/t Case 2: If there are no time indicators like "年, 月, 日, 时, 分, 秒" after the numbers, they should be labeled as numeral m. Example: 1998/m 中文/n 信息/n 处理/vn 国际/n 会议/n Case 3: Although historical dynasty names have the nature of proper nouns, they are still labeled as t. Example: 西周/t, 秦朝/t, 东汉/t, 南北朝/t, 清代/t Case 4: "牛年, 虎年" etc. should not be segmented at all, and are labeled as t. Example: 牛年/t, 虎年/t, 甲午年/t, 甲午/t 战争/n, 庚子/t 赔款/n, 戊戌/t 变法/n |
| **Tg** | Temporal morpheme | Bound morphemes with temporal meaning. Functions as time-related components in compounds. Example: 3日/t 晚/Tg 在/p 总统府/n 发表/v 声明/n ，尊重/v 现/Tg 执政/vn 当局/n 的/u 权威/n |
| **u** | Auxiliary/Particle | Function words including particles and auxiliaries. Functions for grammatical purposes. Example: 的, 地, 得, 着/了/过 aspect markers) |
| **v** | Verb | General verbs expressing actions, processes, or states. Functions as main predicates. Example: 奠定/v 了/u 基础/n, 总结/v 经验/n |
| **vd** | Verb as adverbial | Verbs directly functioning as adverbials (状语). Functions to modify other verbs, combining verbal and adverbial characteristics. Example: 形势/n 会/v 持续/vd 好转/v, 认为/v 是/v 电话局/n 收/v 错/vd 了/u 费/n |
| **Vg** | Verb morpheme | Bound morphemes with verbal function. Functions as verb-like components in compounds. Example: 洗/v 了/u 一个/m 舒舒服服/z 的/u 澡/Vg |
| **vn** | Verb as noun | Verbs that function as nouns. Example: 引起/v 人们/n 的/u 关注/vn 和/c 思考/vn, 收费/vn 电话/n 的/u 号码/n |
| **w** | Punctuation | Punctuation marks and symbols. Functions to structure text. Example: , 。，！？；：). |
| **x** | Unclassified/String | Unclassifiable items or character strings. Functions as catch-all for unclear or non-standard elements. |
| **y** | Sentence-final particle | Functions to express mood, attitude, or questioning. Example: 会/v 泄露/v 用户/n 隐私/n 吗/y, 又/d 何在/v 呢/y ？/w, 北京/ns 到/v 了/y, 我/r 和/p 他/r 见面/v 了/y |
| **Yg** | Modal particle morpheme | Bound morphemes with modal particle function. Functions as morphemic components contributing modal or sentence-final particle meaning in compounds. Example: 唯/d 大力/d 者/k 能/v 致/v 之/u 耳/Yg |
| **z** | Descriptive word/Stative verb | Descriptive or stative words. Functions to describe states or properties. Example: 取得/v 扎扎实实/z 的/u 突破性/n 进展/vn, 四季/n 常青/z 的/u 热带/n 树木/n, 短短/z 几/m 年/q 间 |
"""

ZH_PKU_EXAMPLE = """### Example 1:

**Text**: "领导对这件事有考虑"

**Output JSON**: 
[
  {{'token': '领导', 'tag': 'n', 'desc': 'Common noun'}},
  {{'token': '对', 'tag': 'p', 'desc': 'Preposition'}},
  {{'token': '这', 'tag': 'r', 'desc': 'Pronoun'}},
  {{'token': '件', 'tag': 'q', 'desc': 'Classifier/Measure word'}},
  {{'token': '事', 'tag': 'n', 'desc': 'Common noun'}},
  {{'token': '有', 'tag': 'v', 'desc': 'Verb'}},
  {{'token': '考虑', 'tag': 'vn', 'desc': 'Verb as noun'}},
]

### Example 2:

**Text**: "予以严肃处理"

**Output JSON**: 
[
  {{'token': '予以', 'tag': 'v', 'desc': 'Verb'}},
  {{'token': '严肃', 'tag': 'a', 'desc': 'Adjective'}},
  {{'token': '处理', 'tag': 'vn', 'desc': 'Verb as noun'}},
]

### Example 3:

**Text**: 北京到了

**Output JSON**: 
[
  {{'token': '北京', 'tag': 'ns', 'desc': 'Place name'}},
  {{'token': '到', 'tag': 'v', 'desc': 'Verb'}},
  {{'token': '了', 'tag': 'y', 'desc': 'Sentence-final particle'}},
]

### Example 4:

**Text**: "维护环境的整洁"

**Output JSON**: 
[
  {{'token': '维护', 'tag': 'v', 'desc': 'Verb'}},
  {{'token': '环境', 'tag': 'a', 'desc': 'Adjective'}},
  {{'token': '的', 'tag': 'u', 'desc': 'Auxiliary/Particle'}},
  {{'token': '整洁', 'tag': 'an', 'desc': 'Adjective as noun'}},
]
"""
# LLM Dependency Parsing Prompt Template
# Placeholders: deprel, example, text

EN_UD_PROMPT = """You are a professional corpus linguist specialized in dependency parsing.

Your task is to annotate English text following the annotation scheme of English Universal Dependency 2.0.
First segment the given text into tokens. Then assign the head token and dependency relation to each token.

## 1. ANNOTATION RULES

**YOU MUST**:
- **Keep all original text exactly as they appear - do NOT modify, correct, or rephrase any words**
- Tag each token individually by DEFAULT
- Ensure every token is covered in your output

## 2. THE COMPLETE DEPENDENCY RELATIONS

{deprel}

## 3. OUTPUT FORMAT

Return a JSON list. Each object must contain:

- `token`: The individual token.
- `head: The head token for that token.
- `rel`: The dependency relation.
- `desc`: The description of dependency relation from the reference table.

## 4. EXAMPLE

{example}

---

**YOUR TASK**:

Annotate the following Tokens. Tag each token following ALL the rules above.

**Text**: {text}

**Output JSON**:
"""

# === UD 2.0 英语依存关系 ===

# 51 labels
# https://universaldependencies.org/u/dep/
# https://universaldependencies.org/treebanks/en_ewt/index.html
EN_UD_DEPREL = """
# English EWT Treebank Dependency Relations

## In the following examples, the head word is enclosed by single bracket: [], while the dependent is by double star: **.

| Label | Description | Explanation |
|-------|-------------|-------------|
| **root** | Root of sentence | The main predicate of the sentence with no governor. Every sentence has exactly one root. |
| **acl** | Clausal modifier of noun | A finite or non-finite clause that modifies a noun (adjectival clause). Note that in English relative clauses get assigned a specific relation acl:relcl, a subtype of acl. Example: the [book] to **read**, A [president] **certain** that they are correct, online [sites] **offering** booking facilities |
| **acl:relcl** | Relative clause modifier | **SUBTYPE**: Specifically marks relative clauses with explicit  (that/which/who) or implicit relativizer. Example: the [book] that I **read**, [people] who **came**, the [man] you **love** |
| **advcl** | Adverbial clause modifier | A clause modifying a verb/predicate as adverbial. Example: he [left] because it **rained**, when **finished**, [call] me |
| **advcl:relcl** | Adverbial relative clause modifier | **ENGLISH-SPECIFIC SUBTYPE**: A relative clause that modifies a clause. Example: I tried to [explain] myself - which was a bad **idea** |
| **advmod** | Adverbial modifier | Adverb modifying verb/adj/adverb. Example: **very** [good], **not** [going], **extremely** [fast] |
| **amod** | Adjectival modifier | Adjective modifying noun. Example: **red** [car], [nothing] **wrong** |
| **appos** | Appositional modifier | Noun phrase in apposition to another. Example: [Sam], my **brother**; the [CEO], John **Smith** |
| **aux** | Auxiliary | Modal/aspectual auxiliary verbs. Example: **has** [died], **will** [go] |
| **aux:pass** | Passive auxiliary | **SUBTYPE**: Marks passive voice auxiliaries. Example: **was** [built], **got** [fired]. Uses 'be' or 'get'. |
| **case** | Case marking | Preposition/postposition marking grammatical case. Example: **in** the [house], responsible **for** [meals],  the [school] **'s** grounds |
| **cc** | Coordinating conjunction | Conjunction linking coordinates. Example: apples **and** [oranges], **or**, **but**, **nor**, etc. |
| **cc:preconj** | Preconjunct | **ENGLISH-SPECIFIC SUBTYPE**: First part of correlative conjunctions. Example: **both** the [boys] and the girls |
| **ccomp** | Clausal complement | Finite clause complement of verb. Example: I [know] that he **left**, I'm [afraid] that this would **happen** |
| **compound** | Compound | Multi-word expressions forming single unit. Example: **phone** [book], **bus** [stop], **ice** [cream] |
| **compound:prt** | Phrasal verb particle | **ENGLISH-SPECIFIC SUBTYPE**: Particle in phrasal verbs. Example: [give] **up**, [take] **off** |
| **conj** | Conjunct | Second/subsequent conjunct in coordination. Example: [apples] and **oranges**, [run] or **walk** |
| **cop** | Copula | Copula verb (linking verb). The copula 'be' is not treated as the head of a clause, but rather the nonverbal predicate. Example: **is** a [student] (Head: student, Dependent: is), **was** [happy], **being** [ready] |
| **csubj** | Clausal subject | Finite clause as subject. Example: What he **said** was [true], that it **rained** [surprised] me |
| **csubj:outer** | Outer clause subject | **SUBTYPE**:  Aa clausal subject of a copular clause whose predicate is itself a clause, to signal that it is not the subject of the nested clause. |
| **csubj:pass** | Clausal passive subject | **SUBTYPE**: Clausal subject in passive. Example: that he **lied** was [believed] |
| **dep** | Unclassified dependency | Fallback relation when relation cannot be determined. Should be rare in well-annotated corpora. |
| **det** | Determiner | Articles and determiners. Example: **the** [book], **a** [car], **this** [person] |
| **det:predet** | Predeterminer | **ENGLISH-SPECIFIC SUBTYPE**: Predeterminers appearing before articles. Example: **all** the [books], **both** the [cars], **what** a [mess] |
| **discourse** | Discourse element | Interjections, discourse markers, filler words. Example: **well**, I [think]...; **oh**; **um**, etc. |
| **dislocated** | Dislocated elements | Fronted/postposed elements outside core structure. Example: **that person**, I [know] him; I [know] him, **that person** |
| **expl** | Expletive | Expletive/pleonastic pronouns with no semantic content. Example: **it** is [clear] that we should decline, **there** [is] a problem |
| **fixed** | Fixed multiword expression | Fixed grammaticalized expressions. Example: [in] **order** **to**, [as] **well** **as**, [rather] **than** |
| **flat** | Flat multiword expression | Non-headed multiword expressions. Example: [Joe] **Biden**, titles, dates |
| **goeswith** | Goes with | Marks word fragments that should be joined. Used for tokenization errors. Example: [some-] **thing** → something |
| **iobj** | Indirect object | Indirect object of ditransitive verb. Example: [give] **me** the book, tell [him] the truth |
| **list** | List | Relations in list structures. Example: items in bulleted/numbered lists, enumeration structures |
| **mark** | Marker | Subordinating conjunction/marker. Example: **if** it [rains], **because** I [left], **that** he [came], **to** [go] |
| **nmod** | Nominal modifier | Noun modifying another noun (usually with preposition). Example: the [destruction] of the **city**, [book] about **science** |
| **nmod:desc** | Descriptive modifier | **ENGLISH-SPECIFIC SUBTYPE**: Descriptive nominal modifiers without preposition, typically informal. Example: [age] **70**, [size] **large** |
| **nmod:poss** | Possessive modifier | **SUBTYPE**: Possessive/genitive nominal modifier. Example: **John** 's [book], the **company** 's [profits] |
| **nmod:unmarked** | Unmarked modifier | **ENGLISH-SPECIFIC SUBTYPE**: Nominal modifier without case marking (temporal or other special cases). Example: a [pizza] the **size** of a sun |
| **nsubj** | Nominal subject | Subject of verb/clause. Example: **I** [eat], **the dog** [barked] |
| **nsubj:outer** | Outer subject | **SUBTYPE**: This relation specifies a nominal subject of a copular clause whose predicate is itself a clause, to signal that it is not the subject of the nested clause. |
| **nsubj:pass** | Passive nominal subject | **SUBTYPE**: Subject in passive construction. Example: the **book** was [read] |
| **nummod** | Numeric modifier | Number modifying noun. Example: **three** [books], **first** [place] |
| **obj** | Object | Direct object of verb. Example: [read] a **book**, [eat] **pizza**, [see] **him** |
| **obl** | Oblique nominal | Oblique argument/adjunct. Example: [go] to **school**, [live] in **Boston**, [work] on **Monday** |
| **obl:agent** | Oblique agent | **SUBTYPE**: Agent in passive (with 'by'). Example: [written] by **Shakespeare**, [built] by **workers** |
| **obl:unmarked** | Unmarked oblique | **ENGLISH-SPECIFIC SUBTYPE**: Oblique without preposition (typically temporal/spatial). Example: [go] home last **night** |
| **orphan** | Orphan | Promotion in gapping constructions. Used when head is elided in coordination. Example: John went to Paris and **Mary** to [London] |
| **parataxis** | Parataxis | Relation between coordinated/juxtaposed clauses without explicit coordination. Example: he **came**, I [left] |
| **punct** | Punctuation | All punctuation marks. Example: **.**, **,**, **!**, **?**, **"**, **(**, **)** |
| **reparandum** | Reparandum | Disfluency/correction in speech or informal writing. Overridden/corrected word. Example: go to the **right-* to the [left] |
| **vocative** | Vocative | Addressee/call. Example: **John**, [come] here |
| **xcomp** | Open clausal complement | Predicative/infinitive complement without own subject. Example: [want] to **go**, [seems] **happy**, [made] him **leave** |
"""

EN_UD_EXAMPLE = """"### Example 1:

**Text**: "Bill is an honest man."

**Output JSON**:
[
    {{'token': 'Bill', 'head': 'man', 'rel':'nsubj', 'desc': 'Nominal subject'}},
    {{'token': 'is', 'head': 'man', 'rel':'cop', 'desc': 'cop'}},
    {{'token': 'an', 'head': 'man', 'rel':'det', 'desc': 'Determiner'}},
    {{'token': 'honest', 'head': 'man', 'rel':'amod', 'desc': 'Adjectival modifier'}},
    {{'token': 'man', 'head': 'ROOT', 'rel':'root', 'desc': 'Root of sentence'}},
    {{'token': '.', 'head': 'man', 'rel':'punct', 'desc': 'Punctuation'}},
]

### Example 2:

**Text**: "He is powerless to console the girl."

**Output JSON**:
[
    {{'token': 'He', 'head': 'powerless', 'rel':'nsubj', 'desc': 'Nominal subject'}},
    {{'token': 'is', 'head': 'powerless', 'rel':'cop', 'desc': 'Copula'}},
    {{'token': 'powerless', 'head': 'ROOT', 'rel':'root', 'desc': 'Root of sentence'}},
    {{'token': 'to', 'head': 'console', 'rel':'mark', 'desc': 'Marker'}},
    {{'token': 'console', 'head': 'powerless', 'rel':'xcomp', 'desc': 'Open clausal complement'}},
    {{'token': 'the', 'head': 'girl', 'rel':'', 'desc': 'Determiner'}},
    {{'token': 'girl', 'head': 'console', 'rel':'obj', 'desc': 'Object'}},
    {{'token': '.', 'head': 'powerless', 'rel':'punct', 'desc': 'Punctuation'}},
]

Example 3:

**Text**: "One of the students passed the exam."

**Output JSON**:
[
    {{'token': 'One', 'head': 'passed', 'rel':'nsubj', 'desc': 'Nominal subject'}},
    {{'token': 'of', 'head': 'students', 'rel':'case', 'desc': 'Case marking'}},
    {{'token': 'the', 'head': 'students', 'rel':'det', 'desc': 'Determiner'}},
    {{'token': 'students', 'head': 'One', 'rel':'nmod', 'desc': 'Nominal modifier'}},
    {{'token': 'passed', 'head': 'ROOT', 'rel':'root', 'desc': 'Root of sentence'}},
    {{'token': 'the', 'head': 'exam', 'rel':'det', 'desc': 'Determiner'}},
    {{'token': 'exam', 'head': 'passed', 'rel':'obj', 'desc': 'Object'}},
    {{'token': '.', 'head': 'passed', 'rel':'punct', 'desc': 'Punctuation'}},
]

Example 4:

**Text**: "What are you talking about?"

**Output JSON**:
[
    {{'token': 'What', 'head': 'talking', 'rel':'obl', 'desc': 'Oblique nominal'}},
    {{'token': 'are', 'head': 'talking', 'rel':'aux', 'desc': 'Auxiliary'}},
    {{'token': 'you', 'head': 'talking', 'rel':'nsubj', 'desc': 'Nominal subject'}},
    {{'token': 'talking', 'head': 'ROOT', 'rel':'root', 'desc': 'Root of sentence'}},
    {{'token': 'about', 'head': 'case', 'rel':'What', 'desc': 'Case marking'}},
    {{'token': '?', 'head': 'talking', 'rel':'punct', 'desc': 'Punctuation'}},
]
"""

ZH_UD_PROMPT = """You are a professional corpus linguist specialized in dependency parsing.

Your task is to annotate Chinese text following the annotation scheme of Chinese Universal Dependency 2.0.
First segment the given text into tokens. Then assign the head token and dependency relation to each token.

## 1. ANNOTATION RULES

**YOU MUST**:
- **Keep all original text exactly as they appear - do NOT modify, correct, or rephrase any words**
- Tag each token individually by DEFAULT
- Ensure every token is covered in your output

## 2. THE COMPLETE DEPENDENCY RELATIONS

{deprel}

## 3. OUTPUT FORMAT

Return a JSON list. Each object must contain:

- `token`: The individual token.
- `head: The head token for that token.
- `rel`: The dependency relation.
- `desc`: The description of dependency relation from the reference table.

## 4. EXAMPLES

{example}

---

**YOUR TASK**:

Annotate the following tokens. Tag each token following ALL the rules above.

**Text**: {text}

**Output JSON**:
"""

# === UD 2.0 汉语依存关系 ===

# 48 labels
# https://universaldependencies.org/u/dep/
# https://universaldependencies.org/treebanks/zh_gsd/index.html
ZH_UD_DEPREL = """
### Chinese GSD Treebank Dependency Relations

**In the following examples, the head word is enclosed by single bracket: `[head]`, while the dependent is by double star: `**dependent**`.**

| Label | Description | Explanation |
|-------|-------------|-------------|
| **root** | Root of sentence | The main predicate of the sentence with no governor. Every sentence has exactly one root. |
| **acl** | Clausal modifier of noun | A clause that modifies a noun (adjectival clause). Example: 我**看**的[书] |
| **advcl** | Adverbial clause modifier | A clause modifying a verb/predicate as adverbial. Example: 因为**下雨**，[取消]了, **拍**胸口[保证] |
| **advmod** | Adverbial modifier | Adverb modifying verb/adj/adverb. Example: **很**[好], **不**[去], **已经**[答应]他们 |
| **amod** | Adjectival modifier | Adjective modifying noun. Example: **新**[产品], **严重**的[问题] |
| **appos** | Appositional modifier | Noun phrase in apposition to another. Example: [他们]**四个**写得, 在[门口]**那边** |
| **aux** | Auxiliary | Modal/aspectual auxiliary verbs. Example: **应该**[帮帮]我们, **着**(durative aspect), **了**(perfective aspect), **过**(experiential aspect) |
| **aux:pass** | Passive auxiliary | **SUBTYPE**: Marks passive voice auxiliaries. Example: **被**[打]. Common with 被(bèi), 为(wèi). |
| **case** | Case marking | Adposition marking case relation. Example: **在**[公司]已经完成了, 戴**在**[手]上, [你]**的**电话, **跟**[我]来, **把**[他们]藏在房里, **被**[他]偷了 |
| **case:loc** | Postpositional localizer | Treat localizers (方位词) as postpositions which typically denote spatial locations analogous to adpositions or case markers  Example: 放在你[桌]**上** |
| **cc** | Coordinating conjunction | Conjunction linking coordinates. Example: 和, 或, 但. Example: 苹果**和**[香蕉], 先管**而**后[教] |
| **ccomp** | Clausal complement | A full clause that functions like an object of verb. Example: 我[知道]他*来*了. The ccomp relation is also used for the copula 是(shì) when its argument is a clause (although in copular constructions, 是(shì) is a cop dependent of the predicate when the predicate is non-clausal). Example: 原因[是]他没**来** |
| **clf** | Classifier | **CHINESE-SPECIFIC**: Measure words/classifiers between number and noun. Example: [三]**本**书, [一]**个**人 |
| **compound** | Compound | Used primarily for noun-noun compounds. Example: **中文**[试卷], **职业**[介绍所] |
| **compound:dir** | Directional verb compound | *CHINESE-SPECIFIC SUBTYPE**: A "directional verb compound" consists of a series of at least two verbs where the second verb is one of the directional or deitic motion verbs Example: 他[爬]**上来**了, 我把你[留]**下来**, [爬]**上**山**去**了, [带]他们**出去** |
| **compound:ext** | Extent compound | **CHINESE-SPECIFIC SUBTYPE**: Extent/degree constructions with 得(de). Example: [跑*]*得**很快 |
| **compound:vo** | Verb-object compound | **CHINESE-SPECIFIC SUBTYPE**: Used for verb-verb and verb-adjective compounds where the second verb/adjective covers what are known as “resultative complements” and “phase complements” in Chinese. Example: 我[帅]**破**了腿, [行]不**通**的, 他[哭]**累**了 |
| **compound:vv** | Verb-verb compound | **CHINESE-SPECIFIC SUBTYPE**: Used for verb-object compounds where the combination is semantically one unit but syntactically separate. These are known as 离合词 "separable words" in Chinese. Example: [打]了几次**针**, 我[读]完**书**了 |
| **conj** | Conjunct | Second/subsequent conjunct in coordination. Example: [苹果]和**香蕉** |
| **cop** | Copula | Copula verb (linking verb). The copula '是' or '为' is not treated as the head of a clause, but rather the nonverbal predicate. Example: **是**[学生] (Head: 学生, Dependent: 是), **为**[主席] |
| **csubj** | Clausal subject | Finite clause as subject. Example: **学**中文很[难] |
| **csubj:pass** | Clausal passive subject | **SUBTYPE**: Clausal subject in passive. Example: **换**衣服被人[看]见 |
| **det** | Determiner | Articles and determiners. Example: **这**个[人], **每**[天], **哪**一[位]. Note: In the Determiner + Classifier + Noun construction, the head of determiner is the noun, instead of the classifier. |
| **discourse** | Discourse element | Interjections, discourse markers. Example: **啊**, **嗯**, **哦* |
| **discourse:sp** | Sentence-final particle | **CHINESE-SPECIFIC SUBTYPE**: Sentence-final particles showing mood/tone. Example: [好]**吗*, [是]**的**, [来]**吧** |
| **dislocated** | Dislocated elements | Fronted/postposed elements outside core structure. Example: 今天的**午餐**，我[请客] |
| **flat** | Flat multiword expression | Non-headed multiword expressions. For names, titles, dates |
| **flat:foreign** | Foreign flat expression | **SUBTYPE**: Foreign language expressions. Example: 当《[Game] **Informer**》提到 |
| **flat:name** | Name flat structure | **SUBTYPE**: Proper names without internal structure. |
| **iobj** | Indirect object | Indirect object of verb. Example: [给]他**书** |
| **mark** | Marker | Subordinating conjunction/marker. Example: **如果**, **因为**, **虽然**; 要[玩]**的话**, 我就将事情闹大 |
| **mark:adv** | Adverbial marker | **CHINESE-SPECIFIC SUBTYPE**: Adverbial particle 地(de) linking adverb to verb. Example: [慢慢]**地**走 |
| **mark:rel** | Relativizer | **CHINESE-SPECIFIC SUBTYPE**: Three related uses of 的 de: adjectives, relative clauses, and nominalized clauses. Example: [严重]**的**问题, 我[买]**的**书, 他们[写]**的**不是诗 |
| **nmod** | Nominal modifier | Used for nominal dependents of another noun or noun phrase and functionally corresponds to an attribute, or genitive (possessive) complement. In Mandarin, it is expressed with the 的 de particle. Example: **你**的[电话], **你**[公公], **目前**的[情况] |
| **nmod:tmod** | Temporal modifier | **SUBTYPE**: Temporal noun as modifier. Example: **去年**的[事] |
| **nsubj** | Nominal subject | Subject of verb/clause. Example: **我**马上[吃饭], **他**是[学生] |
| **nsubj:pass** | Passive nominal subject | **SUBTYPE**: Subject in passive construction. Example: **书**被[借]走了 |
| **nummod** | Numeric modifier | Number modifying noun. Example: **三**个好[警察], **五**[天] |
| **obj** | Object | Direct object of verb. Example: [开]瓶**酒**, [给]**他**两本书 |
| **obl** | Oblique nominal | Oblique argument/adjunct. Example: [还]车子给**我们**, 比**他们**更早[达到]公司 |
| **obl:agent** | Oblique agent | **SUBTYPE**: Agent in passive (introduced by 被, 由, etc.). Example: 被**他**[打] |
| **obl:patient** | Oblique patient | **CHINESE-SPECIFIC SUBTYPE**: Patient in bǎ-construction. Example: 把**书**[印]出来 |
| **orphan** | Orphan | Promotion in gapping constructions. Used when head is elided in coordination |
| **parataxis** | Parataxis | Relation between coordinated/juxtaposed clauses. Example: 他[來]了，我很**高兴** |
| **punct** | Punctuation | All punctuation marks. Example: **，**、**。**、**！**、**？** |
| **reparandum** | Reparandum | Disfluency/correction in speech. Overridden/corrected word |
| **vocative** | Vocative | Addressee/call. Example: 你[放心]吧，**校长** |
| **xcomp** | Open clausal complement | Predicative/infinitive complement. Example: [打算]**去**, [要求]**改进** |
"""

ZH_UD_EXAMPLE = """"### Example 1:

**Text**: "他是一个好学生。"

**Output JSON**:
[
    {{'token': '他', 'head': '是', 'rel':'nsubj', 'desc': 'Nominal subject'}},
    {{'token': '是', 'head': '学生', 'rel':'cop', 'desc': 'Copula'}},
    {{'token': '一', 'head': '学生', 'rel':'nummod', 'desc': 'Numeric modifier'}},
    {{'token': '个', 'head': '一', 'rel':'clf', 'desc': 'Classifier'}},
    {{'token': '好', 'head': '学生', 'rel':'amod', 'desc': 'Root of sentence'}},
    {{'token': '学生', 'head': 'ROOT', 'rel':'root', 'desc': 'Adjectival modifier'}},
    {{'token': '。', 'head': '学生', 'rel':'punct', 'desc': 'Punctuation'}},
]

### Example 2:

**Text**: "他把书放在桌子上。"

**Output JSON**:
[
    {{'token': '他', 'head': '放', 'rel':'nsubj', 'desc': 'Nominal subject'}},
    {{'token': '把', 'head': '书', 'rel':'case', 'desc': 'Case marking'}},
    {{'token': '书', 'head': '放', 'rel':'obl:patient', 'desc': 'Oblique patient'}},
    {{'token': '放', 'head': 'ROOT', 'rel':'root', 'desc': 'Root of sentence'}},
    {{'token': '在', 'head': '桌子', 'rel':'case', 'desc': 'Case marking'}},
    {{'token': '桌子', 'head': '放', 'rel':'obl', 'desc': 'Oblique nominal'}},
    {{'token': '上', 'head': '桌子', 'rel':'case:loc', 'desc': 'Postpositional localizer'}},
    {{'token': '。', 'head': '放', 'rel':'punct', 'desc': 'Punctuation'}},
]

### Example 3:

**Text**: "前面有三个人，一个是学生，两个是老师。"
**Output JSON**:
[
    {{'token': '前面', 'head': '有', 'rel':'nsubj', 'desc': 'Nominal subject'}},
    {{'token': '有', 'head': 'ROOT', 'rel':'root', 'desc': 'Root of sentence'}},
    {{'token': '三', 'head': '人', 'rel':'nummod', 'desc': 'Numeric modifier'}},
    {{'token': '个', 'head': '三', 'rel':'clf', 'desc': 'Classifier'}},
    {{'token': '人', 'head': '有', 'rel':'obj', 'desc': 'Object'}},
    {{'token': '，', 'head': '有', 'rel':'punct', 'desc': 'Punctuation'}},
    {{'token': '一', 'head': '个', 'rel':'nummod', 'desc': 'Numeric modifier'}},
    {{'token': '个', 'head': '学生', 'rel':'nsubj', 'desc': 'Nominal subject'}},
    {{'token': '是', 'head': '学生', 'rel':'cop', 'desc': 'Copula'}},
    {{'token': '学生', 'head': '有', 'rel':parataxis', 'desc': 'Parataxis'}},
    {{'token': '，', 'head': '学生', 'rel':'punct', 'desc': 'Punctuation'}},
    {{'token': '两', 'head': '个', 'rel':'nummod', 'desc': 'Numeric modifier'}},
    {{'token': '个', 'head': '老师', 'rel':'nsubj', 'desc': 'Nominal subject'}},
    {{'token': '是', 'head': '老师', 'rel':'cop', 'desc': 'Copula'}},
    {{'token': '老师', 'head': '有', 'rel':parataxis', 'desc': 'Parataxis'}},
    {{'token': '。', 'head': '有', 'rel':'punct', 'desc': 'Punctuation'}},
]

### Example 4:

**Text**: "门前站着几个工人。"

**Output JSON**:
[
    {{'token': '门前', 'head': '站', 'rel':'obl', 'desc': 'Oblique nominal'}},
    {{'token': '站', 'head': 'ROOT', 'rel':'root', 'desc': 'Root of sentence'}},
    {{'token': '着', 'head': '站', 'rel':'aux', 'desc': 'Numeric modifier'}},
    {{'token': '几', 'head': '工人', 'rel': 'nummod', 'desc': 'Numeric modifier'}},
    {{'token': '个', 'head': '几', 'rel':'clf', 'desc': 'Classifier'}},
    {{'token': '工人', 'head': '站', 'rel':'nsubj', 'desc': 'Nominal subject'}},
    {{'token': '。', 'head': '站', 'rel':'punct', 'desc': 'Punctuation'}},
]

### Example 5:

**Text**: "我们帮他考试。"

**Output JSON**:
[
    {{'token': '我们', 'head': '帮', 'rel':'nsubj', 'desc': 'Nominal subject'}},
    {{'token': '帮', 'head': 'ROOT', 'rel':'root', 'desc': 'Root of sentence'}},
    {{'token': '他', 'head': '帮', 'rel':'obj', 'desc': 'Object'}},
    {{'token': '考试', 'head': '帮', 'rel': 'xcomp', 'desc': 'Open clausal complement'}},
    {{'token': '。', 'head': '帮', 'rel':'punct', 'desc': 'Punctuation'}},
]

### Example 6:

**Text**: "我知道他考试了。"

**Output JSON**:
[
    {{'token': '我', 'head': '知道', 'rel':'nsubj', 'desc': 'Nominal subject'}},
    {{'token': '知道', 'head': 'ROOT', 'rel':'root', 'desc': 'Root of sentence'}},
    {{'token': '他', 'head': '考试', 'rel':'nsubj', 'desc': ''Nominal subject'}},
    {{'token': '考试', 'head': '知道', 'rel': 'ccomp', 'desc': 'Clausal complement'}},
    {{'token': '了', 'head': '考试', 'rel':'discourse:sp', 'desc': 'Sentence-final particle'}},
    {{'token': '。', 'head': '知道', 'rel':'punct', 'desc': 'Punctuation'}},
]

### Example 7:

**Text**: "靠近学校的商店里，出售各种文具。"

**Output JSON**:
[
    {{'token': '靠近', 'head': '商店', 'rel':'acl', 'desc': 'Clausal modifier of noun'}},
    {{'token': '学校', 'head': '靠近', 'rel':'obj', 'desc': 'Object'}},
    {{'token': '的', 'head': '靠近', 'rel':'mark', 'desc': 'Marker'}},
    {{'token': '商店', 'head': '出售', 'rel': 'nsubj', 'desc': 'Nominal subject}},
    {{'token': '里', 'head': '商店', 'rel':'case:loc', 'desc': 'Postpositional localizer '}},
    {{'token': '，', 'head': '出售', 'rel':'punct', 'desc': 'Punctuation'}},
    {{'token': '出售', 'head': 'ROOT', 'rel':'root', 'desc': 'Root of sentence'}},
    {{'token': '各种', 'head': '文具', 'rel':'det', 'desc': 'Determiner'}},
    {{'token': '文具', 'head': '出售', 'rel': 'obj', 'desc': 'Object'}},
    {{'token': '。', 'head': '出售', 'rel':'punct', 'desc': 'Punctuation'}},
]

### Example 8:

**Text**: "他哭累了。"

**Output JSON**:
[
    {{'token': '他', 'head': '哭', 'rel':'nsubj', 'desc': 'Nominal subject'}},
    {{'token': '哭', 'head': 'ROOT', 'rel':'root', 'desc': 'Root of sentence'}},
    {{'token': '累', 'head': '哭', 'rel':'compound:vv', 'desc': 'Verb-verb compound'}},
    {{'token': '了', 'head': '累', 'rel': 'discourse:sp', 'desc': 'Sentence-final particle}},
    {{'token': '。', 'head': '哭', 'rel':'punct', 'desc': 'Punctuation'}},
]
"""
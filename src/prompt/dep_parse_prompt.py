# LLM Dependency Parsing Prompt Template
# Placeholders: lang, scheme, deprel, example, text

PROMPT = """You are a professional corpus linguist specialized in dependency parsing.

Your task is to annotate {lang} text following the annotation scheme of {scheme}.
First segment the given text into tokens. Then assign the head token and dependency relation to each token.

## 1. ANNOTATION RULES

**YOU MUST**:
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

Annotate the following text. Tag each token following ALL the rules above.

**Text**: {text}

**Output JSON**:
"""

# === UD 2.0 英语依存关系 ===

EN_UD_NAME = """English Universal Dependency 2.0 (UD 2.0, based on English EWT Treebank)"""

# 51 labels
# https://universaldependencies.org/u/dep/
# https://universaldependencies.org/treebanks/en_ewt/index.html
EN_UD_DEPREL = """
# English EWT Treebank Dependency Relations

| Label | Description | Explanation |
|-------|-------------|-------------|
| **root** | Root of sentence | The main predicate of the sentence with no governor. Every sentence has exactly one root. |
| **acl** | Clausal modifier of noun | A clause that modifies a noun (adjectival clause). Example: the **book** [to read], issues [to discuss] |
| **acl:relcl** | Relative clause modifier | **SUBTYPE**: Specifically marks relative clauses with explicit relativizer (that/which/who). Example: the **book** [that I read], people [who came] |
| **advcl** | Adverbial clause modifier | A clause modifying a verb/predicate as adverbial. Example: he left [because it rained], [when finished], call me |
| **advcl:relcl** | Reduced relative adverbial | **ENGLISH-SPECIFIC SUBTYPE**: Reduced relative clauses functioning adverbially. Rare construction for temporal/causal reduced relatives. |
| **advmod** | Adverbial modifier | Adverb modifying verb/adj/adverb. Example: very **good**, not **going**, extremely **fast** |
| **amod** | Adjectival modifier | Adjective modifying noun. Example: **red** car, **good** idea, **the first** time |
| **appos** | Appositional modifier | Noun phrase in apposition to another. Example: Sam, **my brother**; the CEO, **John Smith** |
| **aux** | Auxiliary | Modal/aspectual auxiliary verbs. Example: **will** go, **can** do, **has** eaten, **should** try |
| **aux:pass** | Passive auxiliary | **SUBTYPE**: Marks passive voice auxiliaries. Example: was **built**, **got** fired. Uses 'be' or 'get'. |
| **case** | Case marking | Preposition/postposition marking grammatical case. Example: **in** the house, **on** Monday, **by** car |
| **cc** | Coordinating conjunction | Conjunction linking coordinates. Example: apples **and** oranges, **or**, **but**, **nor** |
| **cc:preconj** | Preconjunct | **ENGLISH-SPECIFIC SUBTYPE**: First part of correlative conjunctions. Example: **both** ... and, **either** ... or, **neither** ... nor |
| **ccomp** | Clausal complement | Finite clause complement of verb. Example: I know [**that** he left], she said [**he** came] |
| **compound** | Compound | Multi-word expressions forming single unit. Example: **phone** book, **bus** stop, **ice** cream |
| **compound:prt** | Phrasal verb particle | **ENGLISH-SPECIFIC SUBTYPE**: Particle in phrasal verbs. Example: give **up**, look **forward** to, take **off** |
| **conj** | Conjunct | Second/subsequent conjunct in coordination. Example: apples and **oranges**, run or **walk** |
| **cop** | Copula | Copula verb (linking verb). Example: **is** a student, **was** happy, **being** ready |
| **csubj** | Clausal subject | Finite clause as subject. Example: [**What he said**] was true, [**that it rained**] surprised me |
| **csubj:outer** | Outer clause subject | **SUBTYPE**: Subject of outer clause in raising constructions. Example: **it** seems [that he left] - 'it' is outer subject |
| **csubj:pass** | Clausal passive subject | **SUBTYPE**: Clausal subject in passive. Example: [**that he lied**] was believed |
| **dep** | Unclassified dependency | Fallback relation when relation cannot be determined. Should be rare in well-annotated corpora. |
| **det** | Determiner | Articles and determiners. Example: **the** book, **a** car, **this** person, **some** ideas, **my** house |
| **det:predet** | Predeterminer | **ENGLISH-SPECIFIC SUBTYPE**: Predeterminers appearing before articles. Example: **all** the books, **both** the cars, **half** the time |
| **discourse** | Discourse element | Interjections, discourse markers, filler words. Example: **well**, I think...; **oh**, really?; **um**, maybe |
| **dislocated** | Dislocated elements | Fronted/postposed elements outside core structure. Example: **that person**, I know him; I know him, **that person** |
| **expl** | Expletive | Expletive/pleonastic pronouns with no semantic content. Example: **it** is raining, **there** is a problem |
| **fixed** | Fixed multiword expression | Fixed grammaticalized expressions. Example: **in** order **to**, **as** well **as**, **rather** than |
| **flat** | Flat multiword expression | Non-headed multiword expressions. Example: **New York**, **Joe Biden**, titles, dates |
| **goeswith** | Goes with | Marks word fragments that should be joined. Used for tokenization errors. Example: some- **thing** → something |
| **iobj** | Indirect object | Indirect object of ditransitive verb. Example: give **me** the book, tell **him** the truth |
| **list** | List | Relations in list structures. Example: items in bulleted/numbered lists, enumeration structures |
| **mark** | Marker | Subordinating conjunction/marker. Example: **if** it rains, **because** I left, **that** he came, **to** go |
| **nmod** | Nominal modifier | Noun modifying another noun (usually with preposition). Example: the destruction **of** the city, book **about** science |
| **nmod:desc** | Descriptive modifier | **ENGLISH-SPECIFIC SUBTYPE**: Descriptive nominal modifiers without preposition, typically informal. Example: age **70**, model **T**, size **large** |
| **nmod:poss** | Possessive modifier | **SUBTYPE**: Possessive/genitive nominal modifier. Example: **John's** book, the **company's** profits, **Mary's** car |
| **nmod:unmarked** | Unmarked modifier | **ENGLISH-SPECIFIC SUBTYPE**: Nominal modifier without case marking (temporal or other special cases). Example: **last year**, **this morning** |
| **nsubj** | Nominal subject | Subject of verb/clause. Example: **I** eat, **the dog** barked, **she** is happy |
| **nsubj:outer** | Outer subject | **SUBTYPE**: Subject of outer clause in raising/control. Example: **he** seems [to like it] - 'he' is also subject of 'like' |
| **nsubj:pass** | Passive nominal subject | **SUBTYPE**: Subject in passive construction. Example: the **book** was read, **she** was elected |
| **nummod** | Numeric modifier | Number modifying noun. Example: **three** books, **$5**, **first** place, **100** people |
| **obj** | Object | Direct object of verb. Example: read a **book**, eat **pizza**, see **him** |
| **obl** | Oblique nominal | Oblique argument/adjunct. Example: go **to** school, live **in** Boston, work **on** Monday |
| **obl:agent** | Oblique agent | **SUBTYPE**: Agent in passive (with 'by'). Example: written **by** Shakespeare, built **by** workers |
| **obl:unmarked** | Unmarked oblique | **ENGLISH-SPECIFIC SUBTYPE**: Oblique without preposition (typically temporal/spatial). Example: go **home**, **yesterday**, **last night** |
| **orphan** | Orphan | Promotion in gapping constructions. Used when head is elided in coordination. Example: John went to Paris and **Mary** ∅ to London |
| **parataxis** | Parataxis | Relation between coordinated/juxtaposed clauses without explicit coordination. Example: he came, I left; "go away," she said |
| **punct** | Punctuation | All punctuation marks. Example: **.**, **,**, **!**, **?**, **"**, **(**, **)** |
| **reparandum** | Reparandum | Disfluency/correction in speech or informal writing. Overridden/corrected word. Example: go to the- **to** Boston |
| **vocative** | Vocative | Addressee/call. Example: **John**, come here; **ladies and gentlemen**, welcome |
| **xcomp** | Open clausal complement | Predicative/infinitive complement without own subject. Example: want **to go**, seems **happy**, made him **leave** |
"""

EN_UD_EXAMPLE = """**Text**: "Sha Ruishan's job was to create a more detailed map of the cosmic microwave background using observational data."

**Output JSON**:
[
    {{'token': 'Sha', 'head': 'job', 'rel':'nmod:poss', 'desc': 'Possessive modifier'}},
    {{'token': 'Ruishan', 'head': 'Sha', 'rel':'flat', 'desc': 'Flat multiword expression'}},
    {{'token': "'s", 'head': 'Sha', 'rel':'case', 'desc': 'Case marking'}},
    {{'token': 'job', 'head': 'create', 'rel':'nsubj', 'desc': 'Nominal subject'}},
    {{'token': 'was', 'head': 'create', 'rel':'cop', 'desc': 'Copula'}},
    {{'token': 'to', head': 'create', 'rel':'mark', 'desc': 'Marker'}},
    {{'token': 'create', head': 'ROOT', 'rel':'root', 'desc': 'Root of sentence'}},
    {{'token': 'a', head': 'map', 'rel':'det', 'desc': 'Determiner'}},
    {{'token': 'more', head': 'detailed', 'rel':'advmod', 'desc': 'Adverbial modifier'}},
    {{'token': 'detailed', head': 'map', 'rel':'amod', 'desc': 'Adjectival modifier'}},
    {{'token': 'map', head': 'create', 'rel':'obj', 'desc': 'Object'}},
    {{'token': 'of', head': 'background', 'rel':'case', 'desc': 'Case marking'}},
    {{'token': 'the', head': 'background', 'rel':'det', 'desc': 'Determiner'}},
    {{'token': 'cosmic', head': 'background', 'rel':'amod', 'desc': 'Adjectival modifier'}},
    {{'token': 'microwave', head': 'background', 'rel':'compound', 'desc': 'Compound'}},
    {{'token': 'background', head': 'map', 'rel':'nmod', 'desc': 'Nominal modifier'}},
    {{'token': 'using', head': 'create', 'rel':'advcl', 'desc': 'Adverbial clause modifier'}},
    {{'token': 'observational', head': 'data', 'rel':'amod', 'desc': 'Adjectival modifier'}},
    {{'token': 'data', head': 'using', 'rel':'obj', 'desc': 'Object'}},
    {{'token': '.', head': 'create', 'rel':'punct', 'desc': 'punctuation'}},
]
"""

# === UD 2.0 汉语依存关系 ===

ZH_UD_NAME = """Chinese Universal Dependency 2.0 (UD 2.0, based on Chinese GSD Treebank)"""

# 46 labels
# https://universaldependencies.org/u/dep/
# https://universaldependencies.org/treebanks/zh_gsd/index.html
ZH_UD_DEPREL = """
# Chinese GSD Treebank Dependency Relations

| Label | Description | Explanation |
|-------|-------------|-------------|
| **root** | Root of sentence | The main predicate of the sentence with no governor. Every sentence has exactly one root. |
| **acl** | Clausal modifier of noun | A clause that modifies a noun (adjectival clause). 例: 我看的**书**(book [that] I read) |
| **acl:relcl** | Relative clause modifier | **CHINESE-SPECIFIC SUBTYPE**: Specifically marks relative clauses. 例: 他写的**文章**(article that he wrote). Uses 的 (de) as relativizer. |
| **advcl** | Adverbial clause modifier | A clause modifying a verb/predicate as adverbial. 例: 因为下雨，**取消**了(canceled because of rain) |
| **advmod** | Adverbial modifier | Adverb modifying verb/adj/adverb. 例: **很**好(very good), **不**去(not go) |
| **amod** | Adjectival modifier | Adjective modifying noun. 例: **红**色(red color), **好**人(good person) |
| **appos** | Appositional modifier | Noun phrase in apposition to another. 例: 李明，**校长**(Li Ming, the principal) |
| **aux** | Auxiliary | Modal/aspectual auxiliary verbs. 例: **会**说(can speak), **了**(perfective aspect) |
| **aux:pass** | Passive auxiliary | **SUBTYPE**: Marks passive voice auxiliaries. 例: **被**打(was hit). Common with 被(bèi), 为(wèi). |
| **case** | Case marking | Adposition marking case relation. 例: 在**家**(at home) - 在 marks location |
| **cc** | Coordinating conjunction | Conjunction linking coordinates. 例: 和(and), 或(or), 但(but). Example: 苹果**和**香蕉 |
| **ccomp** | Clausal complement | Finite clause complement of verb. 例: 我知道**他来了**(I know [that] he came) |
| **clf** | Classifier | **CHINESE-SPECIFIC**: Measure words/classifiers between number and noun. 例: 三**本**书(three [CL] books), 一**个**人(one [CL] person) |
| **compound** | Compound | Multi-word expressions forming single unit. 例: 火**车**(fire-vehicle = train), 电**脑**(electric-brain = computer) |
| **compound:ext** | Extent compound | **CHINESE-SPECIFIC SUBTYPE**: Extent/degree constructions with 得(de). 例: 跑**得**很快(run so fast) - links result clause to main verb |
| **conj** | Conjunct | Second/subsequent conjunct in coordination. 例: 苹果和**香蕉**(apples and bananas) |
| **cop** | Copula | Copula verb (linking verb). 例: **是**学生(is a student), **为**主席(serve as chairman) |
| **csubj** | Clausal subject | Finite clause as subject. 例: **学中文**很难([To] learn Chinese is difficult) |
| **csubj:pass** | Clausal passive subject | **SUBTYPE**: Clausal subject in passive. 例: **打人**被禁止([Hitting people] is prohibited) |
| **det** | Determiner | Articles and determiners. 例: **这**个(this [one]), **那些**人(those people), **每**天(every day) |
| **discourse** | Discourse element | Interjections, discourse markers. 例: **啊**(ah), **嗯**(um), **哦**(oh) |
| **discourse:sp** | Sentence-final particle | **CHINESE-SPECIFIC SUBTYPE**: Sentence-final particles showing mood/tone. 例: 好**吗**(good [QUE]), 是**的**(yes [SFP]), 来**吧**(come [IMP]) |
| **dislocated** | Dislocated elements | Fronted/postposed elements outside core structure. 例: **那个人**，我认识(that person, I know [him]) |
| **flat** | Flat multiword expression | Non-headed multiword expressions. For names, titles, dates |
| **flat:foreign** | Foreign flat expression | **SUBTYPE**: Foreign language expressions. 例: **New York**, **Harvard University** |
| **flat:name** | Name flat structure | **SUBTYPE**: Proper names without internal structure. 例: **李明**, **北京大学** |
| **iobj** | Indirect object | Indirect object of verb. 例: 给他**书**(give him books) - 他 would be iobj |
| **mark** | Marker | Subordinating conjunction/marker. 例: **如果**(if), **因为**(because), **虽然**(although) |
| **mark:adv** | Adverbial marker | **CHINESE-SPECIFIC SUBTYPE**: Adverbial particle 地(de) linking adverb to verb. 例: 慢慢**地**走(slowly [ADV] walk) |
| **mark:rel** | Relativizer | **CHINESE-SPECIFIC SUBTYPE**: Relative clause marker 的(de). 例: 我买**的**书(book that I bought) - 的 marks relative clause |
| **nmod** | Nominal modifier | Noun modifying another noun. 例: **学校**图书馆(school library), **中国**历史(Chinese history) |
| **nmod:tmod** | Temporal modifier | **SUBTYPE**: Temporal noun as modifier. 例: **今天**去(today go), **去年**的事(last year's matter) |
| **nsubj** | Nominal subject | Subject of verb/clause. 例: **我**吃饭(I eat), **他**是学生(he is student) |
| **nsubj:outer** | Outer subject | **SUBTYPE**: Subject of outer clause in control. 例: **他**说要来(he said [he] would come) |
| **nsubj:pass** | Passive nominal subject | **SUBTYPE**: Subject in passive construction. 例: **书**被借走了(book was borrowed) |
| **nummod** | Numeric modifier | Number modifying noun. 例: **三**个人(three people), **第一**名(first place) |
| **obj** | Object | Direct object of verb. 例: 吃**饭**(eat rice), 看**书**(read book) |
| **obl** | Oblique nominal | Oblique argument/adjunct. 例: 在**学校**学习(study at school), 用**筷子**吃(eat with chopsticks) |
| **obl:agent** | Oblique agent | **SUBTYPE**: Agent in passive (introduced by 被, 由, etc.). 例: 被**他**打(hit by him) |
| **obl:patient** | Oblique patient | **CHINESE-SPECIFIC SUBTYPE**: Patient in bǎ-construction. 例: 把**书**借走(BA book borrow = borrow the book) |
| **orphan** | Orphan | Promotion in gapping constructions. Used when head is elided in coordination |
| **parataxis** | Parataxis | Relation between coordinated/juxtaposed clauses. 例: 他來了，我很高兴(He came, I'm happy) |
| **punct** | Punctuation | All punctuation marks. 例: **，**、**。**、**！**、**？** |
| **reparandum** | Reparandum | Disfluency/correction in speech. Overridden/corrected word |
| **vocative** | Vocative | Addressee/call. 例: **老师**，请问(Teacher, may I ask) |
| **xcomp** | Open clausal complement | Predicative/infinitive complement. 例: 打算**去**(plan to go), 要求**改进**(demand to improve) |
"""

ZH_UD_EXAMPLE = """"**Text**: "沙瑞山的工作就是根据卫星观测数据，重新绘制一幅更精确的全宇宙微波辐射背景图。"

**Output JSON**:
[
    {{'token': '沙瑞山', 'head': '工作', 'rel':'nmod', 'desc': 'Nominal modifier'}},
    {{'token': '的', 'head': '沙瑞山', 'rel':'case', 'desc': 'Case marking'}},
    {{'token': '工作', 'head': '是', 'rel':'nsubj', 'desc': 'Nominal subject'}},
    {{'token': '就', 'head': '是', 'rel':'advmod', 'desc': 'Adverbial modifier'}},
    {{'token': '是', 'head': 'ROOT', 'rel':'root', 'desc': 'Root of sentence'}},
    {{'token': '根据', 'head': '数据', 'rel':'case', 'desc': 'Case marking'}},
    {{'token': '卫星', 'head': '数据', 'rel':'nmod', 'desc': 'Nominal modifier'}},
    {{'token': '观测', 'head': '数据', 'rel':'nmod', 'desc': 'Nominal modifier'}},
    {{'token': '数据', 'head': '绘制', 'rel':'obl', 'desc': 'Oblique nominal'}},
    {{'token': '，', 'head': '绘制', 'rel':'punct', 'desc': 'Punctuation'}},
    {{'token': '重新', 'head': '绘制', 'rel':'advmod', 'desc': 'Adverbial modifier'}},
    {{'token': '绘制', 'head': '是', 'rel':'xcomp', 'desc': 'Open clausal complement'}},
    {{'token': '一', 'head': '幅', 'rel':'nummod', 'desc': 'Numeric modifier'}},
    {{'token': '幅', 'head': '图', 'rel':'clf', 'desc': 'Classifier'}},
    {{'token': '更', 'head': '精确', 'rel':'advmod', 'desc': 'Adverbial modifier'}},
    {{'token': '精确', 'head': '图', 'rel':'amod', 'desc': 'Adjectival modifier'}},
    {{'token': '的', 'head': '精确', 'rel':'mark:rel', 'desc': 'Relativizer'}},
    {{'token': '全', 'head': '宇宙', 'rel':'det', 'desc': 'Determiner'}},
    {{'token': '宇宙', 'head': '图', 'rel':'nmod', 'desc': 'Nominal modifier'}},
    {{'token': '微波', 'head': '图', 'rel':'nmod', 'desc': 'Nominal modifier'}},
    {{'token': '辐射', 'head': '图', 'rel':'nmod', 'desc': 'Nominal modifier'}},
    {{'token': '背景', 'head': '图', 'rel':'compound', 'desc': 'Compound'}},
    {{'token': '图', 'head': '绘制', 'rel':'obj', 'desc': 'Object'}},
    {{'token': '。', 'head': '是', 'rel':'punct', 'desc': 'Punctuation'}},
]
"""

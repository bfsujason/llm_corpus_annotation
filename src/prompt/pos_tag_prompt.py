# LLM POS Tagging Prompt Template
# Placeholders: lang, scheme, tagset, example, text

PROMPT = """You are a professional corpus linguist specialized in Part-of-Speech (POS) tagging.

Your task is to annotate {lang} text following the annotation scheme of {scheme}.
First segment the given text into tokens. Then assign a POS tag to each token.

## 1. ANNOTATION RULES

**YOU MUST**:
- Tag each token individually by DEFAULT
- Ensure every token is covered in your output

## 2. THE COMPLETE TAGSET

{tagset}

## 3. OUTPUT FORMAT

Return a JSON list. Each object must contain:

- `token`: The individual token.
- `tag`: The POS tag code for that token.
- `desc`: The description of that tag from the reference table.

## 4. EXAMPLE

{example}

---

**YOUR TASK**:

Annotate the following text. Tag each token following ALL the rules above.

**Text**: {text}

**Output JSON**:
"""

# === PTB 英语词性赋码集 ===

EN_PTB_NAME = """Spacy's Penn Treebank (PTB) POS Tagset"""

# 45 + 6 tags (with Spacy's extension)
# https://catalog.ldc.upenn.edu/docs/LDC99T42/tagguid1.pdf
# https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
# https://spacy.io/models/en#en_core_web_trf
# https://github.com/explosion/spaCy/blob/master/spacy/glossary.py

EN_PTB_TAGSET = """
| Label | Description | Explanation | Tag Type |
|-------|-------------|-------------|----------|
| **$** | Dollar sign | Currency symbol, also used for other currency symbols. Functions to mark monetary values. | Punctuation (PTB) |
| **''** | Closing quotation mark | Right/closing double quote. Functions to mark the end of quoted material. | Punctuation (PTB) |
| **,** | Comma | Punctuation mark for separation. Functions to separate clauses, list items, or other sentence elements. | Punctuation (PTB) |
| **-LRB-** | Left round bracket | Escaped left parenthesis "(" in PTB format. Functions to group or set apart supplementary information. | Punctuation (PTB) |
| **-RRB-** | Right round bracket | Escaped right parenthesis ")" in PTB format. Functions to close parenthetical expressions. | Punctuation (PTB) |
| **.** | Sentence terminator | Period, exclamation point, or question mark ending a sentence. Functions to mark sentence boundaries. | Punctuation (PTB) |
| **:** | Colon or ellipsis | Colon, semicolon, or ellipsis (...). Functions to introduce lists, separate clauses, or indicate pauses. | Punctuation (PTB) |
| **``** | Opening quotation mark | Left/opening double quote. Functions to mark the beginning of quoted material. | Punctuation (PTB) |
| **#** | Pound sign | Hash symbol. Functions to mark numbers, social media hashtags, or other special uses. | Punctuation (PTB) |
| **ADD** | Email or web address | Email addresses, URLs, and other internet-specific additions. Functions to identify non-standard textual elements in web/biomedical corpora. | **Spacy Extension** |
| **AFX** | Affix | Bound morphological prefix or suffix that doesn't exist as free-standing word (e.g., "non-", "pre-", "anti-" when separated by hyphen). Functions to mark morphological units in tokenized compounds. | **Spacy Extension** |
| **CC** | Coordinating conjunction | Conjunctions connecting elements of equal grammatical rank. Functions to join words, phrases, or clauses (e.g., *and*, *but*, *or*, *yet*). | Core PTB (36) |
| **CD** | Cardinal number | Numerical values, including integers, decimals, fractions. Functions to express quantity or numerical order (e.g., *one*, *1*, *2.5*, *million*). | Core PTB (36) |
| **DT** | Determiner | Articles and determiners that introduce and specify nouns. Functions to express definiteness, specificity, or quantity (e.g., *the*, *a*, *an*, *this*, *these*, *some*). | Core PTB (36) |
| **EX** | Existential "there" | The word "there" when used as expletive subject. Functions as placeholder subject in existential constructions (e.g., "There is a problem"). | Core PTB (36) |
| **FW** | Foreign word | Words from other languages not assimilated into English. Functions to mark non-English vocabulary (e.g., *bon vivant*, *zeitgeist*). | Core PTB (36) |
| **HYPH** | Hyphen | Hyphen character when tokenized separately. Functions to connect compound words or mark line breaks; used when hyphens are split from surrounding text in modern tokenization. | **Spacy Extension** |
| **IN** | Preposition or subordinating conjunction | Prepositions and subordinating conjunctions. Functions to show spatial/temporal relationships or introduce subordinate clauses (e.g., *in*, *of*, *because*, *although*, *while*). | Core PTB (36) |
| **JJ** | Adjective | Base form adjective modifying nouns. Functions to describe qualities or attributes (e.g., *big*, *red*, *happy*, *old*). | Core PTB (36) |
| **JJR** | Adjective, comparative | Comparative form of adjective. Functions to compare two entities (e.g., *bigger*, *better*, *more interesting*). | Core PTB (36) |
| **JJS** | Adjective, superlative | Superlative form of adjective. Functions to compare three or more entities, indicating the extreme (e.g., *biggest*, *best*, *most interesting*). | Core PTB (36) |
| **LS** | List item marker | Symbols or numbers used as list markers. Functions to enumerate items in lists (e.g., *1.*, *a)*, *(i)*). | Core PTB (36) |
| **MD** | Modal auxiliary | Modal verbs expressing modality. Functions to indicate possibility, necessity, ability, permission (e.g., *can*, *could*, *will*, *would*, *should*, *must*, *may*, *might*). | Core PTB (36) |
| **NFP** | Superfluous punctuation | Non-standard or excessive punctuation often found in informal web text. Functions to mark unusual punctuation patterns (e.g., *!!!*, *???*, emoticons in some contexts). | **Spacy Extension** |
| **NN** | Noun, singular or mass | Common noun in singular form or mass noun. Functions as head of noun phrases for general entities or uncountable substances (e.g., *dog*, *city*, *water*, *information*). | Core PTB (36) |
| **NNP** | Proper noun, singular | Singular proper noun naming specific entities. Functions to identify particular individuals, places, organizations (e.g., *Mary*, *London*, *Microsoft*). | Core PTB (36) |
| **NNPS** | Proper noun, plural | Plural proper noun. Functions to name specific entities in plural form (e.g., *Americas*, *Smiths*, *Rockies*). | Core PTB (36) |
| **NNS** | Noun, plural | Common noun in plural form. Functions to refer to multiple instances of entities (e.g., *dogs*, *cities*, *ideas*). | Core PTB (36) |
| **PDT** | Predeterminer | Determiners that precede other determiners. Functions to modify the entire noun phrase before the main determiner (e.g., *all*, *both*, *half*, *such* in "all the people"). | Core PTB (36) |
| **POS** | Possessive ending | Possessive marker "'s" or apostrophe. Functions to indicate possession or relationship (e.g., *John's*, *students'*). | Core PTB (36) |
| **PRP** | Personal pronoun | Subject and object pronouns. Functions to substitute for noun phrases and refer to entities (e.g., *I*, *you*, *he*, *she*, *it*, *we*, *they*, *me*, *him*, *her*, *us*, *them*). | Core PTB (36) |
| **PRP$** | Possessive pronoun | Possessive pronouns used as determiners. Functions to show ownership (e.g., *my*, *your*, *his*, *her*, *its*, *our*, *their*). | Core PTB (36) |
| **RB** | Adverb | Base form adverb modifying verbs, adjectives, or other adverbs. Functions to express manner, time, place, degree (e.g., *quickly*, *very*, *here*, *never*, *almost*). | Core PTB (36) |
| **RBR** | Adverb, comparative | Comparative form of adverb. Functions to compare actions or qualities (e.g., *faster*, *better*, *more quickly*). | Core PTB (36) |
| **RBS** | Adverb, superlative | Superlative form of adverb. Functions to indicate the extreme in comparing actions (e.g., *fastest*, *best*, *most quickly*). | Core PTB (36) |
| **RP** | Particle | Verbal particle in phrasal verbs. Functions as part of multiword verbs, changing the verb's meaning (e.g., *up* in "look up", *out* in "figure out"). | Core PTB (36) |
| **SYM** | Symbol | Mathematical, scientific, or other non-punctuation symbols. Functions to represent concepts, operations, or special notations (e.g., *+*, *%*, *&*, *@*, *§*, mathematical symbols). | Core PTB (36) |
| **TO** | Infinitival "to" | The word "to" when used as infinitive marker. Functions to introduce infinitive verb forms (e.g., "I want to go"). | Core PTB (36) |
| **UH** | Interjection | Exclamations and interjections expressing emotion. Functions as standalone expressions of feeling or reaction (e.g., *oh*, *wow*, *ouch*, *uh*, *hmm*, *hello*). | Core PTB (36) |
| **VB** | Verb, base form | Base/infinitive form of verb. Functions as bare infinitive or imperative (e.g., *go*, *be*, *run* in "I can go"). | Core PTB (36) |
| **VBD** | Verb, past tense | Simple past tense form. Functions to express past actions or states (e.g., *went*, *was*, *ran*, *thought*). | Core PTB (36) |
| **VBG** | Verb, gerund/present participle | -ing form of verb. Functions as gerund (noun) or present participle (progressive aspect, adjectival use) (e.g., *going*, *being*, *running*). | Core PTB (36) |
| **VBN** | Verb, past participle | Past participle form. Functions in perfect tenses, passive voice, or as adjective (e.g., *gone*, *been*, *run*, *thought*). | Core PTB (36) |
| **VBP** | Verb, non-3rd person singular present | Present tense for non-third-person subjects. Functions to express current action/state (e.g., *go*, *are*, *think* with I/you/we/they). | Core PTB (36) |
| **VBZ** | Verb, 3rd person singular present | Present tense for third-person singular subjects. Functions to express current action/state (e.g., *goes*, *is*, *thinks* with he/she/it). | Core PTB (36) |
| **WDT** | Wh-determiner | Wh-words functioning as determiners. Functions to introduce relative clauses or questions (e.g., *which*, *that*, *what* in "which book"). | Core PTB (36) |
| **WP** | Wh-pronoun | Wh-pronouns for questions and relative clauses. Functions to introduce interrogatives or relative clauses (e.g., *who*, *whom*, *what*, *that* when used as pronoun). | Core PTB (36) |
| **WP$** | Possessive wh-pronoun | Possessive form of wh-pronoun. Functions in questions about possession (e.g., *whose*). | Core PTB (36) |
| **WRB** | Wh-adverb | Wh-words functioning as adverbs. Functions to introduce questions or relative clauses about manner, time, place, reason (e.g., *where*, *when*, *why*, *how*). | Core PTB (36) |
| **XX** | Unknown | Token of unclear or unknown category. Functions as catch-all for items that cannot be confidently assigned to other categories; also used for some typos or malformed text. | **Spacy Extension** |
| **_SP** | Space token | Represents whitespace or space characters. Functions to explicitly mark spacing in Spacy's tokenization; internal Spacy tag not standard in PTB. | **Spacy Extension** |
"""

EN_PTB_EXAMPLE = """**Text**: "Sha Ruishan's job was to create a more detailed map of the cosmic microwave background using observational data."

**Output JSON**:
[
    {{'token': 'Sha', 'tag': 'NNP', 'desc': 'Proper noun, singular'}},
    {{'token': 'Ruishan', 'tag': 'NNP', 'desc': 'Proper noun, singular'}},
    {{'token': "'s", 'tag': 'POS', 'desc': 'Possessive ending'}},
    {{'token': 'job', 'tag': 'NN', 'desc': 'Noun, singular or mass'}},
    {{'token': 'was', 'tag': 'VBD', 'desc': 'Verb, past tense'}},
    {{'token': 'to', 'tag': 'TO', 'desc': 'Infinitival "to"'}},
    {{'token': 'create', 'tag': 'VB', 'desc': 'Verb, base form'}},
    {{'token': 'a', 'tag': 'DT', 'desc': 'Determiner'}},
    {{'token': 'more', 'tag': 'RBR', 'desc': 'Adverb, comparative'}},
    {{'token': 'detailed', 'tag': 'JJ', 'desc': 'Adjective'}},
    {{'token': 'map', 'tag': 'NN', 'desc': 'Noun, singular or mass'}},
    {{'token': 'of', 'tag': 'IN', 'desc': 'Preposition or subordinating conjunction'}},
    {{'token': 'the', 'tag': 'DT', 'desc': 'Determiner'}},
    {{'token': 'cosmic', 'tag': 'JJ', 'desc': 'Adjective'}},
    {{'token': 'microwave', 'tag': 'NN', 'desc': 'Noun, singular or mass'}},
    {{'token': 'background', 'tag': 'NN', 'desc': 'Noun, singular or mass'}},
    {{'token': 'using', 'tag': 'VBG', 'desc': 'Verb, gerund/present participle'}},
    {{'token': 'observational', 'tag': 'JJ', 'desc': 'Adjective'}},
    {{'token': 'data', 'tag': 'NNS', 'desc': 'Proper noun, plural'}},
    {{'token': '.', 'tag': '.', 'desc': 'Sentence terminator'}},
]
"""

# === UD 英语词性赋码集 ===

EN_UD_NAME = """Universal POS Tagset"""

# 17 tags
# https://universaldependencies.org/u/pos/index.html
# https://github.com/explosion/spaCy/blob/master/spacy/glossary.py
# https://github.com/hankcs/HanLP/blob/ddb1299bddff079e447af52ec12549c50636bfa8/docs/annotations/pos/ud.md

EN_UD_TAGSET = """
| Label | Description | Explanation |
|-------|-------------|-------------|
| **ADJ** | Adjective | Words that modify nouns, describing qualities, quantities, or states. Functions to provide additional information about entities (e.g., *big*, *red*, *happy*). |
| **ADP** | Adposition | Covers prepositions and postpositions that express spatial or temporal relations. Functions to show relationships between words, typically governing nouns or pronouns (e.g., *in*, *on*, *at*, *from*). |
| **ADV** | Adverb | Words that modify verbs, adjectives, or other adverbs. Functions to express manner, time, place, degree, or frequency (e.g., *quickly*, *very*, *here*, *often*). |
| **AUX** | Auxiliary verb | Helping verbs that accompany main verbs to form tenses, moods, or voice. Functions to express grammatical distinctions like tense, aspect, modality, or voice (e.g., *be*, *have*, *will*, *can*, *must*). |
| **CCONJ** | Coordinating conjunction | Words that connect elements of equal grammatical rank. Functions to join words, phrases, or clauses in a non-subordinate relationship (e.g., *and*, *or*, *but*). |
| **DET** | Determiner | Words that introduce and specify nouns. Functions to express reference, quantity, or definiteness of nouns (e.g., *the*, *a*, *this*, *some*, *every*). |
| **INTJ** | Interjection | Words used to express emotion or sudden feeling. Functions as standalone expressions or exclamations, often loosely connected to the sentence structure (e.g., *oh*, *wow*, *ouch*, *hello*). |
| **NOUN** | Noun | Words that denote common entities, objects, concepts, or ideas. Functions as the head of noun phrases, typically referring to general classes of things (e.g., *dog*, *city*, *happiness*). |
| **NUM** | Numeral | Words expressing numbers or numerical quantities. Functions to quantify or order entities, including cardinal and ordinal numbers (e.g., *one*, *two*, *first*, *dozen*). |
| **PART** | Particle | Function words that don't fit other categories, often with grammatical rather than lexical meaning. Functions to express grammatical relationships or modify meaning, including infinitive markers and verbal particles (e.g., *to*, *not*, *up* in phrasal verbs). |
| **PRON** | Pronoun | Words that substitute for nouns or noun phrases. Functions to refer to entities without repeating the noun, including personal, possessive, reflexive, and relative pronouns (e.g., *he*, *they*, *mine*, *who*). |
| **PROPN** | Proper noun | Words that name specific individuals, places, organizations, or unique entities. Functions to identify particular instances rather than general classes, typically capitalized (e.g., *London*, *Mary*, *Microsoft*). |
| **PUNCT** | Punctuation | Non-alphabetic symbols used in writing. Functions to structure text, indicate pauses, separate elements, or convey intonation (e.g., *,* *.* *?* *!* *;*). |
| **SCONJ** | Subordinating conjunction | Words that introduce subordinate clauses. Functions to create hierarchical relationships between clauses, marking dependency (e.g., *because*, *although*, *if*, *that*, *when*). |
| **SYM** | Symbol | Non-punctuation symbols with specific meanings. Functions to represent concepts, mathematical operations, currencies, or special notations (e.g., *$*, *%*, *+*, *@*, *§*). |
| **VERB** | Verb | Words that express actions, events, or states. Functions as the main predicate of a clause, conveying what happens or exists (e.g., *run*, *think*, *is*, *become*). |
| **X** | Other | Words that cannot be assigned to other categories. Functions as a catch-all for foreign words, typos, unclear elements, or language-specific items that don't fit standard categories. |
"""

EN_UD_EXAMPLE = """"**Text**: "Sha Ruishan's job was to create a more detailed map of the cosmic microwave background using observational data."

**Output JSON**:
[
    {{'token': 'Sha', 'tag': 'PROPN', 'desc': 'Proper noun'}},
    {{'token': 'Ruishan', 'tag': 'PROPN', 'desc': 'Proper noun'}},
    {{'token': "'s", 'tag': 'PART', 'desc': 'Particle'}},
    {{'token': 'job', 'tag': 'NOUN', 'desc': 'Noun'}},
    {{'token': 'was', 'tag': 'AUX', 'desc': 'Auxiliary verb'}},
    {{'token': 'to', 'tag': 'PART', 'desc': 'Particle'}},
    {{'token': 'create', 'tag': 'VERB', 'desc': 'Verb'}},
    {{'token': 'a', 'tag': 'DET', 'desc': 'Determiner'}},
    {{'token': 'more', 'tag': 'ADV', 'desc': 'Adverb'}},
    {{'token': 'detailed', 'tag': 'ADJ', 'desc': 'Adjective'}},
    {{'token': 'map', 'tag': 'NOUN', 'desc': 'Noun'}},
    {{'token': 'of', 'tag': 'ADP', 'desc': 'Adposition'}},
    {{'token': 'the', 'tag': 'DET', 'desc': 'Determiner'}},
    {{'token': 'cosmic', 'tag': 'ADJ', 'desc': 'Adjective'}},
    {{'token': 'microwave', 'tag': 'NOUN', 'desc': 'Noun'}},
    {{'token': 'background', 'tag': 'NOUN', 'desc': 'Noun'}},
    {{'token': 'using', 'tag': 'VERB', 'desc': 'Verb'}},
    {{'token': 'observational', 'tag': 'ADJ', 'desc': 'Adjective'}},
    {{'token': 'data', 'tag': 'NOUN', 'desc': 'Noun'}},
    {{'token': '.', 'tag': 'PUNCT', 'desc': 'Punctuation'}},
]
"""

# === CLAWS 英语词性赋码集 ===

EN_CLAWS_NAME = """UCREL's CLAWS7 POS Tagset"""

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

**Note on "Ditto Tags"**:
Any tag can be modified with two digits (e.g., DD21, DD22) to indicate multi-word sequences treated as single grammatical units. The first digit shows the total words in the sequence, the second shows the position within it (e.g., "in terms of" → in_II31 terms_II32 of_II33).

**Note on punctuation**:
The tag for punctuation is the punctuation itself. For example, the tag for ',' is still ','.
"""

EN_CLAWS_EXAMPLE = """"**Text**: "Sha Ruishan's job was to create a more detailed map of the cosmic microwave background using observational data."

**Output JSON**:
[
    {{'token': 'Sha', 'tag': 'NP1', 'desc': 'Singular proper noun'}},
    {{'token': 'Ruishan', 'tag': 'NP1', 'desc': 'Singular proper noun'}},
    {{'token': "'s", 'tag': 'GE', 'desc': 'Germanic genitive marker'}},
    {{'token': 'job', 'tag': 'NN1', 'desc': 'Singular common noun'}},
    {{'token': 'was', 'tag': 'VBDZ', 'desc': 'Was'}},
    {{'token': 'to', 'tag': 'TO', 'desc': 'Infinitive marker'}},
    {{'token': 'create', 'tag': 'VVI', 'desc': 'Infinitive of lexical verb'}},
    {{'token': 'a', 'tag': 'AT1', 'desc': 'Singular article'}},
    {{'token': 'more', 'tag': 'RGR', 'desc': 'Comparative degree adverb'}},
    {{'token': 'detailed', 'tag': 'JJ', 'desc': 'General adjective'}},
    {{'token': 'map', 'tag': 'NN1', 'desc': 'Singular common noun'}},
    {{'token': 'of', 'tag': 'IO', 'desc': 'Of (preposition)'}},
    {{'token': 'the', 'tag': 'AT', 'desc': 'Article'}},
    {{'token': 'cosmic', 'tag': 'JJ', 'desc': 'General adjective'}},
    {{'token': 'microwave', 'tag': 'NN1', 'desc': 'Singular common noun'}},
    {{'token': 'background', 'tag': 'NN1', 'desc': 'Singular common noun'}},
    {{'token': 'using', 'tag': 'VVG', 'desc': '-ing participle of lexical verb'}},
    {{'token': 'observational', 'tag': 'JJ', 'desc': 'General adjective'}},
    {{'token': 'data', 'tag': 'NN', 'desc': 'Common noun (neutral for number)'}},
    {{'token': '.', 'tag': '.', 'desc': 'Punctuation'}},
]
"""

# === CTB 汉语词性赋码集 ===

ZH_CTB_NAME = """HanLP's Penn Chinese Treebank (CTB) POS Tagset"""

# 33 + 4 tags (with HanLP's extension)
# https://catalog.ldc.upenn.edu/docs/LDC2010T07/ctb-posguide.pdf
# https://github.com/hankcs/HanLP/blob/ddb1299bddff079e447af52ec12549c50636bfa8/docs/annotations/pos/ctb.md

ZH_CTB_TAGSET = """
| Label | Description | Explanation | Tag Origin |
|-------|-------------|-------------|------------|
| **AD** | Adverb | Modifies verbs, adjectives, or other adverbs to express manner, degree, time, or frequency. Functions as sentence or VP-level modifier (e.g., 也 "also", 很 "very", 仍然 "still", 大大 "greatly"). | Original CTB (33) |
| **AS** | Aspect marker | Grammatical particles indicating aspect of verbs. Functions to mark perfective (了), durative (着), or experiential (过) aspects. | Original CTB (33) |
| **BA** | 把 in ba-construction | The preposition 把 in disposal constructions. Functions to front the object for emphasis or disposal meaning (e.g., 把书看完 "finish reading the book"). | Original CTB (33) |
| **CC** | Coordinating conjunction | Conjunctions connecting parallel elements. Functions to join words, phrases, or clauses of equal status (e.g., 和 "and", 或 "or", 但 "but"). | Original CTB (33) |
| **CD** | Cardinal number | Numerical values and quantities. Functions to express amounts, counting, or mathematical values (e.g., 一 "one", 两 "two", 一百 "one hundred", 几 "several"). | Original CTB (33) |
| **CS** | Subordinating conjunction | Conjunctions introducing subordinate clauses. Functions to mark dependent clauses expressing condition, concession, cause, etc. (e.g., 虽然 "although", 因为 "because", 如果 "if"). | Original CTB (33) |
| **DEC** | 的 in relative clause | The particle 的 modifying nouns in relative clauses. Functions as relativizer or nominalizer (e.g., 我买的书 "the book I bought"). | Original CTB (33) |
| **DEG** | Associative 的 | The possessive/associative particle 的 showing possession or modification. Functions to link modifiers to head nouns (e.g., 我的书 "my book", 中国的文化 "Chinese culture"). | Original CTB (33) |
| **DER** | 得 in V-de construction | The particle 得 in verb-complement or result constructions. Functions to introduce degree complements or result/manner descriptions (e.g., 跑得快 "run fast", 说得对 "speak correctly"). | Original CTB (33) |
| **DEV** | 地 before VP | The particle 地 introducing adverbial modifiers before verbs. Functions to mark manner adverbials derived from adjectives (e.g., 高兴地说 "happily say", 认真地学习 "study seriously"). | Original CTB (33) |
| **DT** | Determiner | Demonstratives and determiners specifying nouns. Functions to indicate reference or specify which entity (e.g., 这 "this", 那 "that", 每 "every", 各 "each"). | Original CTB (33) |
| **ETC** | Etcetera word | Words meaning "and so on" or "et cetera". Functions to indicate incomplete lists (e.g., 等 "etc.", 等等 "and so on"). | Original CTB (33) |
| **FW** | Foreign word | Words from other languages, usually in alphabet. Functions to mark non-Chinese vocabulary, typically English letters or words (e.g., "A", "CD", "WTO"). | Original CTB (33) |
| **IJ** | Interjection | Exclamations expressing emotion or reaction. Functions as standalone utterances showing feeling or attitude (e.g., 哈哈 "haha", 哎呀 "oh my", 嗯 "mm"). | Original CTB (33) |
| **JJ** | Other noun-modifier / Adjective | Attributive adjectives modifying nouns, different from predicative use. Functions to describe noun qualities when used attributively (e.g., 新 "new" in "新书", 大 "big" in "大楼"). | Original CTB (33) |
| **LB** | 被 in long bei-construction | The preposition 被 in full passive constructions with explicit agent. Functions to mark passive voice with by-phrase (e.g., 被他打了 "was hit by him"). | Original CTB (33) |
| **LC** | Localizer | Locative particles indicating spatial or temporal position. Functions to express location or direction (e.g., 里 "inside", 上 "on/above", 中 "in/among", 前 "before/in front"). | Original CTB (33) |
| **M** | Measure word / Classifier | Classifiers used with nouns and numbers. Functions to specify countable units or categories (e.g., 个 "general classifier", 本 "book classifier", 位 "person classifier"). | Original CTB (33) |
| **MSP** | Other particle | Miscellaneous particles with grammatical functions. Functions for special grammatical purposes (e.g., 所 in nominalization constructions). | Original CTB (33) |
| **NN** | Common noun | General nouns referring to ordinary entities or concepts. Functions as heads of noun phrases for non-proper, non-temporal entities (e.g., 工作 "work", 问题 "problem", 人 "person"). | Original CTB (33) |
| **NR** | Proper noun | Names of specific people, places, and organizations. Functions to identify unique entities (e.g., 中国 "China", 北京 "Beijing", 李明 "Li Ming"). | Original CTB (33) |
| **NT** | Temporal noun | Nouns expressing time or temporal concepts. Functions to denote time points, periods, or temporal relations (e.g., 今天 "today", 目前 "currently", 以前 "before", 时候 "time/when"). | Original CTB (33) |
| **OD** | Ordinal number | Numbers indicating order or sequence. Functions to express ranking or position (e.g., 第一 "first", 第二 "second"). | Original CTB (33) |
| **ON** | Onomatopoeia | Words imitating sounds. Functions to represent auditory impressions or sound effects in text. | Original CTB (33) |
| **P** | Preposition (excluding 把 and 被) | General prepositions showing relationships. Functions to indicate location, direction, time, manner, beneficiary, etc. (e.g., 在 "at/in", 从 "from", 对 "to/toward", 为 "for"). | Original CTB (33) |
| **PN** | Pronoun | Words substituting for nouns. Functions to refer to people, things, or entities contextually (e.g., 我 "I", 你 "you", 他 "he/him", 它 "it", 这 "this", 什么 "what"). | Original CTB (33) |
| **PU** | Punctuation | Punctuation marks and symbols. Functions to structure text and indicate pauses, boundaries, or intonation (e.g., 。，、！？). | Original CTB (33) |
| **SB** | 被 in short bei-construction | The preposition 被 in short passive constructions without explicit agent. Functions to mark agentless passive voice (e.g., 被打了 "was hit"). | Original CTB (33) |
| **SP** | Sentence-final particle | Modal particles at sentence end expressing attitude or mood. Functions to indicate questions, suggestions, assertions, or speaker's stance (e.g., 吗 "question particle", 吧 "suggestion", 呢 "continuation"). | Original CTB (33) |
| **VA** | Predicative adjective | Adjectives functioning as main predicates without copula. Functions as stative verbs describing qualities or states (e.g., 好 "good/well", 高兴 "happy", 重要 "important"). | Original CTB (33) |
| **VC** | Copula | The verb 是 and related linking verbs. Functions to link subject with predicate nominal or adjective (e.g., 是 "be", 为 "be", 当作 "regard as"). | Original CTB (33) |
| **VE** | 有 as main verb | The verb 有 expressing existence or possession. Functions to indicate having or existence (e.g., 有钱 "have money", 有问题 "there's a problem"). | Original CTB (33) |
| **VV** | Other verb | General verbs not classified elsewhere. Functions as main predicates expressing actions, processes, or changes (e.g., 去 "go", 说 "say", 认为 "think", 发展 "develop"). | Original CTB (33) |
| **IC** | Incomplete component | Incomplete or fragmented words/morphemes, especially in ASR (automatic speech recognition) output. Functions to mark partial or truncated components that don't form complete linguistic units (e.g., 好xin, 那个ba). | **HanLP Extension** |
| **EM** | Emoticon or emoji | Emoticons, emoji, and other sentiment symbols. Functions to identify emotional expressions in social media and informal text (e.g., :), ^_^, 😊). | **HanLP Extension** |
| **NOI** | Noise or garbage text | Unrecognizable characters, corrupted text, or meaningless strings. Functions to mark text that should be filtered or ignored in processing (e.g., encoding errors, random characters). | **HanLP Extension** |
| **URL** | Web address / URL | Internet addresses and web links. Functions to mark URLs and web addresses in modern Chinese text (e.g., http://example.com, www.example.cn). | **HanLP Extension** |
"""

ZH_CTB_EXAMPLE = """**Text**: "沙瑞山的工作就是根据卫星观测数据，重新绘制一幅更精确的全宇宙微波辐射背景图。"

**Output JSON**:
[
    {{'token': '沙瑞山', 'tag': 'NR', 'desc': 'Proper noun'}},
    {{'token': '的', 'tag': 'DEG', 'desc': 'Associative 的'}},
    {{'token': '工作', 'tag': 'NN', 'desc': 'Common noun'}},
    {{'token': '就', 'tag': 'AD', 'desc': 'Adverb'}},
    {{'token': '是', 'tag': 'VC', 'desc': 'Copula'}},
    {{'token': '根据', 'tag': 'P', 'desc': ' Preposition (excluding 把 and 被)'}},
    {{'token': '卫星', 'tag': 'NN', 'desc': 'Common noun'}},
    {{'token': '观测', 'tag': 'NN', 'desc': 'Common noun'}},
    {{'token': '数据', 'tag': 'NN', 'desc': 'Common noun'}},
    {{'token': '，', 'tag': 'PU', 'desc': 'Punctuation'}},
    {{'token': '重新', 'tag': 'AD', 'desc': 'Adverb'}},
    {{'token': '绘制', 'tag': 'VV', 'desc': 'Other verb'}},
    {{'token': '一', 'tag': 'CD', 'desc': 'Cardinal number'}},
    {{'token': '幅', 'tag': 'M', 'desc': 'Measure word'}},
    {{'token': '更', 'tag': 'AD', 'desc': 'Adverb'}},
    {{'token': '精确', 'tag': 'VA', 'desc': 'Predicative adjective'}},
    {{'token': '的', 'tag': 'DEC', 'desc': '的 in relative clause'}},
    {{'token': '全', 'tag': 'DT', 'desc': 'Determiner'}},
    {{'token': '宇宙', 'tag': 'NN', 'desc': 'Common noun'}},
    {{'token': '微波', 'tag': 'NN', 'desc': 'Common noun'}},
    {{'token': '辐射', 'tag': 'NN', 'desc': 'Common noun'}},
    {{'token': '背景', 'tag': 'NN', 'desc': 'Common noun'}},
    {{'token': '图', 'tag': 'NN', 'desc': 'Common noun'}},
    {{'token': '。', 'tag': 'PU', 'desc': 'Punctuation'}},
]
"""

# === PKU 汉语词性赋码集 ===

ZH_PKU_NAME = """HanLP's PKU POS Tagset (北大计算语言学研究所词性标注集)"""

# 43 tags
# https://github.com/lancopku/pkuseg-python/blob/master/tags.txt
# https://github.com/hankcs/HanLP/blob/ddb1299bddff079e447af52ec12549c50636bfa8/docs/annotations/pos/pku.md

ZH_PKU_TAGSET = """
| Label | Description | Explanation | Tag Origin |
|-------|-------------|-------------|------------|
| **a** | Adjective | General adjectives describing qualities or states. Functions to modify nouns or serve as predicates (e.g., 大 "big", 好 "good", 重要 "important"). | Original PKU (26 basic) |
| **ad** | Adjective as adverbial | Adjectives functioning as adverbials. Functions to modify verbs (e.g., 积极 "actively"). | PKU detailed tag (36) |
| **Ag** | Adjectival morpheme | Bound morphemes with adjectival function. Functions as components in compound words that contribute adjectival meaning. | PKU detailed tag (36) |
| **an** | Nominal adjective | Adjectives that can function as nouns. Functions to describe entities that can stand alone as nominals. | PKU detailed tag (36) |
| **b** | Distinguishing word | Words expressing distinction or classification, often modifying nouns. Functions to differentiate categories (e.g., 大型 "large-scale", 多种 "multiple types"). | Original PKU (26 basic) |
| **Bg** | Distinguishing word morpheme | Bound morphemes with distinguishing/classification function. Functions as morphemic components for words expressing distinction or differentiation (e.g., 橙 "orange" in color words, distinguishing different categories). | PKU detailed tag (36) |
| **c** | Conjunction | Connectives linking words, phrases, or clauses. Functions to express logical relationships (e.g., 和 "and", 或者 "or", 但是 "but"). | Original PKU (26 basic) |
| **d** | Adverb | Words modifying verbs, adjectives, or other adverbs. Functions to express manner, degree, time, scope, or negation (e.g., 很 "very", 也 "also", 不 "not"). | Original PKU (26 basic) |
| **Dg** | Adverb morpheme | Bound morphemes with adverbial function. Functions as components contributing adverbial meaning in compounds. | PKU detailed tag (36) |
| **e** | Interjection | Exclamations expressing emotion or response. Functions as standalone utterances showing feeling (e.g., 啊 "ah", 哎呀 "oh my"). | Original PKU (26 basic) |
| **f** | Directional/Localizer | Direction words and location markers. Functions to indicate spatial or directional relationships (e.g., 上 "up/on", 里 "inside", 前 "front"). | Original PKU (26 basic) |
| **h** | Prefix | Prefixes attached to word beginnings. Functions to modify or specify word meaning (e.g., 第 in 第一 "first", 老 in 老师 "teacher"). | Original PKU (26 basic) |
| **i** | Idiom | Fixed idiomatic expressions and set phrases. Functions as lexical units with non-compositional meanings (e.g., 四字成语 four-character idioms). | Original PKU (26 basic) |
| **j** | Abbreviation | Shortened forms of longer expressions. Functions to represent organizations, concepts, or phrases concisely (e.g., 北大 for 北京大学). | Original PKU (26 basic) |
| **k** | Suffix | Suffixes attached to word endings. Functions to derive new words or indicate grammatical features (e.g., 性 "-ness", 化 "-ization", 们 plural marker). | Original PKU (26 basic) |
| **l** | Idiom or fixed phrase | Fixed expressions treated as units (alternative idiom tag). Functions similarly to 'i' for set expressions. | Original PKU (26 basic) |
| **m** | Numeral | Numbers and numerical expressions. Functions to express quantity or amount (e.g., 一 "one", 三 "three", 几 "several"). | Original PKU (26 basic) |
| **Mg** | Numeral morpheme | Bound morphemes with numerical meaning. Functions as numerical components in compounds. | PKU detailed tag (36) |
| **n** | Common noun | General nouns for ordinary entities and concepts. Functions as heads of noun phrases (e.g., 人 "person", 工作 "work", 国家 "country"). | Original PKU (26 basic) |
| **Ng** | Noun morpheme | Bound morphemes with nominal function. Functions as noun-like components in compounds. | PKU detailed tag (36) |
| **nr** | Personal name | Names of people. Functions to identify individuals (e.g., 张三 "Zhang San", 李明 "Li Ming"). | Original PKU (26 basic) |
| **ns** | Place name | Geographic locations and place names. Functions to identify locations (e.g., 北京 "Beijing", 中国 "China"). | Original PKU (26 basic) |
| **nt** | Organization name | Names of organizations, companies, and institutions. Functions to identify organizational entities (e.g., 联合国 "United Nations", 公司 "company"). | Original PKU (26 basic) |
| **nx** | Non-Chinese name/Transliteration | Foreign names or transliterated words. Functions to mark non-Chinese proper nouns (e.g., English names, foreign terms). | PKU detailed tag (36) |
| **nz** | Other proper noun | Proper nouns not classified as nr, ns, or nt. Functions for miscellaneous named entities and brands. | Original PKU (26 basic) |
| **o** | Onomatopoeia | Sound-imitating words. Functions to represent auditory impressions (e.g., 哈哈 "haha", 咚咚 "thump thump"). | Original PKU (26 basic) |
| **p** | Preposition | Words governing nouns to show relationships. Functions to indicate location, direction, time, or manner (e.g., 在 "at", 从 "from", 对 "to/toward"). | Original PKU (26 basic) |
| **q** | Classifier/Measure word | Classifiers used with nouns and numbers. Functions to specify countable units (e.g., 个 "general classifier", 本 "book classifier", 位 "person classifier"). | Original PKU (26 basic) |
| **r** | Pronoun | Words substituting for nouns or noun phrases. Functions to refer anaphorically or deictically (e.g., 我 "I", 你 "you", 他 "he/him", 这 "this"). | Original PKU (26 basic) |
| **Rg** | Pronominal morpheme | Bound morphemes with pronominal function. Functions as pronoun-like components in compounds. | PKU detailed tag (36) |
| **s** | Space word/Locative | Spatial words and location expressions. Functions to denote places or spaces. | Original PKU (26 basic) |
| **t** | Time word/Temporal noun | Words expressing time or temporal concepts. Functions to indicate time points or periods (e.g., 今天 "today", 现在 "now", 以前 "before"). | Original PKU (26 basic) |
| **Tg** | Temporal morpheme | Bound morphemes with temporal meaning. Functions as time-related components in compounds. | PKU detailed tag (36) |
| **u** | Auxiliary/Particle | Function words including particles and auxiliaries. Functions for grammatical purposes (e.g., 的 possessive, 地 adverbial, 得 complement marker, 着/了/过 aspect markers). | Original PKU (26 basic) |
| **v** | Verb | General verbs expressing actions, processes, or states. Functions as main predicates (e.g., 是 "be", 有 "have", 做 "do", 说 "say", 去 "go"). | Original PKU (26 basic) |
| **vd** | Verb as adverbial | Verbs directly functioning as adverbials (状语). Functions to modify other verbs, combining verbal and adverbial characteristics (e.g., 持续 in 持续好转 "continuously improve", 错 in 收错了 "mistakenly collected"). | PKU detailed tag (36) |
| **Vg** | Verb morpheme | Bound morphemes with verbal function. Functions as verb-like components in compounds. | PKU detailed tag (36) |
| **vn** | Verbal noun | Nouns derived from or related to verbs, often gerunds. Functions as nominalizations (e.g., 研究 "research", 发展 "development"). | PKU detailed tag (36) |
| **w** | Punctuation | Punctuation marks and symbols. Functions to structure text (e.g., 。，！？；：). | Original PKU (26 basic) |
| **x** | Unclassified/String | Unclassifiable items or character strings. Functions as catch-all for unclear or non-standard elements. | Original PKU (26 basic) |
| **y** | Modal particle | Sentence-final or modal particles. Functions to express mood, attitude, or questioning (e.g., 吗 "question", 吧 "suggestion", 呢 "continuation"). | Original PKU (26 basic) |
| **Yg** | Modal particle morpheme | Bound morphemes with modal particle function. Functions as morphemic components contributing modal or sentence-final particle meaning in compounds (e.g., 耳 in classical Chinese modal expressions). | PKU detailed tag (36) |
| **z** | Descriptive word/Stative verb | Descriptive or stative words. Functions to describe states or properties. | Original PKU (26 basic) |
"""

ZH_PKU_EXAMPLE = """**Text**: "沙瑞山的工作就是根据卫星观测数据，重新绘制一幅更精确的全宇宙微波辐射背景图。"

**Output JSON**: 
[
  {{'token': '沙瑞山', 'tag': 'nr', 'desc': 'Personal name'}},
  {{'token': '的', 'tag': 'u', 'desc': 'Auxiliary/Particle'}},
  {{'token': '工作', 'tag': 'vn', 'desc': 'Verbal noun'}},
  {{'token': '就', 'tag': 'd', 'desc': 'Adverb'}},
  {{'token': '是', 'tag': 'v', 'desc': 'Verb'}},
  {{'token': '根据', 'tag': 'p', 'desc': 'Preposition'}},
  {{'token': '卫星', 'tag': 'n', 'desc': 'Common noun'}},
  {{'token': '观测', 'tag': 'vn', 'desc': 'Verbal noun'}},
  {{'token': '数据', 'tag': 'n', 'desc': 'Common noun'}},
  {{'token': '，', 'tag': 'w', 'desc': 'Punctuation'}},
  {{'token': '重新', 'tag': 'd', 'desc': 'Adverb'}},
  {{'token': '绘制', 'tag': 'v', 'desc': 'Verb'}},
  {{'token': '一', 'tag': 'm', 'desc': 'Numeral'}},
  {{'token': '幅', 'tag': 'q', 'desc': 'Classifier/Measure word'}},
  {{'token': '更', 'tag': 'd', 'desc': 'Adverb'}},
  {{'token': '精确', 'tag': 'a', 'desc': 'Adjective'}},
  {{'token': '的', 'tag': 'u', 'desc': 'Auxiliary/Particle'}},
  {{'token': '全', 'tag': 'a', 'desc': 'Adjective'}},
  {{'token': '宇宙', 'tag': 'n', 'desc': 'Common noun'}},
  {{'token': '微波', 'tag': 'n', 'desc': 'Common noun'}},
  {{'token': '辐射', 'tag': 'vn', 'desc': 'Verbal noun'}},
  {{'token': '背景', 'tag': 'n', 'desc': 'Common noun'}},
  {{'token': '图', 'tag': 'n', 'desc': 'Common noun'}},
  {{'token': '。', 'tag': 'w', 'desc': 'Punctuation'}},
]
"""

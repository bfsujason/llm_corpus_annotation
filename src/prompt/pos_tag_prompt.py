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
- **Carefully study and follow ALL the disambiguation guidelines in Section 3 before tagging**
- **Carefully study and follow ALL the provided examples in Section 5; when in doubt, find the closest parallel in the examples and follow the same tagging decision**

## 2. Ditto tags

**Ditto tags** mark multiword expressions that function as a single grammatical unit. They are formed by adding a **two-digit suffix** to the base tag.

**Format**: `TAG` + `N` + `P`, where:
- **N** = the **total number of words** in the multiword expression (count ALL words first!)
- **P** = the **position** of the current word within the sequence (1st word → 1, 2nd word → 2, …, Nth word → N)

### ⚠️ CRITICAL: Count the total number of words FIRST, THEN assign position numbers.

**Step-by-step procedure**:
1. Identify the multiword expression and its base tag.
2. **Count the total number of words** in the expression → this becomes N (the FIRST suffix digit for ALL words in the expression).
3. **Assign position numbers** 1, 2, …, N to each word → this becomes P (the SECOND suffix digit).
4. Every word in the expression gets the SAME first digit N.

### Worked examples

**2-word expressions** (N=2): first digit is always **2** for both words.

| Expression | Function | Word 1 | Word 2 |
|------------|----------|--------|--------|
| of course | adverb | of_RR**21** | course_RR**22** |
| at length | adverb | at_RR**21** | length_RR**22** |
| due to | preposition | due_II**21** | to_II**22** |
| because of | preposition | because_II**21** | of_II**22** |
| so that | conjunction | so_CS**21** | that_CS**22** |

**3-word expressions** (N=3): first digit is always **3** for ALL THREE words.

| Expression | Function | Word 1 | Word 2 | Word 3 |
|------------|----------|--------|--------|--------|
| in terms of | preposition | in_II**31** | terms_II**32** | of_II**33** |
| in front of | preposition | in_II**31** | front_II**32** | of_II**33** |
| in spite of | preposition | in_II**31** | spite_II**32** | of_II**33** |
| on top of | preposition | on_II**31** | top_II**32** | of_II**33** |
| by means of | preposition | by_II**31** | means_II**32** | of_II**33** |
| as long as | conjunction | as_CS**31** | long_CS**32** | as_CS**33** |
| as soon as | conjunction | as_CS**31** | soon_CS**32** | as_CS**33** |
| as well as | conjunction | as_CS**31** | well_CS**32** | as_CS**33** |
| as far as | conjunction | as_CS**31** | far_CS**32** | as_CS**33** |
| in order to | before-clause marker | in_BCL**31** | order_BCL**32** | to_BCL**33** |

**Common error to AVOID**:
- ❌ WRONG: as_CS21 long_CS22 as_CS23 (misuses "2" as first digit for a 3-word expression)
- ✅ RIGHT: as_CS31 long_CS32 as_CS33 (correctly uses "3" as first digit because there are 3 words)

The first digit must be the SAME across all words and must equal the TOTAL word count. If you see the first digit varying across words in the same expression, or if it does not match the total word count, you have made an error.

### Common multiword expressions that may use ditto tags include:
- Compound prepositions: in spite of, in front of, in terms of, on top of, by means of, because of, due to
- Compound conjunctions: as long as, as soon as, as well as, as far as, so that, in order that
- Before-clause markers: in order to
- Compound adverbs: at least, at most, at length, of course
- Fixed expressions: a lot (of), a bit (of), kind of, sort of

**Note**: Only use ditto tags for established multiword expressions in the CLAWS idiomlist, not for arbitrary word combinations.

## 3. DISAMBIGUATION GUIDELINES FOR CONFUSABLE CATEGORIES

### 3.1 Finite Base Form vs. Infinitive (VV0 vs. VVI; VH0 vs. VHI; VD0 vs. VDI; VB0 vs. VBI)

This distinction applies to ALL verb paradigms (lexical verbs VV, have VH, do VD, be VB):

| Context | Tag | Example |
|---------|-----|---------|
| After a modal auxiliary (will, can, must, shall, should, would, could, might, may) | Infinitive: VVI / VHI / VDI / VBI | "must **have**" → have_VHI; "'ll **give**" → give_VVI; "must **be**" → be_VBI |
| After auxiliary do/does/did | Infinitive: VVI / VHI / VBI | "didn't want" → want_VVI; "doesn't have" → have_VHI; "did ... do" → do_VDI |
| After infinitive marker *to* | Infinitive: VVI / VHI / VDI / VBI | "to **cry**" → cry_VVI; "to **be**" → be_VBI |
| After causative/perception verbs (let, make, see, hear, etc.) as bare infinitive complement | Infinitive: VVI | "let us **go**" → go_VVI |
| Imperative | Finite base form: VV0 / VB0 | "**Give** me that!" → Give_VV0; "**Be** careful!" → Be_VB0 |
| Present tense (subject is not 3rd person singular) | Finite base form: VV0 / VH0 / VD0 | "they **understand**" → understand_VV0; "they **have**" → have_VH0 |

**Key principle**: If the verb is governed by another verb or *to*, use the infinitive tag. If the verb is a finite predicate (imperative, present tense), use the base form tag.

### 3.2 The 's Ambiguity

The clitic **'s** has three distinct analyses in CLAWS7. You must determine which applies from context:

| Analysis | Tag | Test | Example |
|----------|-----|------|---------|
| is (contraction of *is*) | VBZ | Can be expanded to "is"; followed by predicate (adjective, noun phrase, verb) | "That girl**'s** only a baby" → 's_VBZ |
| Genitive marker | GE | Followed by a noun (possessive reading) | "his son**'s** astuteness" → 's_GE |
| us (contraction of *us*) | VM22 | Only in "let's" | "Let**'s** go" → Let_VM21 's_VM22 |

### 3.3 Determiners with Pronominal Function: D-tags vs. P-tags

**Core CLAWS7 rule**: ALL determiners capable of pronominal function receive D-tags, REGARDLESS of whether they are acting as determiners or pronouns in the given context. Only words that can NEVER function as determiners (e.g., *they*, *nobody*, *who*) receive P-tags.

| Word | Tag | Reasoning |
|------|-----|-----------|
| each | DD1 | Can modify nouns ("each day") — always DD1, even in "each of them" |
| what | DDQ | Can modify nouns ("what color?") — always DDQ, even in "what have they done?" |
| this/that | DD1 | Can modify nouns — always DD1, even in pronominal use |
| these/those | DD2 | Plural determiner — always DD2 |
| which | DDQ | Can modify nouns — always DDQ |
| who | PNQS | Can NEVER modify a noun — true pronoun, use P-tag |
| they/he/she | PPHS1/PPHS2 | Can NEVER modify a noun — true pronoun |
| nobody/everyone | PN1 | Can NEVER modify a noun — true pronoun |

### 3.4 one: MC1 vs. PN1

| Usage | Tag | Example |
|-------|-----|---------|
| Selecting/identifying an individual from a set; numerical contrast | MC1 | "**One** was a white-haired old man" (one of three); "the **one** he addressed as Zongxi"; "**one** of the nine provinces" |
| Generic/impersonal pronoun (= a person in general) | PN1 | "**One** should always be careful" |

### 3.5 Past Participle vs. Adjective (VVN vs. JJ)

Many past participle forms can function as adjectives. Use these tests:

| Indicator | → Tag | Example |
|-----------|-------|---------|
| Followed by *by* + agent (doer of action) | VVN | "**startled** by this sudden violence" → VVN |
| Can be paraphrased with passive "was/were + V-ed by..." | VVN | "**armed** with a halberd" → VVN (= who were armed) |
| Takes adjective complements (with, about, at, of) rather than agent *by* | JJ | "**pleased** with his son's astuteness" → JJ |
| Accepts degree modifiers (very, quite, rather) naturally | JJ | "very pleased" is natural → JJ |
| Fixed adjective+preposition collocation (pleased with, interested in, worried about) | JJ | "**pleased** with..." → JJ |
| Used attributively before a noun with no verbal force | JJ | "a **startled** expression" → JJ 

### 3.6 Adverb Subcategories: RR vs. RG vs. RL vs. RP vs. RT

This is one of the most error-prone areas. Use the following decision guide:

| Tag | Function | Typical Words | Example |
|-----|----------|---------------|---------|
| **RG** (degree adverb) | Modifies an adjective, adverb, or numeral/quantifier to express degree | very, so, too, quite, rather, extremely, somewhat, even (before comparatives), some (≈ approximately before numbers), more (before adj/adv/numerals) | "**very** cruel" → very_RG; "**even** louder" → even_RG; "**some** hundred yards" → some_RG; "**somewhat** portly" → somewhat_RG; "**more** than thirty" → more_RGR |
| **RL** (locative adverb) | Indicates spatial location or direction | here, there, indoors, outdoors, northwards, somewhere, everywhere, nowhere, upstairs, away, abroad | "trudging **northwards**" → northwards_RL; "go **indoors**" → indoors_RL; "up **there**" → there_RL; "**everywhere**" → everywhere_RL |
| **RP** (prepositional adverb / particle) | Part of a phrasal verb; semantically fused with the verb | up (pick up), out (find out), on (put on), off (take off) | "picked **up**" → up_RP; "rose **up**" → up_RP |
| **RT** (quasi-nominal adverb of time) | Time adverbs that can also function as nouns (e.g., after prepositions) | now, then, today, tomorrow, yesterday, tonight | "go indoors **now**" → now_RT; "**then**, on a sheet of paper" → then_RT |
| **RR** (general adverb) | All other adverbs: manner, frequency, focus, discourse markers, sentence adverbs | really, only, never, close, together, wrong (adverbial use), also, though (parenthetical), so (discourse marker) | "**really** give" → really_RR; "cried **close** together" → close_RR; "done **wrong**" → wrong_RR; "**only** grass" → only_RR |

**Key decision steps**:
1. Does it modify an adjective/adverb/numeral to express degree? → **RG**
2. Does it indicate spatial location or direction (and is not part of a phrasal verb)? → **RL**
3. Is it a particle fused with a verb in a phrasal verb? → **RP**
4. Is it a time word that can also serve as a noun? → **RT**
5. Otherwise → **RR**

**Distinguishing RP from RL**: If the word's spatial meaning is transparent and independent (e.g., "running **away**" = running to a distant place), prefer RL. If the word is semantically fused with the verb and its spatial meaning is bleached/abstract (e.g., "rose **up**" = rebelled; "picked **up**" = lifted), prefer RP.

**Distinguishing RP from II (stranded preposition)**: A stranded preposition whose logical object has been fronted retains its preposition tag II, not RP. E.g., "something to cry **about**" → about_II (the logical structure is "cry about something").

### 3.7 Adjective vs. Adverb for Dual-Category Words

Some words (wrong, close, loud, right, etc.) can function as either adjective or adverb without adding -ly:

| Position/Function | Tag | Example |
|-------------------|-----|---------|
| After a linking verb (be, seem, look, etc.) as subject complement | JJ | "is **wrong**" → wrong_JJ; "they were **cruel**" → cruel_JJ |
| Before a noun as modifier | JJ | "the **wrong** answer" → wrong_JJ; "a **close** friend" → close_JJ |
| Modifying a verb (describes manner of action) | RR (or RRR for comparative) | "done **wrong**" → wrong_RR; "walked **close** together" → close_RR; "cried **louder**" → louder_RRR |

### 3.8 Specialized Noun Subcategories

CLAWS7 has several specialized noun tags. Do NOT default to NN1/NN2 when a more specific tag applies:

| Tag | Category | When to Use | Examples |
|-----|----------|-------------|---------|
| **NN** | Number-neutral common noun | The word form is identical in singular and plural (no separate plural form) | deer, sheep, cod, aircraft, headquarters |
| **NNT1/NNT2** | Temporal noun | The noun denotes a unit or period of time | day/days, week/weeks, year/years, month/months |
| **NNU1/NNU2** | Unit of measurement | The noun denotes a measurement unit | inch/inches, yard/yards, foot/feet, mile/miles, centimetre |
| **NNO/NNO2** | Numeral noun | The noun is a number word used as a noun | dozen, hundred, thousand, million |
| **NNL1/NNL2** | Locative noun | The noun denotes a type of place, especially in geographic names | River, Island, Street, Province, Mountain, Lake |
| **NNB** | Preceding noun of title | The noun is a title/honorific placed before a name or used as a form of address | Mr., Dr., Prof., King (in "King George"), Viscount |
| **NNA** | Following noun of title | The noun is a title/qualification placed after a name | M.A., Ph.D., Jr., Sr. |
| **ND1** | Singular noun of direction | The noun denotes a compass direction, used as a noun (often with *of*) | "somewhere **south** of the river" → south_ND1 |

**NNB vs. NN1 for titles**: Use NNB when the title word serves as a title prefix or vocative address. Use NN1 when it is the head noun of the phrase:
- "**Viscount** of Chu" → Viscount_NNB (title prefix)
- "the Zhou **king**" → king_NN1 (head noun modified by "the Zhou")
- "**Papa**," said the boy → Papa_NNB (vocative address)
- "wanting to be **Emperor**" → Emperor_NN1 (head noun, complement of *be*)

### 3.9 Proper Noun vs. Common Noun (NP1 vs. NN1)

| Indicator | Tag | Example |
|-----------|-----|---------|
| Unique name of a person, place, or entity | NP1 | "**Huang** **Zongxi**" → NP1 NP1; "**Chu**" → NP1; "**Zhejiang**" → NP1 |
| Institutional/conceptual noun, even if capitalized, when used generically or with an indefinite article | NN1 | "a cruel **God**" → God_NN1 (indefinite article signals common noun use); "subjects of **Empire**" → Empire_NN1 (abstract/institutional) |
| Proper noun used as modifier before a common noun | NP1 (retained) | "**Zhou** king" → Zhou_NP1; "**Yangtze** River" → Yangtze_NP1 |

### 3.10 The Verb Paradigms for *have*, *do*, and *be*

CLAWS7 assigns dedicated tags to ALL forms of *have*, *do*, and *be* — whether they are used as main verbs or auxiliaries. Never use VV- tags for these verbs.

| Verb | Base finite | Past | -ing | Infinitive | Past participle | 3sg present | Other |
|------|-------------|------|------|------------|-----------------|-------------|-------|
| **have** | VH0 | VHD | VHG | VHI | VHN | VHZ | — |
| **do** | VD0 | VDD | VDG | VDI | VDN | VDZ | — |
| **be** | VB0 | VBDZ (was) / VBDR (were) | VBG | VBI | VBN | VBZ | VBM (am), VBR (are) |

Examples:
- "what ... soldiers **do**" → do_VD0 (main verb, finite base)
- "**had** the name" → had_VHD (main verb *have*, past tense)
- "must **have** made" → have_VHI (infinitive after modal)
- "they **have** ... **done** wrong" → have_VH0 + done_VDN

### 3.11 Conjunction vs. Adverb vs. Other Uses

Several words can function as conjunctions or adverbs depending on context:

| Word | As conjunction | As adverb/other |
|------|---------------|-----------------|
| **that** | CST: introduces a nominal/adverbial clause: "understand **that** what..." | DD1: determiner before noun: "**that** girl"; RG: degree adverb: "not **that** big" |
| **when** | CS: introduces a temporal/conditional clause: "**when** people are massacred" | RRQ: interrogative adverb in questions: "**When** did you arrive?" |
| **though** | CS: introduces a concessive clause: "**Though** it rained, we went" | RR: parenthetical/sentence adverb (≈ however): "for the common people **though**" |
| **so** | CS: introduces a purpose/result clause: "speak clearly **so** everyone hears" | RR: discourse marker (≈ therefore/then): "**So** you understand that..." |
| **as** | CSA: introduces a clause: "**as** I mentioned" | II: preposition meaning "in the role of": "identifiable ... **as** a member" |
| **like** | CS: introduces a clause (informal): "it looks **like** it might rain" | II: preposition before NP: "he, **like** his host, was..." |

### 3.12 both and half as Before-Determiners

| Word | Tag | Context | Example |
|------|-----|---------|---------|
| both | DB2 | Pre-determiner or floating quantifier | "... **both** mean wanting to be Emperor" → both_DB2 |
| half | DB | Pre-determiner before a determiner: "**half** the time" | half_DB |
| half | NN1 | Head noun of NP: "the lower **half** of his face" | half_NN1 |
| all | DB | Pre-determiner: "**all** the people" | all_DB |

### 3.13 some: Determiner vs. Degree Adverb

| Usage | Tag | Example |
|-------|-----|---------|
| Determiner before a noun (= an unspecified quantity) | DD | "**some** soldiers" → some_DD |
| Approximator before a number (≈ approximately) | RG | "**some** hundred yards" → some_RG |

### 3.14 only: RR vs. JJ vs. RG

| Usage | Tag | Example |
|-------|-----|---------|
| Focus adverb (= merely, just); modifies verb or restricts scope of NP | RR | "eats **only** grass"; "girl's **only** a baby"; "**only** the Zhou king had the right" |
| Attributive adjective (= sole) before a noun | JJ | "the **only** child" |
| Degree adverb modifying adj/adv | RG | "**only** slightly better" |

### 3.15 Gerund vs. Present Participle

CLAWS7 does NOT distinguish between gerunds and present participles. Both receive the **VVG** tag (or VHG, VDG, VBG for *have*, *do*, *be*):
- Gerund (noun function): "**Deceiving** Your Majesty was a capital offence" → Deceiving_VVG
- Present participle (verbal/adjectival function): "was **escorting** a line" → escorting_VVG
- After a preposition: "by **running** away" → running_VVG

### 3.16 more: RGR vs. DAR vs. RRR

| Usage | Tag | Example |
|-------|-----|---------|
| Modifying an adjective, adverb, or numeral (degree) | RGR | "**more** than thirty arrests" → more_RGR; "**more** beautiful" → more_RGR |
| Directly modifying a noun (determiner function) | DAR | "**more** books" → more_DAR; "**more** people" → more_DAR |
| Modifying a verb (adverbial function) | RRR | "work **more**" → more_RRR; "eat **more**" → more_RRR |

## 4. THE COMPLETE TAGSET

{tagset}

## 5. OUTPUT FORMAT

Return a JSON list. Each object must contain:

- `token`: The individual token.
- `tag`: The POS tag code for that token.
- `desc`: The description of that tag from the reference table.

## 6. EXAMPLES

**Study the examples below carefully.** 

{example}

---

**YOUR TASK**:

Annotate the following text. Tag each token following ALL the rules and disambiguation guidelines above, applying ditto tags to recognized multiword expressions. When encountering difficult decisions, refer back to Section 3 (Disambiguation Guidelines) and Section 6 (Examples) before making your choice.

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

**Text**: "Along a coastal road somewhere south of the Yangtze River, a detachment of soldiers, each of them armed with a halberd, was escorting a line of seven prison carts, trudging northwards in the teeth of a bitter wind."

**Output JSON**:
[
    {{"token": "Along", "tag": "II", "desc": "General preposition"}},
    {{"token": "a", "tag": "AT1", "desc": "Singular article"}},
    {{"token": "coastal", "tag": "JJ", "desc": "General adjective"}},
    {{"token": "road", "tag": "NN1", "desc": "Singular common noun"}},
    {{"token": "somewhere", "tag": "RL", "desc": "Locative adverb"}},
    {{"token": "south", "tag": "ND1", "desc": "Singular noun of direction"}},
    {{"token": "of", "tag": "IO", "desc": "Of (preposition)"}},
    {{"token": "the", "tag": "AT", "desc": "Article"}},
    {{"token": "Yangtze", "tag": "NP1", "desc": "Singular proper noun"}},
    {{"token": "River", "tag": "NNL1", "desc": "Singular locative noun"}},
    {{"token": ",", "tag": ",", "desc": "Punctuation"}},
    {{"token": "a", "tag": "AT1", "desc": "Singular article"}},
    {{"token": "detachment", "tag": "NN1", "desc": "Singular common noun"}},
    {{"token": "of", "tag": "IO", "desc": "Of (preposition)"}},
    {{"token": "soldiers", "tag": "NN2", "desc": "Plural common noun"}},
    {{"token": ",", "tag": ",", "desc": "Punctuation"}},
    {{"token": "each", "tag": "DD1", "desc": "Singular determiner"}},
    {{"token": "of", "tag": "IO", "desc": "Of (preposition)"}},
    {{"token": "them", "tag": "PPHO2", "desc": "3rd person plural objective pronoun"}},
    {{"token": "armed", "tag": "VVN", "desc": "Past participle of lexical verb"}},
    {{"token": "with", "tag": "IW", "desc": "With/without (prepositions)"}},
    {{"token": "a", "tag": "AT1", "desc": "Singular article"}},
    {{"token": "halberd", "tag": "NN1", "desc": "Singular common noun"}},
    {{"token": ",", "tag": ",", "desc": "Punctuation"}},
    {{"token": "was", "tag": "VBDZ", "desc": "Was"}},
    {{"token": "escorting", "tag": "VVG", "desc": "-ing participle of lexical verb"}},
    {{"token": "a", "tag": "AT1", "desc": "Singular article"}},
    {{"token": "line", "tag": "NN1", "desc": "Singular common noun"}},
    {{"token": "of", "tag": "IO", "desc": "Of (preposition)"}},
    {{"token": "seven", "tag": "MC", "desc": "Cardinal number (neutral)"}},
    {{"token": "prison", "tag": "NN1", "desc": "Singular common noun"}},
    {{"token": "carts", "tag": "NN2", "desc": "Plural common noun"}},
    {{"token": ",", "tag": ",", "desc": "Punctuation"}},
    {{"token": "trudging", "tag": "VVG", "desc": "-ing participle of lexical verb"}},
    {{"token": "northwards", "tag": "RL", "desc": "Locative adverb"}},
    {{"token": "in", "tag": "II41", "desc": "General preposition"}},
    {{"token": "the", "tag": "II42", "desc": "General preposition"}},
    {{"token": "teeth", "tag": "II43", "desc": "General preposition"}},
    {{"token": "of", "tag": "II44", "desc": "General preposition"}},
    {{"token": "a", "tag": "AT1", "desc": "Singular article"}},
    {{"token": "bitter", "tag": "JJ", "desc": "General adjective"}},
    {{"token": "wind", "tag": "NN1", "desc": "Singular common noun"}},
    {{"token": ".", "tag": ".", "desc": "punctuation"}},
]

### Example 2:

**Text**: "In each of the first three carts a single male prisoner was caged, identifiable by his dress as a member of the scholar class."

**Output JSON**:
[   
    {{"token": "In", "tag": "II", "desc": "General preposition"}},
	{{"token": "each", "tag": "DD1", "desc": "Singular determiner"}},
	{{"token": "of", "tag": "IO", "desc": "Of (preposition)"}},
	{{"token": "the", "tag": "AT", "desc": "Article"}},
	{{"token": "first", "tag": "MD", "desc": "Ordinal number"}},
	{{"token": "three", "tag": "MC", "desc": "Cardinal number (neutral)"}},
	{{"token": "carts", "tag": "NN2", "desc": "Plural common noun"}},
	{{"token": "a", "tag": "AT1", "desc": "Singular article"}},
	{{"token": "single", "tag": "JJ", "desc": "General adjective"}},
	{{"token": "male", "tag": "JJ", "desc": "General adjective"}},
	{{"token": "prisoner", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": "was", "tag": "VBDZ", "desc": "Was"}},
	{{"token": "caged", "tag": "VVN", "desc": "Past participle of lexical verb"}},
	{{"token": ",", "tag": ",", "desc": "Punctuation"}},
	{{"token": "identifiable", "tag": "JJ", "desc": "General adjective"}},
	{{"token": "by", "tag": "II", "desc": "General preposition"}},
	{{"token": "his", "tag": "APPGE", "desc": "Possessive pronoun, pre-nominal"}},
	{{"token": "dress", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": "as", "tag": "II", "desc": "General preposition"}},
	{{"token": "a", "tag": "AT1", "desc": "Singular article"}},
	{{"token": "member", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": "of", "tag": "IO", "desc": "Of (preposition)"}},
	{{"token": "the", "tag": "AT", "desc": "Article"}},
	{{"token": "scholar", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": "class", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": ".", "tag": ".", "desc": "Punctuation"}},
]

### Example 3:

**Text**: "Or I'll really give you something to cry about!'"

**Output JSON**:
[   
    {{"token": "Or", "tag": "CC", "desc": "coordinating conjunction"}},
	{{"token": "I", "tag": "PPIS1", "desc": "1st person singular subjective pronoun"}},
	{{"token": "'ll", "tag": "VM", "desc": "Modal auxiliary"}},
	{{"token": "really", "tag": "RR", "desc": "General adverb"}},
	{{"token": "give", "tag": "VVI", "desc": "Infinitive of lexical verb "}},
	{{"token": "you", "tag": "PPY", "desc": "2nd person personal pronoun"}},
	{{"token": "something", "tag": "PN1", "desc": "Indefinite pronoun, singular"}},
	{{"token": "to", "tag": "TO", "desc": "Infinitive marker"}},
	{{"token": "cry", "tag": "VVI", "desc": "Infinitive of lexical verb"}},
	{{"token": "about", "tag": "II", "desc": "General preposition"}},
	{{"token": "!", "tag": "!", "desc": "Punctuation"}},
	{{"token": "'", "tag": "'", "desc": "Punctuation"}},
]

### Example 4:

**Text**: "The baby, startled by this sudden violence, cried even louder."

**Output JSON**:
[   
    {{"token": "The", "tag": "AT", "desc": "Article"}},
	{{"token": "baby", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": ",", "tag": ",", "desc": "Punctuation"}},
	{{"token": "startled", "tag": "VVN", "desc": "Past participle of lexical verb"}},
	{{"token": "by", "tag": "II", "desc": "General preposition"}},
	{{"token": "this", "tag": "DD1", "desc": "singular determiner"}},
	{{"token": "sudden", "tag": "JJ", "desc": "General adjective"}},
	{{"token": "violence", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": ",", "tag": ",", "desc": "Punctuation"}},
	{{"token": "cried", "tag": "VVD", "desc": "Past tense of lexical verb"}},
	{{"token": "even", "tag": "RG", "desc": "Degree adverb"}},
	{{"token": "louder", "tag": "RRR", "desc": "Comparative general adverb"}},
	{{"token": ".", "tag": ".", "desc": "Punctuation"}},
]

### Example 5:

**Text**: "Under the eaves of a large house, some hundred yards from the road, a middle-aged scholar was standing with a ten- or eleven-year-old boy at his side."

**Output JSON**:
[   
    {{"token": "Under", "tag": "II", "desc": "General preposition"}},
	{{"token": "the", "tag": "AT", "desc": "Article"}},
	{{"token": "eaves", "tag": "NN2", "desc": "Plural common noun"}},
	{{"token": "of", "tag": "IO", "desc": "Of (preposition)"}},
	{{"token": "a", "tag": "AT1", "desc": "Aingular article"}},
	{{"token": "large", "tag": "JJ", "desc": "General adjective"}},
	{{"token": "house", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": ",", "tag": ",", "desc": "Punctuation"}},
	{{"token": "some", "tag": "RG", "desc": "Degree adverb"}},
	{{"token": "hundred", "tag": "NNO", "desc": "Numeral noun (neutral)"}},
	{{"token": "yards", "tag": "NNU2", "desc": "Plural unit of measurement"}},
	{{"token": "from", "tag": "II", "desc": "General preposition"}},
	{{"token": "the", "tag": "AT", "desc": "Article"}},
	{{"token": "road", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": ",", "tag": ",", "desc": "Punctuation"}},
	{{"token": "a", "tag": "AT1", "desc": "Singular article"}},
	{{"token": "middle-aged", "tag": "JJ", "desc": "General adjective"}},
	{{"token": "scholar", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": "was", "tag": "VBDZ", "desc": "Was"}},
	{{"token": "standing", "tag": "VVG", "desc": "-ing participle of lexical verb"}},
	{{"token": "with", "tag": "IW", "desc": "With/without (prepositions)"}},
	{{"token": "a", "tag": "AT1", "desc": "Aingular article"}},
	{{"token": "ten-", "tag": "MC", "desc": "Cardinal number"}},
	{{"token": "or", "tag": "CC", "desc": "Coordinating conjunction"}},
	{{"token": "eleven-year-old", "tag": "JJ", "desc": "General adjective"}},
	{{"token": "boy", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": "at", "tag": "II", "desc": "General preposition"}},
	{{"token": "his", "tag": "APPGE", "desc": "Possessive pronoun, pre-nominal"}},
	{{"token": "side", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": ".", "tag": ".", "desc": "Punctuation"}},
]

### Example 6:

**Text**: "'Papa,' said the little boy, 'what have they done wrong?'"

**Output JSON**:
[   
    {{"token": "'", "tag": "'", "desc": "Punctuation"}},
	{{"token": "Papa", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": ",", "tag": ",", "desc": "Punctuation"}},
	{{"token": "'", "tag": "'", "desc": "Punctuation"}},
	{{"token": "said", "tag": "VVD", "desc": "Past tense of lexical verb"}},
	{{"token": "the", "tag": "AT", "desc": "Article"}},
	{{"token": "little", "tag": "JJ", "desc": "General adjective"}},
	{{"token": "boy", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": ",", "tag": ",", "desc": "Punctuation"}},
	{{"token": "'", "tag": "'", "desc": "Punctuation"}},
	{{"token": "what", "tag": "DDQ", "desc": "Wh-determiner"}},
	{{"token": "have", "tag": "VH0", "desc": "Have, base form"}},
	{{"token": "they", "tag": "PPHS2", "desc": "3rd person plural subjective pronoun"}},
	{{"token": "done", "tag": "VDN", "desc": " Done"}},
	{{"token": "wrong", "tag": "RR", "desc": "General adverb"}},
	{{"token": "?", "tag": "?", "desc": "Punctuation"}},
	{{"token": "'", "tag": "'", "desc": "Punctuation"}},
]

### Example 7:

**Text**: "During these last two days they must have made more than thirty arrests."

**Output JSON**:
[   
    {{"token": "During", "tag": "II", "desc": "General preposition"}},
	{{"token": "these", "tag": "DD2", "desc": "Plural determiner"}},
	{{"token": "last", "tag": "MD", "desc": "Ordinal number"}},
	{{"token": "two", "tag": "MC", "desc": "Cardinal number (neutral)"}},
	{{"token": "days", "tag": "NNT2", "desc": "Temporal noun, plural"}},
	{{"token": "they", "tag": "PPHS2", "desc": "3rd person plural subjective pronoun"}},
	{{"token": "must", "tag": "VM", "desc": "Modal auxiliary"}},
	{{"token": "have", "tag": "VHI", "desc": "Have, infinitive"}},
	{{"token": "made", "tag": "VVN", "desc": "Past participle of lexical verb"}},
	{{"token": "more", "tag": "RGR", "desc": "Comparative degree adverb"}},
	{{"token": "than", "tag": "CSN", "desc": "Than (conjunction)"}},
	{{"token": "thirty", "tag": "MC", "desc": "Cardinal number (neutral)"}},
	{{"token": "arrests", "tag": "NN2", "desc": "Plural common noun"}},
	{{"token": ".", "tag": ".", "desc": "Punctuation"}},
]

### Example 8:

**Text**: "'That girl's only a baby,' said the boy."

**Output JSON**:
[   
    {{"token": "'", "tag": "'", "desc": "Punctuation"}},
	{{"token": "That", "tag": "DD1", "desc": "Singular determiner"}},
	{{"token": "girl", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": "'s", "tag": "VBZ", "desc": "Is"}},
	{{"token": "only", "tag": "RR", "desc": "General adverb"}},
	{{"token": "a", "tag": "AT1", "desc": "Singular article"}},
	{{"token": "baby", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": ",", "tag": ",", "desc": "Punctuation"}},
	{{"token": "'", "tag": "'", "desc": "Punctuation"}},
	{{"token": "said", "tag": "VVD", "desc": "Past tense of lexical verb"}},
	{{"token": "the", "tag": "AT", "desc": "Article"}},
	{{"token": "boy", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": ".", "tag": ".", "desc": "Punctuation"}},
]

### Example 9:

**Text**: "'So you understand that what the Government soldiers do is wrong,' said the man."

**Output JSON**:
[   
    {{"token": "'", "tag": "'", "desc": "Punctuation"}},
	{{"token": "So", "tag": "RR", "desc": "General adverb"}},
	{{"token": "you", "tag": "PPY", "desc": "2nd person personal pronoun"}},
	{{"token": "understand", "tag": "VV0", "desc": "Base form of lexical verb"}},
	{{"token": "that", "tag": "CST", "desc": "That (conjunction)"}},
	{{"token": "what", "tag": "DDQ", "desc": "Wh-determiner"}},
	{{"token": "the", "tag": "AT", "desc": "Article"}},
	{{"token": "Government", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": "soldiers", "tag": "NN2", "desc": "Plural common noun"}},
	{{"token": "do", "tag": "VD0", "desc": "Do, base form"}},
	{{"token": "is", "tag": "VBZ", "desc": "Is"}},
	{{"token": "wrong", "tag": "JJ", "desc": "General adjective"}},
	{{"token": ",", "tag": ",", "desc": "Punctuation"}},
	{{"token": "'", "tag": "'", "desc": "Punctuation"}},
	{{"token": "said", "tag": "VVD", "desc": "Past tense of lexical verb"}},
	{{"token": "the", "tag": "AT", "desc": "Article"}},
	{{"token": "man", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": ".", "tag": ".", "desc": "Punctuation"}},
]

### Example 10:

**Text**: "Let's go indoors now."

**Output JSON**:
[   
    {{"token": "Let", "tag": "VM21", "desc": "Modal auxiliary"}},
	{{"token": "'s", "tag": "VM22", "desc": "Modal auxiliary"}},
	{{"token": "go", "tag": "VVI", "desc": "Infinitive of lexical verb"}},
	{{"token": "indoors", "tag": "RL", "desc": "Locative adverb"}},
	{{"token": "now", "tag": "RT", "desc": "Quasi-nominal adverb of time"}},
	{{"token": ".", "tag": ".", "desc": "Punctuation"}},
]

### Example 11:

**Text**: "The man picked up a writing-brush and moistened it on the ink-slab, then, on a sheet of paper, he wrote the character for a deer."

**Output JSON**:
[   
    {{"token": "The", "tag": "AT", "desc": "Article"}},
	{{"token": "man", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": "picked", "tag": "VVD", "desc": "Past tense of lexical verb"}},
	{{"token": "up", "tag": "RP", "desc": "Prepositional adverb/particle"}},
	{{"token": "a", "tag": "AT1", "desc": "Singular article"}},
	{{"token": "writing-brush", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": "and", "tag": "CC", "desc": "Coordinating conjunction"}},
	{{"token": "moistened", "tag": "VVD", "desc": "Past tense of lexical verb"}},
	{{"token": "it", "tag": "PPH1", "desc": "3rd person singular neuter pronoun"}},
	{{"token": "on", "tag": "II", "desc": "General preposition"}},
	{{"token": "the", "tag": "AT", "desc": "Article"}},
	{{"token": "ink-slab", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": ",", "tag": ",", "desc": "Punctuation"}},
	{{"token": "then", "tag": "RT", "desc": "Quasi-nominal adverb of time"}},
	{{"token": ",", "tag": ",", "desc": "Punctuation"}},
	{{"token": "on", "tag": "II", "desc": "General preposition"}},
	{{"token": "a", "tag": "AT1", "desc": "Singular article"}},
	{{"token": "sheet", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": "of", "tag": "IO", "desc": "Of (preposition)"}},
	{{"token": "paper", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": ",", "tag": ",", "desc": "Punctuation"}},
	{{"token": "he", "tag": "PPHS1", "desc": "3rd person singular subjective pronoun"}},
	{{"token": "wrote", "tag": "VVD", "desc": "Past tense of lexical verb"}},
	{{"token": "the", "tag": "AT", "desc": "Article"}},
	{{"token": "character", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": "for", "tag": "IF", "desc": "For (preposition)"}},
	{{"token": "a", "tag": "AT1", "desc": "Singular article"}},
	{{"token": "deer", "tag": "NN", "desc": "Common noun (neutral for number)"}},
	{{"token": ".", "tag": ".", "desc": "Punctuation"}},
]

### Example 12:

**Text**: "If it can't escape by running away, it gets eaten."

**Output JSON**:
[   
    {{"token": "If", "tag": "CS", "desc": "Subordinating conjunction"}},
	{{"token": "it", "tag": "PPH1", "desc": "3rd person singular neuter pronoun"}},
	{{"token": "ca", "tag": "VM", "desc": "Modal auxiliary"}},
	{{"token": "n't", "tag": "XX", "desc": "Not/n't"}},
	{{"token": "escape", "tag": "VVI", "desc": "Infinitive of lexical verb"}},
	{{"token": "by", "tag": "II", "desc": "General preposition"}},
	{{"token": "running", "tag": "VVG", "desc": "-ing participle of lexical verb"}},
	{{"token": "away", "tag": "RL", "desc": "Locative adverb"}},
	{{"token": ",", "tag": ",", "desc": "Punctuation"}},
	{{"token": "it", "tag": "PPH1", "desc": "3rd person singular neuter pronoun"}},
	{{"token": "gets", "tag": "VVZ", "desc": "-s form of lexical verb"}},
	{{"token": "eaten", "tag": "VVN", "desc": "Past participle of lexical verb"}},
	{{"token": ".", "tag": ".", "desc": "Punctuation"}}，
]

### Example 13:

**Text**: "Ambitious men rose up everywhere and fought each other to possess it."

**Output JSON**:
[
    {{"token": "Ambitious", "tag": "JJ", "desc": "General adjective"}},
	{{"token": "men", "tag": "NN2", "desc": "Plural common noun"}},
	{{"token": "rose", "tag": "VVD", "desc": "Past tense of lexical verb"}},
	{{"token": "up", "tag": "RP", "desc": "Prepositional adverb/particle"}},
	{{"token": "everywhere", "tag": "RL", "desc": "Locative adverb"}},
	{{"token": "and", "tag": "CC", "desc": "Coordinating conjunction"}},
	{{"token": "fought", "tag": "VVD", "desc": "Past tense of lexical verb"}},
	{{"token": "each", "tag": "PPX221", "desc": "Plural reflexive personal pronoun"}},
	{{"token": "other", "tag": "PPX221", "desc": "Plural reflexive personal pronoun"}},
	{{"token": "to", "tag": "TO", "desc": "Infinitive marker"}},
	{{"token": "possess", "tag": "VVI", "desc": "Infinitive of lexical verb"}},
	{{"token": "it", "tag": "PPH1", "desc": "3rd person singular neuter pronoun"}},
	{{"token": ".", "tag": ".", "desc": "Punctuation"}}，
]

### Example 14:

**Text**: "The scholar nodded, pleased with his young son's astuteness."

**Output JSON**:
[
    {{"token": "The", "tag": "AT", "desc": "Article"}},
	{{"token": "scholar", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": "nodded", "tag": "VVD", "desc": "Past tense of lexical verb"}},
	{{"token": ",", "tag": ",", "desc": "Punctuation"}},
	{{"token": "pleased", "tag": "JJ", "desc": "General adjective"}},
	{{"token": "with", "tag": "IW", "desc": "With/without (prepositions)"}},
	{{"token": "his", "tag": "APPGE", "desc": "Possessive pronoun, pre-nominal"}},
	{{"token": "young", "tag": "JJ", "desc": "General adjective"}},
	{{"token": "son", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": "'s", "tag": "GE", "desc": "Possessive pronoun, pre-nominal"}},
	{{"token": "astuteness", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": ".", "tag": ".", "desc": "Punctuation"}}，
]

### Example 15:

**Text**: "They were very cruel."

**Output JSON**:
[
    {{"token": "They", "tag": "PPHS2", "desc": "3rd person plural subjective pronoun"}},
	{{"token": "were", "tag": "VBDR", "desc": "Were"}},
	{{"token": "very", "tag": "RG", "desc": "Degree adverb"}},
	{{"token": "cruel", "tag": "JJ", "desc": "General adjective"}},
	{{"token": ".", "tag": ".", "desc": "Punctuation"}}，
]

### Example 16:

**Text**: "They didn't like him."

**Output JSON**:
[   
    {{"token": "They", "tag": "PPHS2", "desc": "3rd person plural subjective pronoun"}},
	{{"token": "did", "tag": "VDD", "desc": "Did"}},
	{{"token": "n't", "tag": "XX", "desc": "Not/n't"}},
	{{"token": "like", "tag": "VVI", "desc": "Infinitive of lexical verb"}},
	{{"token": "him", "tag": "PPHO1", "desc": "3rd person singular objective pronoun"}},
	{{"token": ".", "tag": ".", "desc": "Punctuation"}},
]

### Example 17:

**Text**: "Each of these bronze cauldrons had the name of one of the nine provinces on it."

**Output JSON**:
[
    {{"token": "Each", "tag": "DD1", "desc": "Singular determiner"}},
	{{"token": "of", "tag": "IO", "desc": "Of (preposition)"}},
	{{"token": "these", "tag": "DD2", "desc": "Plural determiner"}},
	{{"token": "bronze", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": "cauldrons", "tag": "NN2", "desc": "Plural common noun"}},
	{{"token": "had", "tag": "VHD", "desc": "Had (past tense)"}},
	{{"token": "the", "tag": "AT", "desc": "Article"}},
	{{"token": "name", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": "of", "tag": "IO", "desc": "Of (preposition)"}},
	{{"token": "one", "tag": "MC1", "desc": "Singular cardinal number"}},
	{{"token": "of", "tag": "IO", "desc": "Of (preposition)"}},
	{{"token": "the", "tag": "AT", "desc": "Article"}},
	{{"token": "nine", "tag": "MC", "desc": " Cardinal number (neutral)"}},
	{{"token": "provinces", "tag": "NN2", "desc": "Plural common noun"}},
	{{"token": "on", "tag": "II", "desc": "General preposition"}},
	{{"token": "it", "tag": "PPH1", "desc": "3rd person singular neuter pronoun"}},
	{{"token": ".", "tag": ".", "desc": "Punctuation"}},
]

### Example 18:

**Text**: "Of course, only the Zhou king had the right."

**Output JSON**:
[
    {{"token": "Of", "tag": "RR21", "desc": "General adverb"}},
	{{"token": "course", "tag": "RR22", "desc": "General adverb"}},
	{{"token": ",", "tag": ",", "desc": "Punctuation"}},
	{{"token": "only", "tag": "RR", "desc": "General adverb"}},
	{{"token": "the", "tag": "AT", "desc": "Article"}},
	{{"token": "Zhou", "tag": "NP1", "desc": "Singular proper noun"}},
	{{"token": "king", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": "had", "tag": "VHD", "desc": "Had (past tense)"}},
	{{"token": "the", "tag": "AT", "desc": "Article"}},
	{{"token": "right", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": ".", "tag": ".", "desc": "Punctuation"}},
]

### Example 19:

**Text**: "He must be a cruel God up there."

**Output JSON**:
[
    {{"token": "He", "tag": "PPHS1", "desc": "3rd person singular subjective pronoun"}},
	{{"token": "must", "tag": "VM", "desc": "Modal auxiliary"}},
	{{"token": "be", "tag": "VBI", "desc": "Be, infinitive"}},
	{{"token": "a", "tag": "AT1", "desc": "Singular article"}},
	{{"token": "cruel", "tag": "JJ", "desc": "General adjective"}},
	{{"token": "God", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": "up", "tag": "RL", "desc": "Locative adverb"}},
	{{"token": "there", "tag": "RL", "desc": "Locative adverb"}},
	{{"token": ".", "tag": ".", "desc": "Punctuation"}},
]

### Example 20:

**Text**: "For the common people though, the subjects of Empire, our role is to be the deer."

**Output JSON**:
[
    {{"token": "For", "tag": "IF", "desc": "For (preposition)"}},
	{{"token": "the", "tag": "AT", "desc": "Article"}},
	{{"token": "common", "tag": "JJ", "desc": "General adjective"}},
	{{"token": "people", "tag": "NN2", "desc": "Plural common noun"}},
    {{"token": "though", "tag": "RR", "desc": "General adverb"}},
	{{"token": ",", "tag": ",", "desc": "Punctuation"}},
	{{"token": "the", "tag": "AT", "desc": "Article"}},
	{{"token": "subjects", "tag": "NN2", "desc": "Plural common noun"}},
	{{"token": "of", "tag": "IO", "desc": "Of (preposition)"}},
	{{"token": "Empire", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": ",", "tag": ",", "desc": "Punctuation"}},
	{{"token": "our", "tag": "APPGE", "desc": "Possessive pronoun, pre-nominal"}},
	{{"token": "role", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": "is", "tag": "VBZ", "desc": "Is"}},
	{{"token": "to", "tag": "TO", "desc": "Infinitive marker"}},
	{{"token": "be", "tag": "VBI", "desc": "Be, infinitive"}},
	{{"token": "the", "tag": "AT", "desc": "Article"}},
	{{"token": "deer", "tag": "NN", "desc": "Common noun (neutral for number)"}},
	{{"token": ".", "tag": ".", "desc": "Punctuation"}},
]

### Example 21:

**Text**: "For the time being I'm not going to cut your eyes out."

**Output JSON**:
[
    {{"token": "For", "tag": "RT41", "desc": "quasi-nominal adverb of time"}},
	{{"token": "the", "tag": "RT42", "desc": "quasi-nominal adverb of time"}},
	{{"token": "time", "tag": "RT43", "desc": "quasi-nominal adverb of time"}},
	{{"token": "being", "tag": "RT44", "desc": "quasi-nominal adverb of time"}},
	{{"token": "I", "tag": "PPIS1", "desc": "1st person singular subjective pronoun"}},
	{{"token": "'m", "tag": "VBM", "desc": "Am"}},
	{{"token": "not", "tag": "XX", "desc": "Not/n't"}},
	{{"token": "going", "tag": "VVGK", "desc": "-ing participle catenative"}},
	{{"token": "to", "tag": "TO", "desc": "Infinitive marker"}},
	{{"token": "cut", "tag": "VVI": "desc": "Infinitive of lexical verb"}},
	{{"token": "your", "tag": "APPGE", "desc": "Possessive pronoun, pre-nominal"}},
	{{"token": "eyes", "tag": "NN2", "desc": "Plural common noun"}},
	{{"token": "out", "tag": "RP", "desc": "Prepositional adverb/particle"}},
	{{"token": ".", "tag": ".", "desc": "Punctuation"}},
]

### Example 22:

**Text**: "He was too light to maintain the upper hand for long, however, and soon the boy was back on top of him again."

**Output JSON**:
[
    {{"token": "He", "tag": "PPHS1", "desc": "3rd person singular subjective pronoun"}},
	{{"token": "was", "tag": "VBDZ", "desc": "Was"}},
	{{"token": "too", "tag": "RG", "desc": "Degree adverb"}},
	{{"token": "light", "tag": "JJ", "desc": "General adjective"}},
	{{"token": "to", "tag": "TO", "desc": "Infinitive marker"}},
	{{"token": "maintain", "tag": "VVI", "desc": "Infinitive of lexical verb"}},
	{{"token": "the", "tag": "AT", "desc": "Article"}},
	{{"token": "upper", "tag": "JJ", "desc": "General adjective"}},
	{{"token": "hand", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": "for", "tag": "RR21", "desc": "General adverb"}},
	{{"token": "long", "tag": "RR22", "desc": "General adverb"}},
	{{"token": ",", "tag": ",", "desc": "Punctuation"}},
	{{"token": "however", "tag": "RR", "desc": "General adverb（"}},
	{{"token": ",", "tag": ",", "desc": "Punctuation（标点）"}},
	{{"token": "and", "tag": "CC", "desc": "Coordinating conjunction"}},
	{{"token": "soon", "tag": "RR", "desc": "General adverb"}},
	{{"token": "the", "tag": "AT", "desc": "Article"}},
	{{"token": "boy", "tag": "NN1", "desc": "Singular common noun"}},
	{{"token": "was", "tag": "VBDZ", "desc": "Was"}},
	{{"token": "back", "tag": "RL", "desc": "Locative adverb"}},
	{{"token": "on", "tag": "II31", "desc": "General preposition"}},
	{{"token": "top", "tag": "II32", "desc": "General preposition"}},
	{{"token": "of", "tag": "II33", "desc": "General preposition "}},
	{{"token": "him", "tag": "PPHO1", "desc": "3rd person singular objective pronoun"}},
	{{"token": "again", "tag": "RR", "desc": "General adverb"}},
	{{"token": ".", "tag": ".", "desc": "Punctuation"}},
]
"""

ZH_PKU_PROMPT = """You are a professional corpus linguist specialized in Part-of-Speech (POS) tagging.

Your task is to annotate Chinese text following the annotation scheme of PKU POS Tagset (北大计算语言学研究所词性标注集).
First segment the given text into tokens. Then assign a POS tag to each token.

## 1. ANNOTATION RULES

**YOU MUST**:
- **Keep all original text exactly as they appear - do NOT modify, correct, or rephrase any words**
- Tag each token individually by DEFAULT
- Ensure every token is covered in your output

## 2. SEGMENTATION PRINCIPLES
Proper segmentation is critical. Follow these principles carefully:

### 2.1 General Principle
Segmentation should be based on **whether a word combination is listed as a lexical entry in a standard modern Chinese dictionary** (such as《现代汉语语法信息词典》or《现代汉语词典》). Common, high-frequency compound words that are conventionally treated as single dictionary entries should be kept as whole units — do NOT over-split them.

### 2.2 Compound Words: Keep as Whole Unit
The following types of compounds should generally be segmented as **one token**:

- **Common verb-object compounds (离合词/常用动宾复合词)** that are dictionary entries:
  e.g., 吃饭、吃奶、下雪、睡觉、吃亏、帮忙、走路、唱歌、跑步、说话、游泳、散步、打仗、报仇
- **Common verb-complement compounds (动补复合词)** that are dictionary entries:
  e.g., 走进、打败、听见、看见、说道、喝道、提高、打开、放下
- ** Common verb-verb compounds (动动复合词)** that are dictionary entries:
  e.g., 说道、喝道、记载、保有、争夺、伤害、逃跑、煮食
- **Fixed idiomatic expressions (习用语)**:
  e.g., 差不多、了不起、说不定、来不及、对不起
- **Idioms (成语)**:
  e.g., 庞然大物、逐鹿中原
- **Common adverbs, conjunctions, and function words that have fused into single units**:
  e.g., 已经、从来、只是、因此、倘若、甚是、极为、就是说、何其

### 2.3 Free Phrases: Split into Separate Tokens
The following types should be split into **separate tokens**:

- **Productive, freely combined verb-object phrases** where the verb can take various objects interchangeably:
  e.g., 伸腿 → 伸/v 腿/n (cf. 伸手、伸脖子 — "伸" is freely productive)
  e.g., 提笔 → 提/v 笔/n (cf. 提刀、提包 — "提" is freely productive)
- **Productive verb-complement combinations** that are not fixed dictionary entries:
  e.g., 踢死 → 踢/v 死/v, 烧死 → 烧/v 死/v, 煮熟 → 煮/v 熟/a (These are freely productive: 踢伤、踢翻、烧焦、煮烂, etc.)
- ** Number + Measure Word + Noun structures**:
  e.g., 一/m 条/q 大路/n, 三/m 辆/q 囚车/n

### 2.4 Bound Morphemes vs. Free Words
A key distinction: in ancient Chinese quotations or literary expressions, many monosyllabic words that were free in classical Chinese are **bound morphemes** in modern Chinese. Tag them by their morpheme type according to their modern Chinese status:

- **Ng (名语素)**: 臣、金、主、道(道路义)、疆、心(内心义)、怀(胸怀义)、世、身
- **Vg (动语素)**: 逐、欺、诛、劳(慰劳义)、观(观看义)、就(前往义)
- **Ag (形容语素)**: 仁(仁慈义)
- **Tg (时语素)**: 秦、夏、周、汉(朝代单字)

Contrast with monosyllabic words that **remain free** in modern Chinese (tag as full word classes):

- **v**: 说、写、问、收、铸、失、知、走、吃、用、煮、烧
- **n**: 鹿、鼎、车、屋、窗、笔、纸、风、人、手、头、路

### 2.5 Location Words: "Noun/Morpheme + Direction Word" Rules
Follow the PKU standard strictly:

**(a)** Free monosyllabic noun (n) + monosyllabic direction word (f) → split into two tokens:
  e.g., 车/n 上/f, 屋/n 里/f, 窗/n 边/f, 纸/n 上/f, 鼎/n 里/f

**(b)** Bound monosyllabic nominal morpheme (Ng) + monosyllabic direction word (f) → merge into one location word (s) or time word (t):
  e.g., 怀中/s, 心里/s, 世上/s, 身上/s, 胸前/s, 桌上/s, 午后/t


### 2.6 Decision Heuristic
When uncertain whether to keep a compound as one token or split it, apply this test:

- **Dictionary test**: Is the combination listed as a single entry in a standard modern Chinese dictionary? → If YES, keep as one token.
- **Productivity test**: Can the first component freely combine with many other second components to form similar phrases with predictable meanings? → If YES (highly productive), split.
- **Frequency test**: Is the combination a common, high-frequency word that native speakers perceive as a single unit? → If YES, keep as one token.
- **When in doubt**, prefer keeping common compounds whole rather than over-splitting.

## 3. THE COMPLETE TAGSET

{tagset}

## 4. OUTPUT FORMAT

Return a JSON list. Each object must contain:

- `token`: The individual token.
- `tag`: The POS tag code for that token.
- `desc`: The description of that tag from the reference table.

## 5. EXAMPLES

**Study the examples below carefully**. Pay close attention to segmentation decisions — which compounds are kept whole and which are split — and apply the same principles consistently.

{example}

---

**YOUR TASK**:

Annotate the following text. Segment and tag each token following ALL the rules above. Pay special attention to segmentation granularity: do not over-split common dictionary words, and do not under-split free phrases.

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
| **nr** | Personal name | Names of people. Functions to identify individuals. Case 1: Surnames and given names of Han Chinese people, as well as those of non-Han people who use the same naming conventions as the Han, are segmented separately and each is tagged as nr. Example: 张/nr 仁伟/nr, 欧阳/nr 修/nr, 阮/nr 志雄/nr, 朴/nr 贞爱/nr Case 2: In addition to single-character and compound surnames, Han Chinese people also have double surnames; that is, some women, after marriage, add their husband’s surname to their original surname. In this situation, both surnames should be segmented and labeled as nr. Example: 陈/nr 方/nr 安生/nr, 唐/nr 鲁氏/nr Case 3: Job titles, honorifics, or titles after surnames should be separated. Example: 江/nr 主席/n, 小平/nr 同志/n, 江/nr 总书记/n, 张/nr 教授/n, 王/nr 部长/n, 陈/nr 老总/n, 李/nr 大娘/n, 刘/nr 阿姨/n, 龙/nr 姑姑/n Case 4: If a person’s abbreviation, honorific, or similar form consists of two characters, it is treated as a single segmentation unit and tagged as nr. Example: 老张/nr, 大李/nr, 小郝/nr, 郭老/nr, 陈总/nr Case 5: Clearly ranked kinship titles should be seg1mented; those not clearly ranked should not be segmented. Example: 三/m 哥/n, 大嫂/n, 大/a 女儿/n, 大哥/n, 小弟/n, 老爸/n Case 6: Some famous writers whose names or pen names are not easily distinguishable by surname and given name should be treated as one segmentation unit. Example: 鲁迅/nr, 茅盾/nr, 巴金/nr, 三毛/nr, 琼瑶/nr, 白桦/nr Case 7: For foreign names or the transliterated names of ethnic minority people (including the surnames of Japanese people) should not be segmented and should be labeled as nr. Example: 克林顿/nr, 叶利钦/nr, 才旦卓玛/nr, 小林多喜二/nr, 北研二/nr, 华盛顿/nr, 爱因斯坦/nr. Case 8: For some Western people's surnames that have a middle dot, do not segment. Example: 卡尔·马克思/nr |
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

**Text**: "江南近海滨的一条大路上，一队清兵手执刀枪，押着七辆囚车，冲风冒寒，向北而行。"

**Output JSON**: 
[
    {{"token": "江南", "tag": "ns", "desc": "Place name"}},
	{{"token": "近", "tag": "v", "desc": "Verb"}},
	{{"token": "海滨", "tag": "n", "desc": "Common noun"}},
	{{"token": "的", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "一", "tag": "m", "desc": "Numeral"}},
	{{"token": "条", "tag": "q", "desc": "Classifier/Measure word"}},
	{{"token": "大路", "tag": "n", "desc": "Common noun"}},
	{{"token": "上", "tag": "f", "desc": "Directional/Localizer"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "一", "tag": "m", "desc": "Numeral"}},
	{{"token": "队", "tag": "q", "desc": "Classifier/Measure word"}},
	{{"token": "清兵", "tag": "n", "desc": "Common noun"}},
	{{"token": "手", "tag": "n", "desc": "Common noun"}},
	{{"token": "执", "tag": "v", "desc": "Verb"}},
	{{"token": "刀枪", "tag": "n", "desc": "Common noun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "押", "tag": "v", "desc": "Verb"}},
	{{"token": "着", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "七", "tag": "m", "desc": "Numeral"}},
	{{"token": "辆", "tag": "q", "desc": "Classifier/Measure"}},
	{{"token": "囚车", "tag": "n", "desc": "Common noun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "冲风", "tag": "v", "desc": "Verb"}},
	{{"token": "冒寒", "tag": "v", "desc": "Verb"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "向", "tag": "p", "desc": "Preposition"}},
	{{"token": "北", "tag": "f", "desc": "Directional/Localizer"}},
	{{"token": "而", "tag": "c", "desc": "Conjunction"}},
	{{"token": "行", "tag": "v", "desc": "Verb"}},
]

### Example 2:

**Text**: "前面三辆囚车中分别监禁的是三个男子，都作书生打扮，一个是白发老者，两个是中年人。"

**Output JSON**: 
[
    {{"token": "前面", "tag": "f", "desc": "Directional/Localizer"}},
	{{"token": "三", "tag": "m", "desc": "Numeral"}},
	{{"token": "辆", "tag": "q", "desc": "Classifier/Measure"}},
	{{"token": "囚车", "tag": "n", "desc": "Common noun"}},
	{{"token": "中", "tag": "f", "desc": "Directional/Localizer"}},
	{{"token": "分别", "tag": "d", "desc": "Adverb"}},
	{{"token": "监禁", "tag": "v", "desc": "Verb"}},
	{{"token": "的", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "是", "tag": "v", "desc": "Verb"}},
	{{"token": "三", "tag": "m", "desc": "Numeral"}},
	{{"token": "个", "tag": "q", "desc": "Classifier/Measure"}},
	{{"token": "男子", "tag": "n", "desc": "Common noun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "都", "tag": "d", "desc": "Adverb"}},
	{{"token": "作", "tag": "v", "desc": "Verb"}},
	{{"token": "书生", "tag": "n", "desc": "Common noun"}},
	{{"token": "打扮", "tag": "vn", "desc": "Verb as noun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "一个", "tag": "m", "desc": "Numeral"}},
	{{"token": "是", "tag": "v", "desc": "Verb"}},
	{{"token": "白发", "tag": "n", "desc": "Common noun"}},
	{{"token": "老者", "tag": "n", "desc": "Common noun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "两个", "tag": "m", "desc": "Numeral"}},
	{{"token": "是", "tag": "v", "desc": "Verb"}},
	{{"token": "中年人", "tag": "n", "desc": "Common noun"}},
	{{"token": "。", "tag": "w", "desc": "Punctuation"}},
]

### Example 3:

**Text**: "后面四辆囚车中坐的是女子，最后一辆囚车中是个少妇，怀中抱着个女婴。"

**Output JSON**: 
[
    {{"token": "后面", "tag": "f", "desc": "Directional/Localizer"}},
	{{"token": "四", "tag": "m", "desc": "Numeral"}},
	{{"token": "辆", "tag": "q", "desc": "Classifier/Measure"}},
	{{"token": "囚车", "tag": "n", "desc": "Common noun"}},
	{{"token": "中", "tag": "f", "desc": "Directional/Localizer"}},
	{{"token": "坐", "tag": "v", "desc": "Verb"}},
	{{"token": "的", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "是", "tag": "v", "desc": "Verb）"}},
	{{"token": "女子", "tag": "n", "desc": "Common noun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "最后", "tag": "f", "desc": "Directional/Localizer"}},
	{{"token": "一", "tag": "m", "desc": "Numeral"}},
	{{"token": "辆", "tag": "q", "desc": "Classifier/Measure"}},
	{{"token": "囚车", "tag": "n", "desc": "Common noun"}},
	{{"token": "中", "tag": "f", "desc": "Directional/Localizer"}},
	{{"token": "是", "tag": "v", "desc": "Verb"}},
	{{"token": "个", "tag": "q", "desc": "Classifier/Measure"}},
	{{"token": "少妇", "tag": "n", "desc": "Common noun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "怀中", "tag": "s", "desc": "Space word/Locative"}},
	{{"token": "抱", "tag": "v", "desc": "Verb"}},
	{{"token": "着", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "个", "tag": "q", "desc": "Classifier/Measure"}},
	{{"token": "女婴", "tag": "n", "desc": "Common noun"}},
]

### Example 4:

**Text**: "女婴啼哭不休。"

**Output JSON**: 
[
    {{"token": "女婴", "tag": "n", "desc": "Common noun"}},
	{{"token": "啼哭", "tag": "v", "desc": "Verb"}},
    {{"token": "不", "tag": "d", "desc": "Adverb"}}, 
    {{"token": "休", "tag": "v", "desc": "Verb"}},
	{{"token": "。", "tag": "w", "desc": "Punctuation"}},
]

### Example 5:

**Text**: "她母亲温言相呵，女婴只是大哭。"

**Output JSON**: 
[
    {{"token": "她", "tag": "r", "desc": "Pronoun"}},
	{{"token": "母亲", "tag": "n", "desc": "Common noun"}},
	{{"token": "温言", "tag": "n", "desc": "Common noun"}},
	{{"token": "相", "tag": "d", "desc": "Adverb"}},
	{{"token": "呵", "tag": "v", "desc": "Verb"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "女婴", "tag": "n", "desc": "Common noun"}},
	{{"token": "只是", "tag": "d", "desc": "Adverb"}},
	{{"token": "大哭", "tag": "v", "desc": "Verb"}},
	{{"token": "。", "tag": "w", "desc": "Punctuation"}},
]

### Example 6:

**Text**: "囚车旁一清兵恼了，伸腿在车上踢了一脚，喝道：“再哭，再哭！"

**Output JSON**: 
[
    {{"token": "囚车", "tag": "n", "desc": "Common noun"}},
	{{"token": "旁", "tag": "f", "desc": "Directional/Localizer"}},
	{{"token": "一", "tag": "m", "desc": "Numeral"}},
	{{"token": "清兵", "tag": "n", "desc": "Common noun"}},
	{{"token": "恼", "tag": "v", "desc": "Verb"}},
	{{"token": "了", "tag": "y", "desc": "Sentence-final particle"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "伸", "tag": "v", "desc": "Verb"}},
    {{"token": "腿", "tag": "n", "desc": "Common noun"}},
	{{"token": "在", "tag": "p", "desc": "Preposition"}},
	{{"token": "车", "tag": "n", "desc": "Common noun"}},
    {{"token": "上", "tag": "s", "desc": "Directional/Localizer"}},
	{{"token": "踢", "tag": "v", "desc": "Verb"}},
	{{"token": "了", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "一", "tag": "m", "desc": "Numeral"}},
	{{"token": "脚", "tag": "q", "desc": "Classifier/Measure"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "喝道", "tag": "v", "desc": "Verb"}},
	{{"token": "：", "tag": "w", "desc": "Punctuation"}},
	{{"token": "“", "tag": "w", "desc": "Punctuation"}},
	{{"token": "再", "tag": "d", "desc": "Adverb"}},
	{{"token": "哭", "tag": "v", "desc": "Verb"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "再", "tag": "d", "desc": "Adverb"}},
	{{"token": "哭", "tag": "v", "desc": "Verb"}},
	{{"token": "！", "tag": "w", "desc": "Punctuation"}},
]

### Example 7:

**Text**: "老子踢死你！”"

**Output JSON**: 
[
    {{"token": "老子", "tag": "r", "desc": "Pronoun"}},
	{{"token": "踢", "tag": "v", "desc": "Verb"}},
	{{"token": "死", "tag": "v", "desc": "Verb"}},
	{{"token": "你", "tag": "r", "desc": "Pronoun"}},
	{{"token": "！", "tag": "w", "desc": "Punctuation"}},
	{{"token": "”", "tag": "w", "desc": "Punctuation"}},
]

### Example 8:

**Text**: "那个小女孩还在吃奶。"

**Output JSON**: 
[
    {{"token": "那个", "tag": "r", "desc": "Pronoun"}},
	{{"token": "小", "tag": "a", "desc": "Adjective"}},
	{{"token": "女孩", "tag": "n", "desc": "Common noun"}},
	{{"token": "还", "tag": "d", "desc": "Adverb"}},
	{{"token": "在", "tag": "d", "desc": "Adverb"}},
	{{"token": "吃奶", "tag": "v", "desc": "Verb"}},
	{{"token": "。", "tag": "w", "desc": "Punctuation"}},
]

### Example 9:

**Text**: "昨日和今朝已逮去了三十几人，都是我们浙江有名的读书人，个个都是无辜株连。"

**Output JSON**: 
[
    {{"token": "昨日", "tag": "t", "desc": "Time word/Temporal noun"}},
	{{"token": "和", "tag": "c", "desc": "Conjunction"}},
	{{"token": "今朝", "tag": "t", "desc": "Time word/Temporal noun"}},
	{{"token": "已", "tag": "d", "desc": "Adverb"}},
	{{"token": "逮", "tag": "v", "desc": "Verb"}},
	{{"token": "去", "tag": "v", "desc": "Verb"}},
	{{"token": "了", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "三十几", "tag": "m", "desc": "Numeral"}},
	{{"token": "人", "tag": "n", "desc": "Common noun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "都", "tag": "d", "desc": "Adverb"}},
	{{"token": "是", "tag": "v", "desc": "Verb"}},
	{{"token": "我们", "tag": "r", "desc": "Pronoun"}},
	{{"token": "浙江", "tag": "ns", "desc": "Place name"}},
	{{"token": "有名", "tag": "a", "desc": "Adjective"}},
	{{"token": "的", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "读书人", "tag": "n", "desc": "Common noun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "个个", "tag": "r", "desc": "Pronoun"}},
	{{"token": "都", "tag": "d", "desc": "Adverb"}},
	{{"token": "是", "tag": "v", "desc": "Verb"}},
	{{"token": "无辜", "tag": "a", "desc": "Adjective"}},
	{{"token": "株连", "tag": "vn", "desc": "Verb as noun"}},
	{{"token": "。", "tag": "w", "desc": "Punctuation"}},
]

### Example 10:

**Text**: "他说到“无辜株连”四字，声音压得甚低，生怕给押囚车的官兵听见了。"

**Output JSON**: 
[
    {{"token": "他", "tag": "r", "desc": "Pronoun"}},
	{{"token": "说", "tag": "v", "desc": "Verb"}},
	{{"token": "到", "tag": "v", "desc": "Verb"}},
	{{"token": "“", "tag": "w", "desc": "Punctuation"}},
	{{"token": "无辜", "tag": "a", "desc": "Adjective"}},
	{{"token": "株连", "tag": "vn", "desc": "Verb as noun"}},
	{{"token": "”", "tag": "w", "desc": "Punctuation"}},
	{{"token": "四", "tag": "m", "desc": "Numeral"}},
	{{"token": "字", "tag": "n", "desc": "Common noun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "声音", "tag": "n", "desc": "Common noun"}},
	{{"token": "压", "tag": "v", "desc": "Verb"}},
	{{"token": "得", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "甚", "tag": "Dg", "desc": "Adverb morpheme"}},
	{{"token": "低", "tag": "a", "desc": "Adjective"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "生怕", "tag": "v", "desc": "Verb"}},
	{{"token": "给", "tag": "p", "desc": "Preposition"}},
	{{"token": "押", "tag": "v", "desc": "Verb"}},
	{{"token": "囚车", "tag": "n", "desc": "Common noun"}},
	{{"token": "的", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "官兵", "tag": "n", "desc": "Common noun"}},
	{{"token": "听见", "tag": "v", "desc": "Verb"}},
	{{"token": "了", "tag": "y", "desc": "Sentence-final particle"}},
	{{"token": "。", "tag": "w", "desc": "Punctuation"}},
]

### Example 11:

**Text**: "那文士道：“你懂得官兵没道理，真是好孩子。"

**Output JSON**: 
[   
    {{"token": "那", "tag": "r", "desc": "Pronoun"}},
	{{"token": "文士", "tag": "n", "desc": "Common noun"}},
	{{"token": "道", "tag": "v", "desc": "Verb"}},
	{{"token": "：", "tag": "w", "desc": "Punctuation"}},
	{{"token": "“", "tag": "w", "desc": "Punctuation"}},
	{{"token": "你", "tag": "r", "desc": "Preposition"}},
	{{"token": "懂得", "tag": "v", "desc": "Verb"}},
	{{"token": "官兵", "tag": "n", "desc": "Common noun"}},
	{{"token": "没", "tag": "v", "desc": "Verb"}},
	{{"token": "道理", "tag": "n", "desc": "Common noun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "真", "tag": "d", "desc": "Adverb"}},
	{{"token": "是", "tag": "v", "desc": "Verb"}},
	{{"token": "好", "tag": "a", "desc": "Adjective"}},
	{{"token": "孩子", "tag": "n", "desc": "Common noun"}},
]

### Example 12:

**Text**: "哎，人为刀俎，我为鱼肉，人为鼎镬，我为麋鹿！”"

**Output JSON**: 
[
    {{"token": "哎", "tag": "e", "desc": "Interjection"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "人为刀俎", "tag": "i", "desc": "Idiom"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "我为鱼肉", "tag": "i", "desc": "Idiom"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "人", "tag": "n", "desc": "Common noun"}},
	{{"token": "为", "tag": "v", "desc": "Verb"}},
	{{"token": "鼎镬", "tag": "n", "desc": "Common noun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "我", "tag": "r", "desc": "Pronoun"}},
	{{"token": "为", "tag": "v", "desc": "Verb"}},
	{{"token": "麋鹿", "tag": "n", "desc": "Common noun"}},
	{{"token": "！", "tag": "w", "desc": "Punctuation"}},
	{{"token": "”", "tag": "w", "desc": "Punctuation"}},
]

### Example 13:

**Text**: "那文士道：“正是！”"

**Output JSON**: 
[
    {{"token": "那", "tag": "r", "desc": "Pronoun"}},
	{{"token": "文士", "tag": "n", "desc": "Common noun"}},
	{{"token": "道", "tag": "v", "desc": "Verb"}},
	{{"token": "：", "tag": "w", "desc": "Punctuation"}},
	{{"token": "“", "tag": "w", "desc": "Punctuation"}},
	{{"token": "正是", "tag": "v", "desc": "Verb"}},
	{{"token": "！", "tag": "w", "desc": "Punctuation"}},
	{{"token": "”", "tag": "w", "desc": "Punctuation"}},
]

### Example 14:

**Text**: "眼见官兵和囚车已经去远，拉着小孩的手道：“外面风大，我们回屋里去。”"

**Output JSON**: 
[
    {{"token": "眼见", "tag": "v", "desc": "Verb"}},
	{{"token": "官兵", "tag": "n", "desc": "Common noun"}},
	{{"token": "和", "tag": "c", "desc": "Conjunction"}},
	{{"token": "囚车", "tag": "n", "desc": "Common noun"}},
	{{"token": "已经", "tag": "d", "desc": "Adverb"}},
	{{"token": "去", "tag": "v", "desc": "Verb"}},
	{{"token": "远", "tag": "a", "desc": "Adjective"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "拉", "tag": "v", "desc": "Verb"}},
	{{"token": "着", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "小孩", "tag": "n", "desc": "Common noun"}},
	{{"token": "的", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "手", "tag": "n", "desc": "Common noun"}},
	{{"token": "道", "tag": "v", "desc": "Verb"}},
	{{"token": "：", "tag": "w", "desc": "Punctuation"}},
	{{"token": "“", "tag": "w", "desc": "Punctuation"}},
	{{"token": "外面", "tag": "f", "desc": "Directional/Localizer"}},
	{{"token": "风", "tag": "n", "desc": "Common noun"}},
	{{"token": "大", "tag": "a", "desc": "Adjective"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "我们", "tag": "r", "desc": "Pronoun"}},
	{{"token": "回", "tag": "v", "desc": "Verb"}},
	{{"token": "屋", "tag": "n", "desc": "Common noun"}},
    {{"token": "里", "tag": "s", "desc": "Directional"}},
	{{"token": "去", "tag": "v", "desc": "Verb"}},
	{{"token": "。", "tag": "w", "desc": "Punctuation"}},
	{{"token": "”", "tag": "w", "desc": "Punctuation"}}，
]

### Example 15:

**Text**: "当下父子二人走进书房。"

**Output JSON**: 
[
    {{"token": "当下", "tag": "t", "desc": "Time word/Temporal noun"}},
	{{"token": "父子", "tag": "n", "desc": "Common noun"}},
	{{"token": "二", "tag": "m", "desc": "Numeral"}},
	{{"token": "人", "tag": "n", "desc": "Common noun"}},
	{{"token": "走进", "tag": "v", "desc": "Verb"}},
	{{"token": "书房", "tag": "n", "desc": "Common noun"}},
	{{"token": "。", "tag": "w", "desc": "Punctuation"}},
]

### Example 16:

**Text**: "那文士提笔蘸上了墨，在纸上写了个“鹿”字，说道：“鹿这种野兽，虽是庞然大物，性子却极为平和，只吃青草和树叶，从来不伤害别的野兽。"

**Output JSON**: 
[
    {{"token": "那", "tag": "r", "desc": "Pronoun"}},
	{{"token": "文士", "tag": "n", "desc": "Common noun"}},
	{{"token": "提", "tag": "v", "desc": "Verb"}},
	{{"token": "笔", "tag": "n", "desc": "Common noun"}},
	{{"token": "蘸", "tag": "v", "desc": "Verb"}},
	{{"token": "上", "tag": "v", "desc": "Verb"}},
	{{"token": "了", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "墨", "tag": "n", "desc": "Common noun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "在", "tag": "p", "desc": "Preposition"}},
	{{"token": "纸", "tag": "n", "desc": "Common noun"}},
	{{"token": "上", "tag": "f", "desc": "Directional/Localizer"}},
	{{"token": "写", "tag": "v", "desc": "Verb"}},
	{{"token": "了", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "个", "tag": "q", "desc": "Classifier/Measure"}},
	{{"token": "“", "tag": "w", "desc": "Punctuation"}},
	{{"token": "鹿", "tag": "n", "desc": "Common noun"}},
	{{"token": "”", "tag": "w", "desc": "Punctuation"}},
	{{"token": "字", "tag": "n", "desc": "Common noun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "说道", "tag": "v", "desc": "Verb"}},
	{{"token": "：", "tag": "w", "desc": "Punctuation"}},
	{{"token": "“", "tag": "w", "desc": "Punctuation"}},
	{{"token": "鹿", "tag": "n", "desc": "Common noun"}},
	{{"token": "这", "tag": "r", "desc": "Pronoun"}},
	{{"token": "种", "tag": "q", "desc": "Classifier/Measure"}},
	{{"token": "野兽", "tag": "n", "desc": "Common noun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "虽", "tag": "c", "desc": "Conjunction"}},
	{{"token": "是", "tag": "v", "desc": "Verb"}},
	{{"token": "庞然大物", "tag": "i", "desc": "Idiom"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "性子", "tag": "n", "desc": "Common noun"}},
	{{"token": "却", "tag": "d", "desc": "Adverb"}},
	{{"token": "极为", "tag": "d", "desc": "Adverb"}},
	{{"token": "平和", "tag": "a", "desc": "Adjective"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "只", "tag": "d", "desc": "Adverb"}},
	{{"token": "吃", "tag": "v", "desc": "Verb"}},
	{{"token": "青草", "tag": "n", "desc": "Common noun"}},
	{{"token": "和", "tag": "c", "desc": "Conjunction"}},
	{{"token": "树叶", "tag": "n", "desc": "Common noun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "从来", "tag": "d", "desc": "Adverb"}},
	{{"token": "不", "tag": "d", "desc": "Adverb"}},
	{{"token": "伤害", "tag": "v", "desc": "Verb"}},
	{{"token": "别的", "tag": "r", "desc": "Pronoun"}},
	{{"token": "野兽", "tag": "n", "desc": "Common noun"}},
	{{"token": "。", "tag": "w", "desc": "Punctuation"}},
]

### Example 17:

**Text**: "又写了“逐鹿”两字，说道：“因此古人常常拿鹿来比喻天下。"

**Output JSON**: 
[
    {{"token": "又", "tag": "d", "desc": "Adverb"}},
	{{"token": "写", "tag": "v", "desc": "Verb"}},
	{{"token": "了", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "“", "tag": "w", "desc": "Punctuation"}},
	{{"token": "逐鹿", "tag": "v", "desc": "Verb"}},
	{{"token": "”", "tag": "w", "desc": "Punctuation"}},
	{{"token": "两", "tag": "m", "desc": "Numeral"}},
	{{"token": "字", "tag": "n", "desc": "Common noun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "说道", "tag": "v", "desc": "Verb"}},
	{{"token": "：", "tag": "w", "desc": "Punctuation"}},
	{{"token": "“", "tag": "w", "desc": "Punctuation"}},
	{{"token": "因此", "tag": "c", "desc": "Conjunction"}},
	{{"token": "古人", "tag": "n", "desc": "Common noun"}},
	{{"token": "常常", "tag": "d", "desc": "Adverb"}},
	{{"token": "拿", "tag": "p", "desc": "Preposition"}},
	{{"token": "鹿", "tag": "n", "desc": "Common noun"}},
	{{"token": "来", "tag": "v", "desc": "Verb"}},
	{{"token": "比喻", "tag": "v", "desc": "Verb"}},
	{{"token": "天下", "tag": "n", "desc": "Common noun"}},
	{{"token": "。", "tag": "w", "desc": "Punctuation"}},
]

### Example 18:

**Text**: "世上百姓都温顺善良，只有给人欺压残害的份儿。"

**Output JSON**: 
[
    {{"token": "世上", "tag": "s", "desc": "Space word/Locative"}},
	{{"token": "百姓", "tag": "n", "desc": "Common noun"}},
	{{"token": "都", "tag": "d", "desc": "Adverb"}},
	{{"token": "温顺", "tag": "a", "desc": "Adjective"}},
	{{"token": "善良", "tag": "a", "desc": "Adjective"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "只有", "tag": "d", "desc": "Adverb"}},
	{{"token": "给", "tag": "p", "desc": "Preposition"}},
	{{"token": "人", "tag": "n", "desc": "Common noun"}},
	{{"token": "欺压", "tag": "v", "desc": "Verb"}},
	{{"token": "残害", "tag": "v", "desc": "Verb"}},
	{{"token": "的", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "份儿", "tag": "n", "desc": "Common noun"}},
	{{"token": "。", "tag": "w", "desc": "Punctuation"},
]

### Example 19:

**Text**: "《汉书》上说：‘秦失其鹿，天下共逐之。’"

**Output JSON**: 
[  
    {{"token": "《", "tag": "w", "desc": "Punctuation"}},
	{{"token": "汉书", "tag": "nz", "desc": "Other proper noun"}},
	{{"token": "》", "tag": "w", "desc": "Punctuation"}},
	{{"token": "上", "tag": "f", "desc": "Directional/Localizer"}},
	{{"token": "说", "tag": "v", "desc": "Verb"}},
	{{"token": "：", "tag": "w", "desc": "Punctuation"}},
	{{"token": "‘", "tag": "w", "desc": "Punctuation"}},
	{{"token": "秦", "tag": "Tg", "desc": "Temporal morpheme"}},
	{{"token": "失", "tag": "v", "desc": "Verb"}},
	{{"token": "其", "tag": "r", "desc": "Pronoun"}},
	{{"token": "鹿", "tag": "n", "desc": "Common noun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "天下", "tag": "n", "desc": "Common noun"}},
	{{"token": "共", "tag": "d", "desc": "Adverb"}},
	{{"token": "逐", "tag": "Vg", "desc": "Verb morpheme"}},
	{{"token": "之", "tag": "r", "desc": "Pronoun"}},
	{{"token": "。", "tag": "w", "desc": "Punctuation"}},
	{{"token": "’", "tag": "w", "desc": "Punctuation"}},
]

### Example 20:

**Text**: "那就是说，秦朝失了天下，群雄并起，大家争夺，最后汉高祖打败了楚霸王，就得了这只又肥又大的鹿。”"

**Output JSON**: 
[
    {{"token": "那", "tag": "c", "desc": "Conjunction"}},
    {{"token": "就是说", "tag": "c", "desc": "Conjunction"}},
    {{"token": "，", "tag": "w", "desc": "Punctuation"}},
    {{"token": "秦朝", "tag": "t", "desc": "Time word/Temporal noun"}},
    {{"token": "失", "tag": "v", "desc": "verb"}},
    {{"token": "了", "tag": "u", "desc": "Auxiliary/Particle"}},
    {{"token": "天下", "tag": "n", "desc": "Common noun"}},
    {{"token": "，", "tag": "w", "desc": "Punctuation"}},
    {{"token": "群雄并起", "tag": "l", "desc": "Idiom or fixed phrase"}},
    {{"token": "，", "tag": "w", "desc": "Punctuation"}},
    {{"token": "大家", "tag": "r", "desc": "Pronoun"}},
    {{"token": "争夺", "tag": "v", "desc": "Verb"}},
    {{"token": "，", "tag": "w", "desc": "Punctuation"}},
    {{"token": "最后", "tag": "t", "desc": "Time word/Temporal noun"}},
    {{"token": "汉高祖", "tag": "nr", "desc": "Personal name"}},
    {{"token": "打败", "tag": "v", "desc": "Verb"}},
    {{"token": "了", "tag": "u", "desc": "Auxiliary/Particle"}},
    {{"token": "楚霸王", "tag": "nr", "desc": "Personal name"}},
    {{"token": "，", "tag": "w", "desc": "Punctuation"}},
    {{"token": "就", "tag": "d", "desc": "Adverb"}},
    {{"token": "得", "tag": "v", "desc": "Verb"}},
    {{"token": "了", "tag": "u", "desc": "Auxiliary/Particle"}},
    {{"token": "这", "tag": "r", "desc": "Pronoun"}},
    {{"token": "只", "tag": "q", "desc": "Classifier/Measure"}},
    {{"token": "又", "tag": "c", "desc": "Conjunction"}},
    {{"token": "肥", "tag": "a", "desc": "Adjective"}},
    {{"token": "又", "tag": "c", "desc": "Conjunction"}},
    {{"token": "大", "tag": "a", "desc": "Adjective"}},
    {{"token": "的", "tag": "u", "desc": "Auxiliary/Particle"}},
    {{"token": "鹿", "tag": "n", "desc": "Common noun"}},
    {{"token": "。", "tag": "w", "desc": "Punctuation"}},
    {{"token": "”", "tag": "w", "desc": "Punctuation"}},
]

### Example 21:

**Text**: "小说书上说‘逐鹿中原’，就是大家争着要作皇帝的意思。”"

**Output JSON**: 
[
    {{"token": "小说", "tag": "n", "desc": "Common noun"}},
	{{"token": "书", "tag": "n", "desc": "Common noun"}},{{"token": "上", "tag": "f", "desc": "Directional/Localizer"}},
	{{"token": "说", "tag": "v", "desc": "Verb"}},
	{{"token": "‘", "tag": "w", "desc": "Punctuation"}},
	{{"token": "逐鹿中原", "tag": "i", "desc": "Idiom"}},
	{{"token": "’", "tag": "w", "desc": "Punctuation"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "就是", "tag": "v", "desc": "Verb"}},
	{{"token": "大家", "tag": "r", "desc": "Pronoun"}},
	{{"token": "争", "tag": "v", "desc": "Verb"}},
	{{"token": "着", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "要", "tag": "v", "desc": "Verb"}},
	{{"token": "作", "tag": "v", "desc": "Verb"}},
	{{"token": "皇帝", "tag": "n", "desc": "Common noun"}},
	{{"token": "的", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "意思", "tag": "n", "desc": "Common noun"}},
	{{"token": "。", "tag": "w", "desc": "Punctuation"}},
	{{"token": "”", "tag": "w", "desc": "Punctuation"}},
]

### Example 22:

**Text**: "那文士甚是喜欢，点了点头，在纸上画了一只鼎的图形，道：“古人煮食，不用灶头锅子，用这样三只脚的鼎，下面烧柴，捉到了鹿，就在鼎里煮来吃。"

**Output JSON**: 
[
    {{"token": "那", "tag": "r", "desc": "Pronoun"}},
	{{"token": "文士", "tag": "n", "desc": "Common noun"}},
	{{"token": "甚是", "tag": "d", "desc": "Adverb"}},
	{{"token": "喜欢", "tag": "v", "desc": "Verb"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "点", "tag": "v", "desc": "Verb"}},
	{{"token": "了", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "点", "tag": "q", "desc": "Classifier/Measure"}},
	{{"token": "头", "tag": "n", "desc": "Common noun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "在", "tag": "p", "desc": "Preposition"}},
	{{"token": "纸", "tag": "n", "desc": "Common noun"}},
	{{"token": "上", "tag": "f", "desc": "Directional/Localizer"}},
	{{"token": "画", "tag": "v", "desc": "Verb"}},
	{{"token": "了", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "一", "tag": "m", "desc": "Numeral"}},
	{{"token": "只", "tag": "q", "desc": "Classifier/Measure"}},
	{{"token": "鼎", "tag": "n", "desc": "Common noun"}},
	{{"token": "的", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "图形", "tag": "n", "desc": "Common noun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "道", "tag": "v", "desc": "Verb"}},
	{{"token": "：", "tag": "w", "desc": "Punctuation"}},
	{{"token": "“", "tag": "w", "desc": "Punctuation"}},
	{{"token": "古人", "tag": "n", "desc": "Common noun"}},
	{{"token": "煮食", "tag": "v", "desc": "Verb"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "不", "tag": "d", "desc": "Adverb"}},
	{{"token": "用", "tag": "v", "desc": "Verb"}},
	{{"token": "灶头", "tag": "n", "desc": "Common noun"}},
	{{"token": "锅子", "tag": "n", "desc": "Common noun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "用", "tag": "v", "desc": "Verb"}},
	{{"token": "这样", "tag": "r", "desc": "Pronoun"}},
	{{"token": "三", "tag": "m", "desc": "Numeral"}},
	{{"token": "只", "tag": "q", "desc": "Classifier/Measure"}},
	{{"token": "脚", "tag": "n", "desc": "Common noun"}},
	{{"token": "的", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "鼎", "tag": "n", "desc": "Common noun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "下面", "tag": "f", "desc": "Directional/Localizer"}},
	{{"token": "烧", "tag": "v", "desc": "Verb"}},
	{{"token": "柴", "tag": "n", "desc": "Common noun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "捉", "tag": "v", "desc": "Verb"}},
	{{"token": "到", "tag": "v", "desc": "Verb"}},
	{{"token": "了", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "鹿", "tag": "n", "desc": "Common noun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "就", "tag": "d", "desc": "Adverb"}},
	{{"token": "在", "tag": "p", "desc": "Preposition"}},
	{{"token": "鼎", "tag": "n", "desc": "Common noun"}},
	{{"token": "里", "tag": "f", "desc": "Directional/Localizer"}},
	{{"token": "煮", "tag": "v", "desc": "Verb"}},
	{{"token": "来", "tag": "v", "desc": "Verb"}},
	{{"token": "吃", "tag": "v", "desc": "Verb"}},
    {{"token": "。", "tag": "w", "desc": "Punctuation"}},
]

### Example 23:

**Text**: "把他放在鼎里活活煮熟。"

**Output JSON**: 
[
    {{"token": "把", "tag": "p", "desc": "Preposition"}},
	{{"token": "他", "tag": "r", "desc": "Pronoun"}},
	{{"token": "放", "tag": "v", "desc": "Verb"}},
	{{"token": "在", "tag": "p", "desc": "Preposition"}},
	{{"token": "鼎", "tag": "n", "desc": "Common noun"}},
	{{"token": "里", "tag": "f", "desc": "Directional/Localizer"}},
	{{"token": "活活", "tag": "d", "desc": "Adverb"}},
	{{"token": "煮", "tag": "v", "desc": "Verb"}},
	{{"token": "熟", "tag": "a", "desc": "Adjective"}},
	{{"token": "。", "tag": "w", "desc": "Punctuation"}}，
]

### Example 24:

**Text**: "臣知欺大王之罪当诛也，臣请就鼎锅。"

**Output JSON**: 
[
    {{"token": "臣", "tag": "Ng", "desc": "Noun morpheme"}},
	{{"token": "知", "tag": "v", "desc": "Verb"}},
	{{"token": "欺", "tag": "Vg", "desc": "Verb morpheme"}},
	{{"token": "大王", "tag": "n", "desc": "Common noun"}},
	{{"token": "之", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "罪", "tag": "n", "desc": "Common noun"}},
	{{"token": "当", "tag": "v", "desc": "Verb"}},
	{{"token": "诛", "tag": "Vg", "desc": "Verb morpheme"}},
	{{"token": "也", "tag": "y", "desc": "Sentence-final particle"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "臣", "tag": "Ng", "desc": "Noun morpheme"}},
	{{"token": "请", "tag": "v", "desc": "Verb"}},
	{{"token": "就", "tag": "v", "desc": "Verb"}},
	{{"token": "鼎锅", "tag": "n", "desc": "Common noun"}},
	{{"token": "。", "tag": "w", "desc": "Punctuation"}},
]

### Example 25:

**Text**: "就是说：‘我该死，将我在鼎里烧死了罢！"

**Output JSON**: 
[
    {{"token": "就是说", "tag": "c", "desc": "Conjunction"}},
	{{"token": "：", "tag": "w", "desc": "Punctuation"}},
	{{"token": "‘", "tag": "w", "desc": "Punctuation"}},
	{{"token": "我", "tag": "r", "desc": "Pronoun"}},
	{{"token": "该", "tag": "v", "desc": "Verb"}},
	{{"token": "死", "tag": "v", "desc": "Verb"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "将", "tag": "p", "desc": "Preposition"}},
	{{"token": "我", "tag": "r", "desc": "Pronoun"}},
	{{"token": "在", "tag": "p", "desc": "Preposition"}},
	{{"token": "鼎", "tag": "n", "desc": "Common noun"}},
	{{"token": "里", "tag": "f", "desc": "Directional/Localizer"}},
	{{"token": "烧", "tag": "v", "desc": "Verb"}},
	{{"token": "死", "tag": "v", "desc": "Verb"}},
	{{"token": "了", "tag": "y", "desc": "Sentence-final particle"}},
	{{"token": "罢", "tag": "y", "desc": "Sentence-final particle"}},
	{{"token": "！", "tag": "w", "desc": "Punctuation"}},
	{{"token": "’", "tag": "w", "desc": "Punctuation"}},
	{{"token": "”", "tag": "w", "desc": "Punctuation"}},
]

### Example 26:

**Text**: "这两句话，意思也差不多么？"

**Output JSON**: 
[
    {{"token": "这", "tag": "r", "desc": "Pronoun"}},
	{{"token": "两", "tag": "m", "desc": "Numeral"}},
	{{"token": "句", "tag": "q", "desc": "Classifier/Measure"}},
	{{"token": "话", "tag": "n", "desc": "Common noun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "意思", "tag": "n", "desc": "Common noun"}},
	{{"token": "也", "tag": "d", "desc": "Adverb"}},
	{{"token": "差不多", "tag": "l", "desc": "Idiom or fixed phrase"}},
	{{"token": "么", "tag": "y", "desc": "Sentence-final particle"}},
	{{"token": "？", "tag": "w", "desc": "Punctuation"}},
]

### Example 27:

**Text**: "夏禹王收九州之金，铸了九大鼎。"

**Output JSON**: 
[
    {{"token": "夏", "tag": "Tg", "desc": "Temporal morpheme"}},
	{{"token": "禹王", "tag": "nr", "desc": "Personal name"}},
	{{"token": "收", "tag": "v", "desc": "Verb"}},
	{{"token": "九州", "tag": "ns", "desc": "Place name"}},
	{{"token": "之", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "金", "tag": "Ng", "desc": "Noun morpheme"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "铸", "tag": "v", "desc": "Verb"}},
	{{"token": "了", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "九", "tag": "m", "desc": "Numeral"}},
	{{"token": "大", "tag": "a", "desc": "Adjective"}},
	{{"token": "鼎", "tag": "n", "desc": "Common noun"}},
	{{"token": "。", "tag": "w", "desc": "Punctuation"}},
]

### Example 28:

**Text**: "《左传》上说：‘楚子观兵于周疆。"

**Output JSON**: 
[
    {{"token": "《", "tag": "w", "desc": "Punctuation"}},
	{{"token": "左传", "tag": "nz", "desc": "Other proper noun"}},
	{{"token": "》", "tag": "w", "desc": "Punctuation"}},
	{{"token": "上", "tag": "f", "desc": "Directional/Localizer"}},
	{{"token": "说", "tag": "v", "desc": "Verb"}},
	{{"token": "：", "tag": "w", "desc": "Punctuation"}},
	{{"token": "‘", "tag": "w", "desc": "Punctuation"}},
	{{"token": "楚子", "tag": "nr", "desc": "Personal name"}},
	{{"token": "观", "tag": "Vg", "desc": "Verb morpheme"}},
	{{"token": "兵", "tag": "n", "desc": "Common noun"}},
	{{"token": "于", "tag": "p", "desc": "Preposition"}},
	{{"token": "周疆", "tag": "n", "desc": "Common noun"}},
	{{"token": "。", "tag": "w", "desc": "Punctuation"}},
]

### Example 29:

**Text**: "定王使王孙满劳楚子。"

**Output JSON**: 
[
    {{"token": "定王", "tag": "nr", "desc": "Personal name"}},
	{{"token": "使", "tag": "v", "desc": "Verb"}},
	{{"token": "王孙满", "tag": "nr", "desc": "Personal name"}},
	{{"token": "劳", "tag": "Vg", "desc": "Verb morpheme"}},
	{{"token": "楚子", "tag": "nr", "desc": "Personal name"}},
	{{"token": "。", "tag": "w", "desc": "Punctuation"}},
]

### Example 30:

**Text**: "楚子问鼎之大小轻重焉。’"

**Output JSON**: 
[
    {{"token": "楚子", "tag": "nr", "desc": "Personal name"}},
	{{"token": "问", "tag": "v", "desc": "Verb"}},
	{{"token": "鼎", "tag": "n", "desc": "Common noun"}},
	{{"token": "之", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "大小", "tag": "n", "desc": "Common noun"}},
	{{"token": "轻重", "tag": "n", "desc": "Common noun"}},
	{{"token": "焉", "tag": "y", "desc": "Sentence-final particle"}},
	{{"token": "。", "tag": "w", "desc": "Punctuation"}},
	{{"token": "’", "tag": "w", "desc": "Punctuation"}},
]

### Example 31:

**Text**: "只有天下之主，方能保有九鼎。"

**Output JSON**: 
[
    {{"token": "只", "tag": "d", "desc": "Adverb"}},
	{{"token": "有", "tag": "v", "desc": "Verb"}},
	{{"token": "天下", "tag": "n", "desc": "Common noun"}},
	{{"token": "之", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "主", "tag": "Ng", "desc": "Noun morpheme"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "方", "tag": "d", "desc": "Adverb"}},
	{{"token": "能", "tag": "v", "desc": "Verb"}},
	{{"token": "保有", "tag": "v", "desc": "Verb"}},
	{{"token": "九鼎", "tag": "nz", "desc": "Other proper noun"}},
	{{"token": "。", "tag": "w", "desc": "Punctuation"}},
]

### Example 32:

**Text**: "楚子只是楚国的诸侯，他问鼎的轻重大小，便是心存不轨，想取周王之位而代之。”"

**Output JSON**: 
[
    {{"token": "楚子", "tag": "nr", "desc": "Personal name"}},
	{{"token": "只", "tag": "d", "desc": "Adverb"}},
	{{"token": "是", "tag": "v", "desc": "Verb"}},
	{{"token": "楚国", "tag": "ns", "desc": "Place name"}},
	{{"token": "的", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "诸侯", "tag": "n", "desc": "Common Noun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "他", "tag": "r", "desc": "Pronoun"}},
	{{"token": "问", "tag": "v", "desc": "Verb"}},
	{{"token": "鼎", "tag": "n", "desc": "Common noun"}},
	{{"token": "的", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "轻重", "tag": "n", "desc": "Common noun"}},
	{{"token": "大小", "tag": "n", "desc": "Common noun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "便", "tag": "d", "desc": "Adverb"}},
	{{"token": "是", "tag": "v", "desc": "Verb"}},
	{{"token": "心存不轨", "tag": "i", "desc": "Idiom"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "想", "tag": "v", "desc": "Verb"}},
	{{"token": "取", "tag": "v", "desc": "Verb"}},
	{{"token": "周王", "tag": "nr", "desc": "Personal name"}},
	{{"token": "之", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "位", "tag": "Ng", "desc": "Noun morpheme"}},
	{{"token": "而", "tag": "c", "desc": "Conjunction"}},
	{{"token": "代", "tag": "v", "desc": "Verb"}},
	{{"token": "之", "tag": "r", "desc": "Pronoun"}},
	{{"token": "。", "tag": "w", "desc": "Punctuation"}},
	{{"token": "”", "tag": "w", "desc": "Punctuation"}},
]

### Example 33:

**Text**: "‘未知鹿死谁手’，就是不知哪一个做成了皇帝。”"

**Output JSON**: 
[
    {{"token": "‘", "tag": "w", "desc": "Punctuation"}},
	{{"token": "未", "tag": "d", "desc": "Adverb"}},
	{{"token": "知", "tag": "v", "desc": "Verb"}},
	{{"token": "鹿死谁手", "tag": "i", "desc": "Idiom"}},
	{{"token": "’", "tag": "w", "desc": "Punctuation"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "就是", "tag": "v", "desc": "Verb"}},
	{{"token": "不", "tag": "d", "desc": "Adverb"}},
	{{"token": "知", "tag": "v", "desc": "Verb"}},
	{{"token": "哪", "tag": "r", "desc": "Pronoun"}},
	{{"token": "一个", "tag": "m", "desc": "Numeral"}},
	{{"token": "做成", "tag": "v", "desc": "Verb"}},
	{{"token": "了", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "皇帝", "tag": "n", "desc": "Common noun"}},
	{{"token": "。", "tag": "w", "desc": "Punctuation"}},
	{{"token": "”", "tag": "w", "desc": "Punctuation"}},
]

### Example 34:

**Text**: "到得后来，‘问鼎’、‘逐鹿’，这四个字，也可借用于别处，但原来的出典，是专指做皇帝而言。”"

**Output JSON**: 
[
    {{"token": "到得", "tag": "v", "desc": "Verb"}},
	{{"token": "后来", "tag": "t", "desc": "Time word/Temporal noun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "‘", "tag": "w", "desc": "Punctuation"}},
	{{"token": "问鼎", "tag": "v", "desc": "verb"}},
	{{"token": "’", "tag": "w", "desc": "Punctuation"}},
	{{"token": "、", "tag": "w", "desc": "Punctuation"}},
	{{"token": "‘", "tag": "w", "desc": "Punctuation"}},
	{{"token": "逐鹿", "tag": "v", "desc": "Verb"}},
	{{"token": "’", "tag": "w", "desc": "Punctuation"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "这", "tag": "r", "desc": "Pronoun"}},
	{{"token": "四", "tag": "m", "desc": "Numeral"}},
	{{"token": "个", "tag": "q", "desc": "Classifier/Measure"}},
	{{"token": "字", "tag": "n", "desc": "Common noun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "也", "tag": "d", "desc": "Adverb"}},
	{{"token": "可", "tag": "v", "desc": "Verb"}},
	{{"token": "借用", "tag": "v", "desc": "Verb"}},
	{{"token": "于", "tag": "p", "desc": "Preposition"}},
	{{"token": "别处", "tag": "r", "desc": "Pronoun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "但", "tag": "c", "desc": "Conjunction"}},
	{{"token": "原来", "tag": "b", "desc": "Distinguishing word"}},
	{{"token": "的", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "出典", "tag": "n", "desc": "Common noun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "是", "tag": "v", "desc": "Verb"}},
	{{"token": "专", "tag": "d", "desc": "Adverb"}},
	{{"token": "指", "tag": "v", "desc": "Verb"}},
	{{"token": "做", "tag": "v", "desc": "Verb"}},
	{{"token": "皇帝", "tag": "n", "desc": "Common noun"}},
	{{"token": "而", "tag": "c", "desc": "Conjunction"}},
	{{"token": "言", "tag": "Vg", "desc": "Verb morpheme"}},
	{{"token": "。", "tag": "w", "desc": "Punctuation"}},
]

### Example 35:

**Text**: "说到这里，叹了口气，道：“咱们做百姓的，总是死路一条。"

**Output JSON**: 
[
    {{"token": "说", "tag": "v", "desc": "Verb"}},
	{{"token": "到", "tag": "v", "desc": "Verb"}},
	{{"token": "这里", "tag": "r", "desc": "Pronoun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "叹", "tag": "v", "desc": "Verb"}},
	{{"token": "了", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "口", "tag": "q", "desc": "Classifier/Measure"}},
	{{"token": "气", "tag": "n", "desc": "Common noun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "道", "tag": "v", "desc": "Verb"}},
	{{"token": "：", "tag": "w", "desc": "Punctuation"}},
	{{"token": "“", "tag": "w", "desc": "Punctuation"}},
	{{"token": "咱们", "tag": "r", "desc": "Pronoun"}},
	{{"token": "做", "tag": "v", "desc": "Verb"}},
	{{"token": "百姓", "tag": "n", "desc": "Common noun"}},
	{{"token": "的", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "总是", "tag": "d", "desc": "Adverb"}},
	{{"token": "死路一条", "tag": "l", "desc": "Idiom or fixed phrase"}},
	{{"token": "。", "tag": "w", "desc": "Punctuation"}},
]

### Example 36:

**Text**: "他说着走到窗边，向窗外望去， 只见天色沉沉的，似要下雪，叹道：“老天爷何其不仁，数百个无辜之人，在这冰霜遍地的道上行走。"

**Output JSON**: 
[
    {{"token": "他", "tag": "r", "desc": "Pronoun"}},
	{{"token": "说", "tag": "v", "desc": "Verb"}},
	{{"token": "着", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "走", "tag": "v", "desc": "Verb"}},
	{{"token": "到", "tag": "v", "desc": "Verb"}},
	{{"token": "窗", "tag": "n", "desc": "Common noun"}},
	{{"token": "边", "tag": "f", "desc": "Directional/Localizer"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "向", "tag": "p", "desc": "Preposition"}},
	{{"token": "窗外", "tag": "s", "desc": "Space word/Locative"}},
	{{"token": "望", "tag": "v", "desc": "Verb"}},
	{{"token": "去", "tag": "v", "desc": "Verb"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "只", "tag": "d", "desc": "Adverb"}},
	{{"token": "见", "tag": "v", "desc": "Verb"}},
	{{"token": "天色", "tag": "n", "desc": "Common noun"}},
	{{"token": "沉沉", "tag": "z", "desc": "Descriptive word/Stative verb"}},
	{{"token": "的", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "似", "tag": "d", "desc": "Adverb"}},
	{{"token": "要", "tag": "v", "desc": "Verb"}},
	{{"token": "下雪", "tag": "v", "desc": "Verb"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "叹", "tag": "v", "desc": "Verb"}},
	{{"token": "道", "tag": "v", "desc": "Verb"}},
	{{"token": "：", "tag": "w", "desc": "Punctuation"}},
	{{"token": "“", "tag": "w", "desc": "Punctuation"}},
	{{"token": "老天爷", "tag": "n", "desc": "Common noun"}},
	{{"token": "何其", "tag": "d", "desc": "Adverb"}},
	{{"token": "不", "tag": "d", "desc": "Adverb"}},
	{{"token": "仁", "tag": "Ag", "desc": "Adjectival morpheme"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "数百", "tag": "m", "desc": "Numeral"}},
	{{"token": "个", "tag": "q", "desc": "Classifier/Measure"}},
	{{"token": "无辜", "tag": "a", "desc": "Adjective"}},
	{{"token": "之", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "人", "tag": "n", "desc": "Common noun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "在", "tag": "p", "desc": "Preposition"}},
	{{"token": "这", "tag": "r", "desc": "Pronoun"}},
	{{"token": "冰霜", "tag": "n", "desc": "Common noun"}},
	{{"token": "遍地", "tag": "v", "desc": "Verb"}},
	{{"token": "的", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "道上", "tag": "s", "desc": "Space word/Locative"}},
	{{"token": "行走", "tag": "v", "desc": "Verb"}},
]

### Example 37:

**Text**: "下起雪来，可又多受一番折磨了。”"

**Output JSON**: 
[
    {{"token": "下", "tag": "v", "desc": "Verb"}},
	{{"token": "起", "tag": "v", "desc": "Verb"}},
	{{"token": "雪", "tag": "n", "desc": "Common noun"}},
	{{"token": "来", "tag": "v", "desc": "Verb"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "可", "tag": "d", "desc": "Adverb"}},
	{{"token": "又", "tag": "d", "desc": "Adverb"}},
	{{"token": "多", "tag": "ad", "desc": "Adjective as adverbial"}},
	{{"token": "受", "tag": "v", "desc": "Verb"}},
	{{"token": "一", "tag": "m", "desc": "Numeral"}},
	{{"token": "番", "tag": "q", "desc": "Classifier/Measure"}},
	{{"token": "折磨", "tag": "vn", "desc": "Verb as noun"}},
	{{"token": "了", "tag": "y", "desc": "Sentence-final particle"}},
	{{"token": "。", "tag": "w", "desc": "Punctuation"}},
	{{"token": "”", "tag": "w", "desc": "Punctuation"}},
]

### Example 38:

**Text**: "忽见南边大道上两个人戴着斗笠，并肩而来，走到近处，认出了面貌。"

**Output JSON**: 
[
    {{"token": "忽", "tag": "d", "desc": "Adverb"}},
	{{"token": "见", "tag": "v", "desc": "Verb"}},
	{{"token": "南边", "tag": "f", "desc": "Directional/Localizer"}},
	{{"token": "大道", "tag": "n", "desc": "Common noun"}},
	{{"token": "上", "tag": "f", "desc": "Directional/Localizer"}},
	{{"token": "两", "tag": "m", "desc": "Numeral"}},
	{{"token": "个", "tag": "q", "desc": "Classifier/Measure"}},
	{{"token": "人", "tag": "n", "desc": "Common noun"}},
	{{"token": "戴", "tag": "v", "desc": "Verb"}},
	{{"token": "着", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "斗笠", "tag": "n", "desc": "Common noun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "并肩", "tag": "d", "desc": "Adverb"}},
	{{"token": "而", "tag": "c", "desc": "Conjunction"}},
	{{"token": "来", "tag": "v", "desc": "verb"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "走", "tag": "v", "desc": "Verb"}},
	{{"token": "到", "tag": "v", "desc": "Verb"}},
	{{"token": "近处", "tag": "s", "desc": "Space word/Locative"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "认出", "tag": "v", "desc": "Verb"}},
	{{"token": "了", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "面貌", "tag": "n", "desc": "Common noun"}},
    {{"token": "。", "tag": "w", "desc": "Punctuation"}},
]

### Example 39:

**Text**: "收你为徒，只怕是我生平所作的一件大错事。"

**Output JSON**: 
[
    {{"token": "收", "tag": "v", "desc": "Verb"}},
	{{"token": "你", "tag": "r", "desc": "Pronoun"}},
	{{"token": "为", "tag": "v", "desc": "Verb"}},
	{{"token": "徒", "tag": "Ng", "desc": "Noun morpheme"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "只怕", "tag": "vd", "desc": Verb as adverbial"}},
	{{"token": "是", "tag": "v", "desc": "Verb"}},
	{{"token": "我", "tag": "r", "desc": "Pronoun"}},
	{{"token": "生平", "tag": "t", "desc": "Time word/Temporal noun"}},
	{{"token": "所", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "作", "tag": "v", "desc": "Verb"}},
	{{"token": "的", "tag": "u", "desc": "Auxiliary/Particle"}},
	{{"token": "一", "tag": "m", "desc": "Numeral"}},
	{{"token": "件", "tag": "q", "desc": "Classifier/Measure"}},
	{{"token": "大", "tag": "a", "desc": "Adjective"}},
	{{"token": "错事", "tag": "n", "desc": "Common noun"}},
	{{"token": "。", "tag": "w", "desc": "Punctuation"}},
]

### Example 40:

**Text**: "韦小宝听他接连提到皇上，心念一动：“难道这里是皇宫？"

**Output JSON**: 
[
    {{"token": "韦小宝", "tag": "nr", "desc": "Personal name"}},
	{{"token": "听", "tag": "v", "desc": "Verb"}},
	{{"token": "他", "tag": "r", "desc": "Pronoun"}},
	{{"token": "接连", "tag": "d", "desc": "Adverb"}},
	{{"token": "提到", "tag": "v", "desc": "Verb"}},
	{{"token": "皇上", "tag": "n", "desc": "Common noun"}},
	{{"token": "，", "tag": "w", "desc": "Punctuation"}},
	{{"token": "心念", "tag": "n", "desc": "Common noun"}},
	{{"token": "一", "tag": "d", "desc": "Adverb"}},
	{{"token": "动", "tag": "v", "desc": "Verb"}},
	{{"token": "：", "tag": "w", "desc": "Punctuation"}},
	{{"token": "“", "tag": "w", "desc": "Punctuation"}},
	{{"token": "难道", "tag": "d", "desc": "Adverb"}},
	{{"token": "这里", "tag": "r", "desc": "Pronoun"}},
	{{"token": "是", "tag": "v", "desc": "Verb"}},
	{{"token": "皇宫", "tag": "n", "desc": "Common noun"}},
	{{"token": "？", "tag": "w", "desc": "Punctuation"}},
]
"""

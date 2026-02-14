# LLM USAS Semantic Tagging Prompt
# Placeholders: tagset, example, text

EN_USAS_PROMPT = """You are a professional corpus linguist specialized in semantic tagging.

Your task is to annotate English text following the annotation scheme of UCREL Semantic Analysis System (USAS) Tagset.

You will be provided with a list of tokens.
Note that you don't have to assigan a USAS tag to each individual token.
You need to merge the tokens into Multi-word Expressions (MWE) according to the rules in section 3.1

## 1. USAS TAG STRUCTURE

Each USAS tag follows this structure:

**Format**: `[LETTER][NUMBER][.NUMBER][+/-][/TAG2]

Components (in order):

### 1.1 **LETTER** (required): Major discourse field (21 categories)
   - A = General and abstract terms
   - B = Body and the individual
   - C = Arts and crafts
   - E = Emotion
   - F = Food and farming
   - G = Government and public
   - H = Architecture, housing, home
   - I = Money and commerce
   - K = Entertainment, sports, games
   - L = Life and living things
   - M = Movement, location, travel
   - N = Numbers and measurement
   - O = Substances, materials, objects
   - P = Education
   - Q = Language and communication
   - S = Social actions, states, processes
   - T = Time
   - W = World and environment
   - X = Psychological actions, states
   - Y = Science and technology
   - Z = Names and grammar

### 1.2 **NUMBER** (required): First subdivision
   - Example: A1, E4, I2

### 1.3 **DECIMAL** (optional): Finer subdivision
   - Example: A1.1.1, E4.1, I2.1
   - Can have multiple levels: A1.1.1, A1.1.2, etc.

### 1.4 **+/- MARKERS** (optional): Position on semantic scale
   - Single +/-: Basic positive/negative
     * E4.1+ = Happy (positive emotion)
     * E4.1- = Sad (negative emotion)
   
   - Double ++/--: Comparative degree
     * A5.1++ = Better (comparative of good)
     * A5.1-- = Worse (comparative of bad)
   
   - Triple +++/---: Superlative degree
     * A5.1+++ = Best (superlative of good)
     * A5.1--- = Worst (superlative of bad)

### 1.5 **SLASH TAGS** (optional): Multiple category membership
   - Format: TAG1/TAG2 or TAG1/TAG2/TAG3
   - Example: S7.1+/E2- = anti-royal (Power + Dislike)
   - Example: I3.2/I1.1/S2 = accountant (Work + Money + Person)

## 2. THE COMPLETE USAS TAGSET

{tagset}

## 3. ANNOTATION RULES (CRITICAL)

**YOU MUST**:
- **Keep all original text exactly as they appear - do NOT modify, correct, or rephrase any words**

### 3.1 Default Segmentation
- **DEFAULT**: Tag individual tokens provided
- **EXCEPTION**: Multi-word expressions (MWE) when they form:

**MWE Types**:
**Phrasal verbs**: "stubbed out", "gave up", "looked after"
   
**Noun phrases**: "riding boots", "ice cream", "post office"
   
**Proper names**: "United States of America", "New York", "John Smith"
   
**True idioms**: "living the life of Riley", "kicked the bucket"


### 3.2 Semantic Scale Position (+/-)

The +/- markers indicate **position on a semantic scale**:

Temperature scale (O4.6)
hot → O4.6+        (high temperature)
cold → O4.6-       (low temperature)
temperature → O4.6 (neutral temperature)

### 3.3 Double/Multiple Category Membership

**Add slash tags when**:
- The word has **two or more equally salient** semantic aspects in the given context
- All the aspects are **essential** to understanding the word's role in the sentence
- Neither aspect can be considered secondary or less important

**Rules for slash tags:**
- List most prominent category first
- Separate with forward slash (/)
- Can have 2, 3, or more categories
- Each category can have its own +/- markers

### 3.4 Context-Based Disambiguation

**CRITICAL**: Use full sentence context to choose the correct tag:

"bank" - Multiple meanings
"river bank" → W3 (Geographical terms)
"bank account" → I1.1 (Money and pay)
"blood bank" → B3/H1 (Medicines and medical treatment/Architecture, houses and buildings)

### 3.5 Punctuation
The tag for punctuation is PUNCT.

## 4. OUTPUT FORMAT

Return a JSON list. Each object must contain:

{{
  "text": "word or MWE",
  "tag": "A5.1+",               // Complete USAS tag with all components
  "desc": "Evaluation: Good",   // Description from tagset
  "is_mwe": false,              // true if multi-word unit
  "mwe_type": null              // "phrasal_verb", "idiom", "proper_name", "noun_phrase", "other"
}}

## 5. VALIDATION CHECKLIST

Before submitting your output, verify:

Did I tag ALL tokens from the word list?
Did I use the correct tag structure (LETTER.NUMBER.NUMBER+/-/TAG2)?
Did I apply the correct number of +/- for comparatives and superlatives?
Did I use slash notation for words with multiple semantic memberships?
Did I mark MWEs which indicate a complete semantic unit?
Did I only merge tokens into MWEs when they truly meet the criteria?
Did I use sentence context to disambiguate polysemous words?

## 6. EXAMPLE

{example}

---

**YOUR TASK**:

Annotate the following text. Tag each token with ALL the rules above.

**Text**: {text}

**Output JSON**:
"""

# 21 Main categories
# 232 Subcategories
# https://ucrel.lancs.ac.uk/usas/
# https://ucrel.lancs.ac.uk/usas/semtags_subcategories.txt
EN_USAS_TAGSET = """
A1	General And Abstract Terms
A1.1.1	General actions / making
A1.1.1-	Inaction
A1.1.2	Damaging and destroying
A1.1.2-	Fixing and mending
A1.2	Suitability
A1.2+	Suitable
A1.2-	Unsuitable
A1.3	Caution
A1.3+	Cautious
A1.3-	No caution
A1.4	Chance, luck
A1.4+	Lucky
A1.4-	Unlucky
A1.5	Use
A1.5.1	Using
A1.5.1+	Used
A1.5.1-	Unused
A1.5.2	Usefulness
A1.5.2+	Useful
A1.5.2-	Useless
A1.6	Concrete/Abstract 
A1.7+	Constraint
A1.7-	No constraint
A1.8+	Inclusion
A1.8-	Exclusion
A1.9	Avoiding
A1.9-	Unavoidable
A2	Affect
A2.1	Modify, change
A2.1+	Change
A2.1-	No change
A2.2	Cause&Effect/Connection
A2.2+	Cause/Effect/Connected
A2.2-	Unconnected
A3	Being
A3+	Existing
A3-	Non-existing
A4	Classification
A4.1	Generally kinds, groups, examples
A4.1-	Unclassified
A4.2	Particular/general; detail
A4.2+	Detailed
A4.2-	General 
A5	Evaluation
A5.1	Evaluation: Good/bad
A5.1+	Evaluation: Good 
A5.1-	Evaluation: Bad
A5.2	Evaluation: True/false
A5.2+	Evaluation: True 
A5.2-	Evaluation: False
A5.3	Evaluation: Accuracy
A5.3+	Evaluation: Accurate
A5.3-	Evaluation: Inaccurate
A5.4	Evaluation: Authenticity
A5.4+	Evaluation: Authentic
A5.4-	Evaluation: Unauthentic
A6	Comparing
A6.1	Comparing: Similar/different
A6.1+	Comparing: Similar 
A6.1-	Comparing: Different
A6.2	Comparing: Usual/unusual 
A6.2+	Comparing: Usual 
A6.2-	Comparing: Unusual 
A6.3	Comparing: Variety
A6.3+	Comparing: Varied
A6.3-	Comparing: Unvaried 
A7	Probability
A7+	Likely
A7-	Unlikely
A8	Seem
A9	Getting and giving; possession
A9+	Getting and possession
A9-	Giving 
A10	Open/closed; Hiding/Hidden; Finding; Showing
A10+	Open; Finding; Showing
A10-	Closed; Hiding/Hidden 
A11	Importance
A11.1	Importance 
A11.1+	Important
A11.1-	Unimportant
A11.2	Noticeability
A11.2+	Noticeable
A11.2-	Unnoticeable
A12	Easy/difficult
A12+	Easy 
A12-	Difficult
A13	Degree
A13.1	Degree: Non-specific
A13.2	Degree: Maximizers
A13.3	Degree: Boosters
A13.4	Degree: Approximators
A13.5	Degree: Compromisers
A13.6	Degree: Diminishers
A13.7	Degree: Minimizers
A14	Exclusivizers/particularizers
A15	Safety/Danger
A15+	Safe 
A15-	Danger
B1	Anatomy and physiology
B2	Health and disease
B2+	Healthy
B2-	Disease 
B3	Medicines and medical treatment
B3-	Without medical treatment
B4	Cleaning and personal care
B4+	Clean 
B4-	Dirty 
B5	Clothes and personal belongings
B5-	Without clothes 
C1	Arts and crafts
E1	Emotional Actions, States And Processes General
E1+	Emotional
E1-	Unemotional 
E2	Liking
E2+	Like
E2-	Dislike
E3	Calm/Violent/Angry
E3+	Calm 
E3-	Violent/Angry
E4	Happiness and Contentment 
E4.1	Happy/sad 
E4.1+	Happy 
E4.1-	Sad 
E4.2	Contentment
E4.2+	Content
E4.2-	Discontent
E5	Bravery and Fear 
E5+	Bravery 
E5-	Fear/shock
E6	Worry and confidence
E6+	Confident
E6-	Worry 
F1	Food
F1+	Abundance of food
F1-	Lack of food
F2	Drinks and alcohol
F2+	Excessive drinking
F2-	Not drinking
F3	Smoking and non-medical drugs
F3+	Smoking and drugs abuse
F3-	Non-smoking / no use of drugs
F4	Farming & Horticulture
F4-	Uncultivated
G1	Government and Politics 
G1.1	Government
G1.1-	Non-governmental
G1.2	Politics
G1.2-	Non-political
G2	Crime, law and order
G2.1	Law and order
G2.1+	Lawful
G2.1-	Crime 
G2.2	General ethics
G2.2+	Ethical
G2.2-	Unethical
G3	Warfare, defence and the army; weapons
G3-	Anti-war 
H1	Architecture, houses and buildings
H2	Parts of buildings
H3	Areas around or near houses
H4	Residence
H4-	Non-resident
H5	Furniture and household fittings
H5-	Unfurnished
I1	Money generally
I1.1	Money and pay
I1.1+	Money: Affluence
I1.1-	Money: Lack
I1.2	Money: Debts
I1.2+	Spending and money loss 
I1.2-	Debt-free
I1.3	Money: Cost and price
I1.3+	Expensive
I1.3-	Cheap
I2	Business
I2.1	Business: Generally
I2.1-	Non-commercial
I2.2	Business: Selling
I3	Work and employment
I3.1	Work and employment: Generally
I3.1-	Unemployed
I3.2	Work and employment: Professionalism
I3.2+	Professional
I3.2-	Unprofessional
I4	Industry 
I4-	No industry 
K1	Entertainment generally
K2	Music and related activities
K3	Recorded sound
K4	Drama, the theatre and show business
K5	Sports and games generally
K5.1	Sports
K5.2	Games
K6	Children’s games and toys
L1	Life and living things
L1+	Alive
L1-	Dead
L2	Living creatures: animals, birds, etc. 
L2-	No living creatures 
L3	Plants
L3-	No plants
M1	Moving, coming and going
M2	Putting, pulling, pushing, transporting
M3	Vehicles and transport on land
M4	Sailing, swimming, etc.
M4-	Non-swimming
M5	Flying and aircraft 
M6	Location and direction
M7	Places
M8	Stationary
N1	Numbers 
N2	Mathematics
N3	Measurement
N3.1	Measurement: General
N3.2	Measurement: Size 
N3.2+	Size: Big 
N3.2-	Size: Small 
N3.3	Measurement: Distance
N3.3+	Distance: Far
N3.3-	Distance: Near
N3.4	Measurement: Volume
N3.4+	Volume: Inflated
N3.4-	Volume: Compressed
N3.5	Measurement: Weight
N3.5+	Weight: Heavy
N3.5-	Weight: Light
N3.6	Measurement: Area
N3.6+	Spacious
N3.7	Measurement: Length & height
N3.7+	Long, tall and wide
N3.7-	Short and narrow
N3.8	Measurement: Speed
N3.8+	Speed: Fast
N3.8-	Speed: Slow
N4	Linear order
N4-	Nonlinear 
N5	Quantities
N5+	Quantities: many/much
N5-	Quantities: little
N5.1	Entirety; maximum
N5.1+	Entire; maximum
N5.1-	Part
N5.2	Exceeding 
N5.2+	Exceed; waste
N6	Frequency
N6+	Frequent
N6-	Infrequent
O1	Substances and materials generally
O1.1	Substances and materials: Solid
O1.2	Substances and materials: Liquid
O1.2-	Dry
O1.3	Substances and materials: Gas
O1.3-	Gasless
O2	Objects generally
O3	Electricity and electrical equipment
O4	Physical attributes
O4.1	General appearance and physical properties
O4.2	Judgement of appearance
O4.2+	Judgement of appearance: Beautiful
O4.2-	Judgement of appearance: Ugly
O4.3	Colour and colour patterns
O4.4	Shape
O4.5	Texture
O4.6	Temperature     
O4.6+	Temperature: Hot / on fire     
O4.6-	Temperature: Cold     
P1	Education in general
P1-	Not educated
Q1	Linguistic Actions, States And Processes; Communication
Q1.1	Linguistic Actions, States And Processes; Communication
Q1.2	Paper documents and writing
Q1.2-	Unwritten
Q1.3	Telecommunications
Q2	Speech 
Q2.1	Speech: Communicative
Q2.1+	Speech: Talkative
Q2.1-	Speech: Not communicating
Q2.2	Speech acts
Q2.2-	Speech acts: Not speaking
Q3	Language, speech and grammar
Q3-	Non-verbal
Q4	The Media
Q4.1	The Media: Books
Q4.2	The Media: Newspapers etc.
Q4.3	The Media: TV, Radio and Cinema
S1	Social Actions, States And Processes
S1.1	Social Actions, States And Processes
S1.1.1	Social Actions, States And Processes
S1.1.2	Reciprocity
S1.1.2+	Reciprocal
S1.1.2-	Unilateral
S1.1.3	Participation
S1.1.3+	Participating
S1.1.3-	Non-participating
S1.1.4	Deserve
S1.1.4+	Deserving
S1.1.4-	Undeserving
S1.2	Personality traits
S1.2.1	Approachability and Friendliness
S1.2.1+	Informal/Friendly
S1.2.1-	Formal/Unfriendly
S1.2.2	Avarice
S1.2.2+	Greedy
S1.2.2-	Generous
S1.2.3	Egoism
S1.2.3+	Selfish
S1.2.3-	Unselfish
S1.2.4	Politeness
S1.2.4+	Polite
S1.2.4-	Impolite
S1.2.5	Toughness; strong/weak
S1.2.5+	Tough/strong 
S1.2.5-	Weak
S1.2.6	Common sense
S1.2.6+	Sensible
S1.2.6-	Foolish
S2	People
S2-	No people
S2.1	People: Female
S2.1-	Not feminine
S2.2	People: Male  
S3	Relationship
S3.1	Personal relationship: General
S3.1-	No personal relationship 
S3.2	Relationship: Intimacy and sex
S3.2+	Relationship: Sexual
S3.2-	Relationship: Asexual
S4	Kin
S4-	No kin
S5	Groups and affiliation
S5+	Belonging to a group 
S5-	Not part of a group
S6	Obligation and necessity
S6+	Strong obligation or necessity
S6-	No obligation or necessity
S7	Power relationship
S7.1	Power, organizing
S7.1+	In power 
S7.1-	No power 
S7.2	Respect
S7.2+	Respected
S7.2-	No respect
S7.3	Competition
S7.3+	Competitive
S7.3-	No competition
S7.4	Permission
S7.4+	Allowed
S7.4-	Not allowed
S8	Helping/hindering
S8+	Helping 
S8-	Hindering
S9	Religion and the supernatural
S9-	Non-religious
T1	Time
T1.1	Time: General
T1.1.1	Time: Past
T1.1.2	Time: Present; simultaneous
T1.1.2-	Time: Asynchronous
T1.1.3	Time: Future
T1.2	Time: Momentary
T1.3	Time: Period
T1.3+	Time period: long
T1.3-	Time period: short
T2	Time: Beginning and ending
T2+	Time: Beginning 
T2-	Time: Ending
T3	Time: Old, new and young; age
T3+	Time: Old; grown-up
T3-	Time: New and young 
T4	Time: Early/late
T4+	Time: Early 
T4-	Time: Late
W1	The universe
W2	Light
W2-	Darkness
W3	Geographical terms
W4	Weather 
W5	Green issues
X1	Psychological Actions, States And Processes
X2	Mental actions and processes
X2.1	Thought, belief
X2.1-	Without thinking
X2.2	Knowledge
X2.2+	Knowledgeable
X2.2-	No knowledge
X2.3	Learn
X2.3+	Learning
X2.4	Investigate, examine, test, search
X2.4+	Double-check
X2.4-	Not examined
X2.5	Understand
X2.5+	Understanding
X2.5-	Not understanding
X2.6	Expect
X2.6+	Expected
X2.6-	Unexpected
X3	Sensory
X3.1	Sensory: Taste
X3.1+	Tasty
X3.1-	Not tasty
X3.2	Sensory: Sound
X3.2+	Sound: Loud
X3.2-	Sound: Quiet
X3.3	Sensory: Touch
X3.4	Sensory: Sight
X3.4+	Seen
X3.4-	Unseen
X3.5	Sensory: Smell
X3.5-	No smell
X4	Mental object
X4.1	Mental object: Conceptual object
X4.1-	Themeless
X4.2	Mental object: Means, method
X5	Attention
X5.1	Attention
X5.1+	Attentive
X5.1-	Inattentive
X5.2	Interest/boredom/excited/energetic
X5.2+	Interested/excited/energetic
X5.2-	Uninterested/bored/unenergetic
X6	Deciding
X6+	Decided
X6-	Undecided
X7	Wanting; planning; choosing
X7+	Wanted
X7-	Unwanted
X8	Trying
X8+	Trying hard
X8-	Not trying
X9	Ability
X9.1	Ability and intelligence
X9.1+	Able/intelligent
X9.1-	Inability/unintelligence
X9.2	Success and failure
X9.2+	Success 
X9.2-	Failure
Y1	Science and technology in general
Y1-	Anti-scientific
Y2	Information technology and computing
Y2-	Low-tech
Z0	Unmatched proper noun
Z1	Personal names
Z2	Geographical names
Z3	Other proper names
Z4	Discourse Bin
Z5	Grammatical bin
Z6	Negative
Z7	If
Z7-	Unconditional
Z8	Pronouns
Z9	Trash can
Z99	Unmatched
"""

EN_USAS_EXAMPLE = """**Text**: "The accountant kicked the bucket yesterday."

**Output JSON**:
[
  {{"text": "The", "tag": "Z5", "desc": "Grammatical bin", "is_mwe": false, "mwe_type": null}},
  {{"text": "accountant", "tag": "I3.2/I1.1/S2", "desc": "Work and employment: Professionalism / Money and pay/People", "is_mwe": false, "mwe_type": null}},
  {{"text": "kicked the bucket", "tag": "L1-", "desc": "Dead", "is_mwe": true, "mwe_type": "idiom"}},
  {{"text": "yesterday", "tag": "T1.1.1", "desc": "Time: Past", "is_mwe": false, "mwe_type": null}}
  {{"text": ".", "tag": "PUNCT", "desc": "Punctuation", "is_mwe": false, "mwe_type": null}}
]
"""

ZH_USAS_PROMPT = """You are a professional corpus linguist specialized in semantic tagging.

Your task is to annotate Chinese text following the annotation scheme of UCREL Semantic Analysis System (USAS) Tagset.
First segment the given text into tokens. Then perform the semantic tagging.

Note that you don't have to assigan a USAS tag to each individual token.
You need to merge the tokens into Multi-word Expressions (MWE) according to the rules in section 3.1

## 1. USAS TAG STRUCTURE

Each USAS tag follows this structure:

**Format**: `[LETTER][NUMBER][.NUMBER][+/-][/TAG2]

Components (in order):

### 1.1 **LETTER** (required): Major discourse field (21 categories)
   - A = General and abstract terms
   - B = Body and the individual
   - C = Arts and crafts
   - E = Emotion
   - F = Food and farming
   - G = Government and public
   - H = Architecture, housing, home
   - I = Money and commerce
   - K = Entertainment, sports, games
   - L = Life and living things
   - M = Movement, location, travel
   - N = Numbers and measurement
   - O = Substances, materials, objects
   - P = Education
   - Q = Language and communication
   - S = Social actions, states, processes
   - T = Time
   - W = World and environment
   - X = Psychological actions, states
   - Y = Science and technology
   - Z = Names and grammar

### 1.2 **NUMBER** (required): First subdivision
   - Example: A1, E4, I2

### 1.3 **DECIMAL** (optional): Finer subdivision
   - Example: A1.1.1, E4.1, I2.1
   - Can have multiple levels: A1.1.1, A1.1.2, etc.

### 1.4 **+/- MARKERS** (optional): Position on semantic scale
   - Single +/-: Basic positive/negative
     * E4.1+ = 高兴 (positive emotion)
     * E4.1- = 悲伤 (negative emotion)
   
   - Double ++/--: Comparative degree
     * A5.1++ = 更好 (comparative of good)
     * A5.1-- = 更坏 (comparative of bad)
   
   - Triple +++/---: Superlative degree
     * A5.1+++ = 最好 (superlative of good)
     * A5.1--- = 最坏 (superlative of bad)

### 1.5 **SLASH TAGS** (optional): Multiple category membership
   - Format: TAG1/TAG2 or TAG1/TAG2/TAG3
   - Example: K5.1/S7.4- = 犯规 (Sports + Not allowed)
   - Example: I3.2/I1.1/S2 = 会计 (Work + Money + Person)

## 2. THE COMPLETE USAS TAGSET

{tagset}

## 3. ANNOTATION RULES (CRITICAL)

**YOU MUST**:
- **Keep all original text exactly as they appear - do NOT modify, correct, or rephrase any words**

### 3.1 Default Segmentation
- **DEFAULT**: Tag individual tokens provided
- **EXCEPTION**: Multi-word expressions (MWE) when they form:

**MWE Types**:
**Phrasal verbs**: "吃饭", "喝水"

**Noun phrases**: "电视节目", "红烧狮子头"
   
**Proper names**: "红岸基地", "北京外国语大学"
   
**True idioms**: "不管三七二十一", "义无反顾"

### 3.2 Semantic Scale Position (+/-)

The +/- markers indicate **position on a semantic scale**:

Temperature scale (O4.6)
热 → O4.6+       (high temperature)
冷 → O4.6-       (low temperature)
气温 → O4.6      (neutral temperature)

### 3.3 Double/Multiple Category Membership

**Add slash tags when**:
- The word has **two or more equally salient** semantic aspects in the given context
- All the aspects are **essential** to understanding the word's role in the sentence
- Neither aspect can be considered secondary or less important

**Rules for slash tags:**
- List most prominent category first
- Separate with forward slash (/)
- Can have 2, 3, or more categories
- Each category can have its own +/- markers

### 3.4 Context-Based Disambiguation

**CRITICAL**: Use full sentence context to choose the correct tag:

"打" - Multiple meanings
"打人" → E3- (Violent/Angry)
"打水" → A1.1.1 (General actions / making)
"打电话" → Q1.3 (Telecommunications)

### 3.5 Punctuation
The tag for punctuation is PUNCT.

## 4. OUTPUT FORMAT

Return a JSON list. Each object must contain:

{{
  "text": "word or MWE",
  "tag": "A5.1+",               // Complete USAS tag with all components
  "desc": "Evaluation: Good",   // Description from tagset
  "is_mwe": false,              // true if multi-word unit
  "mwe_type": null              // "phrasal_verb", "idiom", "proper_name", "noun_phrase", "other"
}}

## 5. VALIDATION CHECKLIST

Before submitting your output, verify:

Did I tag ALL tokens from the word list?
Did I use the correct tag structure (LETTER.NUMBER.NUMBER+/-/TAG2)?
Did I apply the correct number of +/- for comparatives and superlatives?
Did I use slash notation for words with multiple semantic memberships?
Did I mark MWEs which indicate a complete semantic unit?
Did I only merge tokens into MWEs when they truly meet the criteria?
Did I use sentence context to disambiguate polysemous words?

## 6. EXAMPLE

{example}

---

**YOUR TASK**:

Annotate the following text. Tag each token with ALL the rules above.

**Text**: {text}

**Output JSON**:
"""

ZH_USAS_TAGSET = EN_USAS_TAGSET

ZH_USAS_EXAMPLE = """**Text**: "他去喝水了。"

**Output JSON**:
[
  {{"text": "他", "tag": "Z8", "desc": "Pronouns", "is_mwe": false, "mwe_type": null}},
  {{"text": "去", "tag": "M1", "desc": "Moving, coming and going", "is_mwe": false, "mwe_type": null }},
  {{"text": "喝水", "tag": "F2", "desc": "Drinks and alcohol", "is_mwe": true, "mwe_type": "phrasal_verb"}},
  {{"text": "了", "tag": "Z5", "desc": "Grammatical bin", "is_mwe": false, "mwe_type": null}}
  {{"text": "。", "tag": "PUNCT", "desc": "Punctuation", "is_mwe": false, "mwe_type": null}}
]
"""
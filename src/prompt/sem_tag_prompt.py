# LLM USAS Semantic Tagging Prompt
# Placeholders: tagset, example, text

EN_USAS_PROMPT = """You are a professional corpus linguist specialized in semantic tagging.

Your task is to annotate English text following the annotation scheme of UCREL Semantic Analysis System (USAS) Tagset.
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

### 3.1 English Multi-Word Expressions (MWE) Segmentation

- **DEFAULT**: Tag individual tokens
- **EXCEPTION**: Merge tokens into MWEs when they form a semantic unit that cannot be adequately captured by tagging each token separately

**English MWE Types (6 types)**:

#### (1) idiom — True Idioms
Fixed expressions where the overall meaning cannot be derived from the individual words.
Includes figurative expressions and conventional phrases.

Examples:
| MWE | Tag | Description |
|-----|-----|-------------|
| in the teeth of | A12- | Difficult (figurative: facing adversity) |
| kicked the bucket | L1- | Dead (idiom for dying) |
| living the life of Riley | E4.1+ | Happy (idiom for easy life) |
| give you something to cry about | E3-/Q2.2 | Violent / Speech acts (threat idiom) |

#### (2) phrasal_verb — Phrasal Verbs
Verb + particle (adverb/preposition) combinations where the meaning differs from
the sum of its parts, or where the combination forms a distinct semantic unit.

Also includes verb + auxiliary combinations (e.g., "was escorting") when they form
a unified semantic action.

Examples:
| MWE | Tag | Description |
|-----|-----|-------------|
| was escorting | M1/G2.1 | Moving / Law & order |
| shut up | Q2.2- | Speech acts: Not speaking |
| stop it | S8- | Hindering |
| gave up | A1.9 | Avoiding (surrender) |
| looked after | S8+ | Helping |

#### (3) compound_noun — Compound Nouns
Two or more words forming a lexicalized noun where the meaning is a fused unit.
High lexical cohesion — functions as a single lexical item.

Examples:
| MWE | Tag | Description |
|-----|-----|-------------|
| riding boots | B5/K5.1 | Clothes / Sports |
| ice cream | F1 | Food |
| post office | Q1.1/H1 | Communication / Building |
| farm house | F2/H1 | Farming / Building |
| blood bank | B3/H1 | Medicine / Building |

#### (4) noun_phrase — Descriptive Noun Phrases
Multi-word noun phrases where the modifier carries significant semantic content
that would be lost if tagged separately, but with lower cohesion than compound nouns.

Examples:
| MWE | Tag | Description |
|-----|-----|-------------|
| prison carts | G2.1-/M3 | Crime / Land transport |
| scholar class | P1/S5 | Education / Groups |
| coastal road | W3/M3 | Geography / Land transport |
| white-haired | B1/T3+ | Anatomy / Old |
| middle-aged | T3+ | Old; grown-up |
| baby girl | T3-/S2.1 | Young / Female |
| little boy | S2.2/T3- | Male / Young |
| middle years | T3+ | Old; grown-up |
| ten- or eleven-year-old | T3-/N1 | Young / Numbers |

#### (5) proper_name — Proper Names
Names of people, places, organizations, and other proper nouns.

Examples:
| MWE | Tag | Description |
|-----|-----|-------------|
| Yangtze River | W3/Z2 | Geographical terms / Geographical names |
| United States of America | Z2/G1.1 | Geographical names / Government |
| New York | Z2 | Geographical names |

#### (6) fixed_phrase — Fixed Phrases and Collocations
Multi-word adverbial, prepositional, or other set phrases that function as
a single semantic unit but do not fit the above categories.

Examples:
| MWE | Tag | Description |
|-----|-----|-------------|
| more or less | A13.4 | Approximators |
| in an undertone | X3.2-/Q2.2 | Sound: Quiet / Speech acts |
| for fear that | E5- | Fear |
| all of them | N5.1+ | Entire; maximum |
| more than | N5.2+ | Exceeding |

### 3.2 Semantic Scale Position (+/-)

The +/- markers indicate **position on a semantic scale**:

Temperature scale (O4.6):
hot → O4.6+        (high temperature)
cold → O4.6-       (low temperature)
temperature → O4.6 (neutral temperature)

### 3.3 Double/Multiple Category Membership (Slash Tags)

**Add slash tags when**:
- The word has **two or more equally salient** semantic aspects in the given context
- All aspects are **essential** to understanding the word's role in the sentence
- Neither aspect can be considered secondary or unimportant

**Rules for slash tags:**
- List most prominent category first
- Separate with forward slash (/)
- Can have 2, 3, or more categories
- Each category can have its own +/- markers

**Common patterns requiring slash tags:**

| Pattern | Example | Tag | Reason |
|---------|---------|-----|--------|
| Person + Role | soldiers | G3/S2 | Military + People |
| Person + Gender | man | S2.2 | Male (single tag sufficient) |
| Person + Age | old man | S2/T3+ | People + Old |
| Person + Gender + Age | young mother | S2.1/T3-/S4 | Female + Young + Kin |
| Object + Domain | prison carts | G2.1-/M3 | Crime + Land transport |
| Place + Name | Yangtze River | W3/Z2 | Geography + Name |
| Action + Emotion | kick (in anger) | E3-/B1 | Violence + Body |
| Group + Domain | detachment (military) | S5/G3 | Groups + Military |

### 3.4 Context-Based Disambiguation

**CRITICAL**: Use full sentence context to choose the correct tag.

"bank" - Multiple meanings:
"river bank" → W3 (Geographical terms)
"bank account" → I1.1 (Money and pay)

"bitter" - Multiple meanings:
"bitter wind" → O4.6- (Temperature: Cold)
"bitter taste" → X3.1 (Sensory: Taste)
"bitter words" → E4.1- (Sad)

"scene" - Multiple meanings:
"affected by this little scene" → X4.1 (Conceptual object — a situation witnessed)
"the theatre scene" → K4 (Drama, theatre)

"detachment" - Multiple meanings:
"a detachment of soldiers" → S5/G3 (Groups / Military — a military unit)
"emotional detachment" → X5.2- (Interest/boredom — emotional distance)

"occupied" - Multiple meanings:
"carts were occupied by women" → A1.8+ (Inclusion — filled/containing)
"occupied territory" → G3/S7.1+ (Military / Power — controlled)
"occupied with work" → X5.1 (Attention — busy)

"single" - Multiple meanings:
"a single prisoner" → N5.1- (Part — only one)
"single person" → S3.2 (Relationship: unmarried)

"startled" - Disambiguation:
"startled by violence" → E5- (Fear/shock — NOT X5.1+ Attentive)

### 3.5 Cross-Sentence Consistency

**CRITICAL**: The same word referring to the same entity should receive consistent tags throughout the text.

- "soldiers" should always be tagged G3/S2 (not sometimes G3 alone)
- "prison carts" should always be tagged G2.1-/M3 (not sometimes G2.1- alone)
- "baby girl" / "baby" / "little girl" referring to the same entity should maintain consistent gender and age tags
- Speech verbs ("said", "murmured", "added") should consistently use Q2.2

### 3.6 Punctuation
The tag for punctuation is PUNCT.

## 4. OUTPUT FORMAT

Return a JSON list. Each object must contain:

{{
  "text": "word or MWE",
  "tag": "A5.1+",               // Complete USAS tag with all components
  "desc": "Evaluation: Good",   // Description from tagset
  "is_mwe": false,              // true if multi-word unit
  "mwe_type": null              // One of: "idiom", "phrasal_verb", "compound_noun",
                                //         "noun_phrase", "proper_name", "fixed_phrase"
}}

## 5. VALIDATION CHECKLIST

Before submitting your output, verify:

Before submitting your output, verify:

- [ ] Did I tag ALL tokens from the text?
- [ ] Did I use the correct tag structure (LETTER.NUMBER.NUMBER+/-/TAG2)?
- [ ] Did I apply the correct number of +/- for comparatives and superlatives?
- [ ] Did I use slash notation for words with multiple semantic memberships?
- [ ] Did I correctly identify and classify MWEs using the 6 English MWE types?
- [ ] Did I only merge tokens into MWEs when they truly form a semantic unit?
- [ ] Did I use sentence context to disambiguate polysemous words?
- [ ] Did I maintain consistent tags for the same word/entity across the text?
- [ ] Did I use the most specific sub-tag available (e.g., N3.3 not just N3)?
- [ ] For person nouns, did I include relevant slash tags (gender S2.1/S2.2, age T3+/T3-, role P1/G3, group S5)?

## 6. EXAMPLES

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
A1.1.1	General actions/making
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
F3-	Non-smoking/no use of drugs
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
M2	Putting, taking, pulling, pushing, transporting
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
O4.6+	Temperature: Hot/on fire     
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

EN_USAS_EXAMPLE = """### Example 1:

**Text**: "Along a coastal road somewhere south of the Yangtze River, a detachment of soldiers, each of them armed with a halberd, was escorting a line of seven prison carts, trudging northwards in the teeth of a bitter wind."

**Output JSON**:
[
    {{'text': 'Along', 'tag': 'M6', 'desc': 'Location and direction', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'a', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'coastal road', 'tag': 'W3/M3', 'desc': 'Geographical terms / Vehicles and transport on land', 'is_mwe': True, 'mwe_type': 'noun_phrase'}},
	{{'text': 'somewhere', 'tag': 'M7', 'desc': 'Places', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'south', 'tag': 'M6', 'desc': 'Location and direction', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'of', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'the', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'Yangtze River', 'tag': 'W3/Z2', 'desc': 'Geographical terms / Geographical names', 'is_mwe': True, 'mwe_type': 'proper_name'}},
	{{'text': ',', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'a', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'detachment', 'tag': 'S5/G3', 'desc': 'Groups and affiliation / Warfare, defence and the army; weapons', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'of', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'soldiers', 'tag': 'G3/S2', 'desc': 'Warfare, defence and the army; weapons / People', 'is_mwe': False, 'mwe_type': None}},
	{{'text': ',', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'each', 'tag': 'N5.1+', 'desc': 'Entire; maximum', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'of', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'them', 'tag': 'Z8', 'desc': 'Pronouns', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'armed', 'tag': 'G3', 'desc': 'Warfare, defence and the army; weapons', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'with', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'a', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'halberd', 'tag': 'G3', 'desc': 'Warfare, defence and the army; weapons', 'is_mwe': False, 'mwe_type': None}},
	{{'text': ',', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'was escorting', 'tag': 'M1/G2.1', 'desc': 'Moving, coming and going / Law and order', 'is_mwe': True, 'mwe_type': 'phrasal_verb'}},
	{{'text': 'a', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'line', 'tag': 'N4', 'desc': 'Linear order', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'of', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'seven', 'tag': 'N1', 'desc': 'Numbers', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'prison carts', 'tag': 'G2.1-/M3', 'desc': 'Crime / Vehicles and transport on land', 'is_mwe': True, 'mwe_type': 'noun_phrase'}},
	{{'text': ',', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'trudging', 'tag': 'M1/A12-', 'desc': 'Moving, coming and going / Difficult', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'northwards', 'tag': 'M6', 'desc': 'Location and direction', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'in the teeth of', 'tag': 'A12-', 'desc': 'Difficult', 'is_mwe': True, 'mwe_type': 'idiom'}},
	{{'text': 'a', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'bitter', 'tag': 'O4.6-', 'desc': 'Temperature: Cold', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'wind', 'tag': 'W4', 'desc': 'Weather', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '.', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
]

### Example 2:

**Text**: "In each of the first three carts a single male prisoner was caged, identifiable by his dress as a member of the scholar class. One was a white-haired old man. The other two were men of middle years."

**Output JSON**:
[
    {{'text': 'In', 'tag': 'M6', 'desc': 'Location and direction', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'each', 'tag': 'N5.1+', 'desc': 'Entire; maximum', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'of', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'the', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'first', 'tag': 'N4', 'desc': 'Linear order', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'three', 'tag': 'N1', 'desc': 'Numbers', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'carts', 'tag': 'M3', 'desc': 'Vehicles and transport on land', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'a', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'single', 'tag': 'N5.1-', 'desc': 'Part', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'male', 'tag': 'S2.2', 'desc': 'People: Male', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'prisoner', 'tag': 'G2.1-/S2', 'desc': 'Crime / People', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'was', 'tag': 'A3+', 'desc': 'Existing', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'caged', 'tag': 'G2.1-', 'desc': 'Crime', 'is_mwe': False, 'mwe_type': None}},
	{{'text': ',', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'identifiable', 'tag': 'X2.2+', 'desc': 'Knowledgeable', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'by', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'his', 'tag': 'Z8', 'desc': 'Pronouns', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'dress', 'tag': 'B5', 'desc': 'Clothes and personal belongings', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'as', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'a', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'member', 'tag': 'S5+', 'desc': 'Belonging to a group', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'of', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'the', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'scholar class', 'tag': 'P1/S5', 'desc': 'Education in general / Groups and affiliation', 'is_mwe': True, 'mwe_type': 'noun_phrase'}},
	{{'text': '.', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'One', 'tag': 'N1', 'desc': 'Numbers', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'was', 'tag': 'A3+', 'desc': 'Existing', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'a', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'white-haired', 'tag': 'B1/T3+', 'desc': 'Anatomy and physiology / Time: Old; grown-up', 'is_mwe': True, 'mwe_type': 'noun_phrase'}},
	{{'text': 'old', 'tag': 'T3+', 'desc': 'Time: Old; grown-up', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'man', 'tag': 'S2.2', 'desc': 'People: Male', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '.', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'The', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'other', 'tag': 'A6.1-', 'desc': 'Comparing: Different', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'two', 'tag': 'N1', 'desc': 'Numbers', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'were', 'tag': 'A3+', 'desc': 'Existing', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'men', 'tag': 'S2.2', 'desc': 'People: Male', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'of', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'middle years', 'tag': 'T3+', 'desc': 'Time: Old; grown-up', 'is_mwe': True, 'mwe_type': 'noun_phrase'}},
	{{'text': '.', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
]

### Example 3:

**Text**: "The four rear carts were occupied by women, the last of them by a young mother holding a baby girl at her breast."

**Output JSON**:
[
    {{'text': 'The', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'four', 'tag': 'N1', 'desc': 'Numbers', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'rear', 'tag': 'M6', 'desc': 'Location and direction', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'carts', 'tag': 'M3', 'desc': 'Vehicles and transport on land', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'were occupied', 'tag': 'A1.8+', 'desc': 'Inclusion', 'is_mwe': True, 'mwe_type': 'phrasal_verb'}},
	{{'text': 'by', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'women', 'tag': 'S2.1', 'desc': 'People: Female', 'is_mwe': False, 'mwe_type': None}},
	{{'text': ',', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'the', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'last', 'tag': 'N4', 'desc': 'Linear order', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'of', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'them', 'tag': 'Z8', 'desc': 'Pronouns', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'by', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'a', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'young', 'tag': 'T3-', 'desc': 'Time: New and young', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'mother', 'tag': 'S4/S2.1', 'desc': 'Kin / People: Female', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'holding', 'tag': 'A9+', 'desc': 'Getting and possession', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'a', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'baby girl', 'tag': 'T3-/S2.1', 'desc': 'Time: New and young / People: Female', 'is_mwe': True, 'mwe_type': 'noun_phrase'}},
	{{'text': 'at', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'her', 'tag': 'Z8', 'desc': 'Pronouns', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'breast', 'tag': 'B1', 'desc': 'Anatomy and physiology', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '.', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
]

### Example 4:

**Text**: "The little girl was crying in a continuous wail which her mother's gentle words of comfort were powerless to console."

**Output JSON**:
[
    {{'text': 'The', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'little girl', 'tag': 'S2.1/T3-', 'desc': 'People: Female / Time: New and young', 'is_mwe': True, 'mwe_type': 'noun_phrase'}},
	{{'text': 'was', 'tag': 'A3+', 'desc': 'Existing', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'crying', 'tag': 'E4.1-', 'desc': 'Sad', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'in', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'a', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'continuous', 'tag': 'T1.3+/N6+', 'desc': 'Time period: long / Frequent', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'wail', 'tag': 'E4.1-/Q2.2', 'desc': 'Sad / Speech acts', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'which', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'her', 'tag': 'Z8', 'desc': 'Pronouns', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'mother', 'tag': 'S4/S2.1', 'desc': 'Kin / People: Female', 'is_mwe': False, 'mwe_type': None}},
	{{'text': "'s", 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'gentle', 'tag': 'S1.2.1+', 'desc': 'Informal/Friendly', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'words', 'tag': 'Q1.1', 'desc': 'Linguistic Actions, States And Processes; Communication', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'of', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'comfort', 'tag': 'E4.2+', 'desc': 'Content', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'were', 'tag': 'A3+', 'desc': 'Existing', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'powerless', 'tag': 'S7.1-/X9.1-', 'desc': 'No power / Inability/unintelligence', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'to', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'console', 'tag': 'E4.2+', 'desc': 'Content', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '.', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
]

### Example 5:

**Text**: "One of the soldiers marching alongside, irritated by the baby's crying, aimed a mighty kick at the cart. 'Stop it! Shut up!"

**Output JSON**:
[
    {{'text': 'One', 'tag': 'N1', 'desc': 'Numbers', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'of', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'the', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'soldiers', 'tag': 'G3/S2', 'desc': 'Warfare, defence and the army; weapons / People', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'marching', 'tag': 'M1', 'desc': 'Moving, coming and going', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'alongside', 'tag': 'M6', 'desc': 'Location and direction', 'is_mwe': False, 'mwe_type': None}},
	{{'text': ',', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'irritated', 'tag': 'E3-', 'desc': 'Violent/Angry', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'by', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'the', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': "baby's", 'tag': 'S2/T3-', 'desc': 'People / Time: New and young', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'crying', 'tag': 'E4.1-', 'desc': 'Sad ', 'is_mwe': False, 'mwe_type': None}},
	{{'text': ',', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'aimed', 'tag': 'M6/A1.1.1', 'desc': 'Location and direction / General actions/making', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'a', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'mighty', 'tag': 'A13.3', 'desc': 'Degree: Boosters', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'kick', 'tag': 'E3-/B1', 'desc': 'Violent/Angry / Anatomy and physiology', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'at', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'the', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'cart', 'tag': 'M3', 'desc': 'Vehicles and transport on land', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '.', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': "'", 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'Stop it', 'tag': 'S8-', 'desc': 'Hindering', 'is_mwe': True, 'mwe_type': 'phrasal_verb'}},
	{{'text': '!', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'Shut up', 'tag': 'Q2.2-', 'desc': 'Speech acts: Not speaking', 'is_mwe': True, 'mwe_type': 'phrasal_verb'}},
	{{'text': '!', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '"', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
]

### Example 6: 

**Text**: "Or I'll really give you something to cry about!"

**Output JSON**:
[
    {{'text': 'Or', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'I', 'tag': 'Z8', 'desc': 'Pronouns', 'is_mwe': False, 'mwe_type': None}},
	{{'text': "'ll", 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'really', 'tag': 'A13.3', 'desc': 'Degree: Boosters', 'is_mwe': False, 'mwe_type': None}},
    {{"text": "give you something to cry about", "tag": "E3-/Q2.2", "desc": "Violent/Angry / Speech acts", "is_mwe": true, "mwe_type": "idiom"}},
	{{'text': '!', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': "'", 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
]

### Example 7: 

**Text**: "The baby, startled by this sudden violence, cried even louder."

**Output JSON**:
[
    {{'text': 'The', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'baby', 'tag': 'T3-/S2', 'desc': 'Time: New and young / People', 'is_mwe': False, 'mwe_type': None}},
	{{'text': ',', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'startled', 'tag': 'E5-', 'desc': 'Fear/shock', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'by', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'this', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'sudden', 'tag': 'T1.2', 'desc': 'Time: Momentary', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'violence', 'tag': 'E3-', 'desc': 'Violent/Angry', 'is_mwe': False, 'mwe_type': None}},
	{{'text': ',', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'cried', 'tag': 'E4.1-', 'desc': 'Sad', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'even', 'tag': 'A13.3', 'desc': 'Degree: Boosters', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'louder', 'tag': 'X3.2++', 'desc': 'Sound: Loud (comparative)', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '.', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
]

### Example 8: 

**Text**: "Under the eaves of a large house, some hundred yards from the road, a middle-aged scholar was standing with a ten- or eleven-year-old boy at his side."

**Output JSON**:
[
    {{'text': 'Under', 'tag': 'M6', 'desc': 'Location and direction', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'the', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'eaves', 'tag': 'H2', 'desc': 'Parts of buildings', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'of', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'a', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'large', 'tag': 'N3.2+', 'desc': 'Measurement: Size: Big', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'house', 'tag': 'H1', 'desc': 'Architecture, houses and buildings', 'is_mwe': False, 'mwe_type': None}},
	{{'text': ',', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'some', 'tag': 'A13.4', 'desc': 'Degree: Approximators', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'hundred', 'tag': 'N1', 'desc': 'Numbers', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'yards', 'tag': 'N3.3', 'desc': 'Measurement: Distance', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'from', 'tag': 'M6', 'desc': 'Location and direction', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'the', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'road', 'tag': 'M3', 'desc': 'Vehicles and transport on land', 'is_mwe': False, 'mwe_type': None}},
	{{'text': ',', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'a', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'middle-aged', 'tag': 'T3+', 'desc': 'Time: Old; grown-up', 'is_mwe': True, 'mwe_type': 'noun_phrase'}},
	{{'text': 'scholar', 'tag': 'P1/S5', 'desc': 'Education in general / Groups and affiliation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'was', 'tag': 'A3+', 'desc': 'Existing', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'standing', 'tag': 'M8', 'desc': 'Stationary', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'with', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'a', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'ten- or eleven-year-old', 'tag': 'T3-/N1', 'desc': 'Time: New and young / Numbers', 'is_mwe': True, 'mwe_type': 'noun_phrase'}},
	{{'text': 'boy', 'tag': 'S2.2', 'desc': 'People: Male', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'at', 'tag': 'M6', 'desc': 'Location and direction', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'his', 'tag': 'Z8', 'desc': 'Pronouns', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'side', 'tag': 'M6', 'desc': 'Location and direction', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '.', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
]

### Example 9: 

**Text**: "He was evidently affected by this little scene, for a groan escaped his lips and he appeared to be very close to tears. 'Poor creatures!' he murmured to himself."

**Output JSON**:
[
    {{'text': 'He', 'tag': 'Z8', 'desc': 'Pronouns', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'was', 'tag': 'A3+', 'desc': 'Existing', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'evidently', 'tag': 'A5.2+', 'desc': 'Evaluation: True', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'affected', 'tag': 'E4.1-', 'desc': 'Discontent', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'by', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'this', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'little', 'tag': 'A13.6', 'desc': 'Degree: Diminishers', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'scene', 'tag': 'X4.1', 'desc': 'Mental object: Conceptual object', 'is_mwe': False, 'mwe_type': None}},
	{{'text': ',', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'for', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'a', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'groan', 'tag': 'E4.1-/Q2.2', 'desc': 'Sad / Speech acts', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'escaped', 'tag': 'M1', 'desc': 'Moving, coming and going', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'his', 'tag': 'Z8', 'desc': 'Pronouns', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'lips', 'tag': 'B1', 'desc': 'Anatomy and physiology', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'and', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'he', 'tag': 'Z8', 'desc': 'Pronouns', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'appeared', 'tag': 'A8', 'desc': 'Seem', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'to', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'be', 'tag': 'A3+', 'desc': 'Existing', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'very', 'tag': 'A13.3', 'desc': 'Degree: Boosters', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'close', 'tag': 'N3.3-', 'desc': 'Distance: Near', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'to', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'tears', 'tag': 'E4.1-', 'desc': 'Sad', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '.', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': "'", 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'Poor', 'tag': 'A5.1-', 'desc': 'Evaluation: Bad', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'creatures', 'tag': 'S2/L1', 'desc': 'People / Life and living things', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '!', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': "'", 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'he', 'tag': 'Z8', 'desc': 'Pronouns', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'murmured', 'tag': 'Q2.2/X3.2-', 'desc': 'Speech acts / Sound: Quiet', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'to', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'himself', 'tag': 'Z8', 'desc': 'Pronouns', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '.', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
]

### Example 10: 

**Text**: "'Papa,' said the little boy, 'what have they done wrong?'"

**Output JSON**:
[
    {{'text': "'", 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'Papa', 'tag': 'S4', 'desc': 'Kin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': ',', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'said', 'tag': 'Q2.2', 'desc': 'Speech acts', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'the', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'little boy', 'tag': 'S2.2/T3-', 'desc': 'People: Male / Time: New and young', 'is_mwe': True, 'mwe_type': 'noun_phrase'}},
	{{'text': ',', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': "'", 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'what', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'have', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'they', 'tag': 'Z8', 'desc': 'Pronouns', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'done', 'tag': 'A1.1.1', 'desc': 'General actions / making', 'is_mwe': False, 'mwe_type': None}},
	{{'text': 'wrong', 'tag': 'A5.1-', 'desc': 'Evaluation: Bad', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '?', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': "'", 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
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

### 3.1 Chinese Multi-Word Expressions (MWE) Segmentation

- **DEFAULT**: Tag individual tokens
- **EXCEPTION**: Merge tokens into MWEs when they form a semantic unit that cannot be adequately captured by tagging each token separately

**Chinese MWE Types (8 types)**:

#### (1) idiom — 成语 / 四字格
Fixed expressions where the overall meaning cannot be derived from individual characters.
Includes classical four-character idioms (成语) and four-character set phrases (四字格).

Examples:
| MWE | Tag | Description |
|-----|-----|-------------|
| 冲风冒寒 | W4 | Weather (顶风冒寒的四字格) |
| 啼哭不休 | E4.1- | Sad (持续哭泣的四字格) |
| 温言相呵 | S1.2.1+/Q2.2 | Friendly / Speech acts (温柔言语安慰) |
| 义无反顾 | X7+/S1.2.5+ | Determined / Tough (成语) |
| 不管三七二十一 | X7+ | Determined (惯用语) |

#### (2) compound_noun — 复合名词
Two or more characters forming a lexicalized noun where the meaning is a fused unit.
These are **words** rather than phrases — they have high lexical cohesion.

Subtypes:
- Modifier-head (偏正): 囚车, 女婴, 清兵, 屋檐, 海滨
- Coordinate (并列): 刀枪, 山水
- Verb-object frozen as noun (动宾凝固): 知己

Examples:
| MWE | Tag | Description |
|-----|-----|-------------|
| 囚车 | G2.1-/M3 | Crime / Land transport |
| 清兵 | G3/S2 | Military / People |
| 女婴 | S2.1/T3- | Female / Young |
| 刀枪 | G3 | Weapons |
| 屋檐 | H2 | Parts of buildings |
| 海滨 | W3 | Geographical terms |

#### (3) noun_phrase — 名词短语
Descriptive multi-word combinations at the phrase level (lower lexical cohesion than compound nouns).
Typically adjective + noun or other modifier + head structures.

Examples:
| MWE | Tag | Description |
|-----|-----|-------------|
| 大路 | M3 | Land transport (形容词+名词) |
| 大屋 | H1 | Architecture / buildings |
| 车上 | M3 | Land transport (名词+方位词) |
| 中年人 | S2/T3+ | People / Grown-up |

#### (4) proper_name — 专有名称
Names of people, places, organizations, and other proper nouns.

Examples:
| MWE | Tag | Description |
|-----|-----|-------------|
| 江南 | Z2 | Geographical names |
| 长江 | W3/Z2 | Geographical terms / Geographical names |
| 北京外国语大学 | P1/Z2 | Education / Geographical names |

#### (5) verb_complement — 动补结构
Verb + resultative/directional complement. This is a distinctive Chinese structure
where the complement indicates the result, degree, or direction of the action.
The overall meaning often differs from the sum of verb + complement.

Examples:
| MWE | Tag | Description |
|-----|-----|-------------|
| 踢死 | E3-/L1 | Violent / Life (动词+结果补语: 踢→致死) |
| 打碎 | A1.1.2 | Damaging (动词+结果补语: 打→碎) |
| 吓哭 | E5-/E4.1- | Fear / Sad (动词+结果补语: 吓→哭) |
| 看清 | X3.4/A5.3+ | Sight / Accurate (动词+结果补语: 看→清楚) |

#### (6) verb_phrase — 动词短语
Verb + aspect marker (着/了/过) or other verb combinations that form a semantic unit.
Use this type when the aspect marker is integral to the MWE's meaning in context.

Note: Only merge verb + aspect marker into MWE when the combination forms a distinct semantic unit.
Simple "verb + 了/着/过" where the aspect marker is purely grammatical should be tagged separately
(verb tagged by meaning, aspect marker tagged as Z5).

Examples:
| MWE | Tag | Description |
|-----|-----|-------------|
| 见到 | X3.4+ | Sight / Seen (动词+补语标记) |
| 喝道 | Q2.2/X3.2+ | Speech acts / Loud (呵斥着说) |
| 说道 | Q2.2 | Speech acts (言说类动词短语) |

#### (7) separable_word — 离合词
Verb-object compound words that can be seperated by other elements (e.g., aspect markers, modifiers, or quantifiers inserted between the two parts).

DO NOT split, tag as a single MWE.

Examples:
| Form | Tag | Description |
|------|-----|-------------|
| 犯罪 (unsplit) | G2.1- | Crime |
| 犯了…罪 (unsplit: 犯了什么罪) | G2.1- | Crime |
| 睡觉 (unsplit) | B1 | Body (sleep) |
| 睡了一觉 (unsplit) | B1 | Body (sleep) |

#### (8) quantifier_phrase — 数量短语
Numeral + classifier (measure word) combinations.

Examples:
| MWE | Tag | Description |
|-----|-----|-------------|
| 一条 | N1 | Numbers |
| 一队 | N1/S5 | Numbers / Groups |
| 七辆 | N1 | Numbers |
| 三个 | N1 | Numbers |
| 数十 | N5+/A13.4 | Quantities / Approximators |
| 十一二岁 | T3-/N1 | Young / Numbers |

#### (9) other_phrase — 其他固定短语
Adverbial, prepositional, or other set phrases that function as a single semantic unit but do not fit the above 8 categories. Includes directional phrases, adverbial collocations, and other fixed multi-word combinations.

Examples:
| MWE | Tag | Description |
|-----|-----|-------------|
| 向北 | M6 | Location and direction |
| 不禁 | A1.7 | No constraint |
| 更加 | A13.3 | Degree: Boosters |

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

**Common patterns requiring slash tags in Chinese:**

| Pattern | Example | Tag | Reason |
|---------|---------|-----|--------|
| Person + Role | 清兵 (Qing soldier) | G3/S2 | Military + People |
| Person + Gender | 男子 (man) | S2.2 | Male (single tag sufficient) |
| Person + Age | 老者 (elderly person) | S2/T3+ | People + Old |
| Person + Gender + Age | 少妇 (young woman) | S2.1/T3- | Female + Young |
| Object + Domain | 囚车 (prison cart) | G2.1-/M3 | Crime + Land transport |
| Place + Name | 长江 (Yangtze River) | W3/Z2 | Geography + Name |
| Action + Emotion | 踢死 (kick to death) | E3-/L1 | Violence + Life |

### 3.4 Context-Based Disambiguation

**CRITICAL**: Use full sentence context to choose the correct tag:

"打" - Multiple meanings
"打人" → E3- (Violent/Angry)
"打水" → A1.1.1 (General actions/making)
"打电话" → Q1.3 (Telecommunications)

"一" - Multiple meanings:
"一个人" → N1 (Number: one)
"一惊" → T1.2 (Time: Momentary — sudden shock)

"再" - Multiple meanings:
"再来一次" → N6+ (Frequency — again/once more)
"再哭！(威胁)" → Z7 (If — conditional threat: "if you cry again...")

"小" / "大" in different contexts:
"小孩" → T3-/S2 (Young + People — age meaning)
"小路" → N3.2- (Size: Small — physical size)
"大哭" → A13.3/E4.1- (Booster + Sad — intensifier)
"大屋" → N3.2+/H1 (Size: Big + Building — physical size)

### 3.5 Cross-Sentence Consistency

**CRITICAL**: The same word referring to the same entity should receive consistent tags throughout the text.

- 女婴 should always be tagged S2.1/T3- (not sometimes S2, sometimes S2.1)
- 囚车 should always be tagged G2.1-/M3 (not sometimes G2.1- alone)
- 清兵 should always be tagged G3/S2 (not sometimes G3 alone)
- Speech verbs (说道, 喝道, 问道) should consistently use Q2.2

### 3.6 Punctuation
The tag for punctuation is PUNCT.

## 4. OUTPUT FORMAT

Return a JSON list. Each object must contain:

{{
  "text": "word or MWE",
  "tag": "A5.1+",               // Complete USAS tag with all components
  "desc": "Evaluation: Good",   // Description from tagset
  "is_mwe": false,              // true if multi-word unit
  "mwe_type": null              // One of: "idiom", "compound_noun", "noun_phrase",
                                //         "proper_name", "verb_complement",
                                //         "verb_phrase", "separable_word",
                                //         "quantifier_phrase", "other_phrase"
}}

## 5. VALIDATION CHECKLIST

Before submitting your output, verify:

- [ ] Did I tag ALL tokens from the text?
- [ ] Did I use the correct tag structure (LETTER.NUMBER.NUMBER+/-/TAG2)?
- [ ] Did I apply the correct number of +/- for comparatives and superlatives?
- [ ] Did I use slash notation for words with multiple semantic memberships?
- [ ] Did I correctly identify and classify MWEs using the 8 Chinese MWE types?
- [ ] Did I only merge tokens into MWEs when they truly form a semantic unit?
- [ ] Did I use sentence context to disambiguate polysemous words?
- [ ] Did I maintain consistent tags for the same word/entity across the text?
- [ ] Did I use the most specific sub-tag available (e.g., N3.3 not just N3)?
- [ ] For person nouns, did I include relevant slash tags (gender S2.1/S2.2, age T3+/T3-, role P1/G3, group S5)?

## 6. EXAMPLES

{example}

---

**YOUR TASK**:

Annotate the following text. Tag each token with ALL the rules above.

**Text**: {text}

**Output JSON**:
"""

ZH_USAS_TAGSET = EN_USAS_TAGSET

ZH_USAS_EXAMPLE = """### Example 1:

Text**: "江南近海滨的一条大路上，一队清兵手执刀枪，押着七辆囚车，冲风冒寒，向北而行。"

**Output JSON**:
[
    {{'text': '江南', 'tag': 'Z2', 'desc': 'Geographical names', 'is_mwe': True, 'mwe_type': 'proper_name'}},
	{{'text': '近', 'tag': 'N3.3-', 'desc': 'Distance: Near', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '海滨', 'tag': 'W3', 'desc': 'Geographical terms', 'is_mwe': True, 'mwe_type': 'compound_noun'}},
	{{'text': '的', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '一条', 'tag': 'N1', 'desc': 'Numbers', 'is_mwe': True, 'mwe_type': 'quantifier_phrase'}},
	{{'text': '大路', 'tag': 'M3', 'desc': 'Vehicles and transport on land', 'is_mwe': True, 'mwe_type': 'noun_phrase'}},
	{{'text': '上', 'tag': 'M6', 'desc': 'Location and direction', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '，', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '一队', 'tag': 'N1/S5', 'desc': 'Numbers / Groups and affiliation', 'is_mwe': True, 'mwe_type': 'quantifier_phrase'}},
	{{'text': '清兵', 'tag': 'G3/S2', 'desc': 'Warfare, defence and the army; weapons / People', 'is_mwe': True, 'mwe_type': 'compound_noun'}},
	{{'text': '手执', 'tag': 'A9+/B1', 'desc': 'Getting and possession / Anatomy and physiology', 'is_mwe': True, 'mwe_type': 'verb_phrase'}},
	{{'text': '刀枪', 'tag': 'G3', 'desc': 'Warfare, defence and the army; weapons', 'is_mwe': True, 'mwe_type': 'compound_noun'}},
	{{'text': '，', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '押着', 'tag': 'G2.1-/M1', 'desc': 'Crime / Moving, coming and going', 'is_mwe': True, 'mwe_type': 'verb_phrase'}},
	{{'text': '七辆', 'tag': 'N1', 'desc': 'Numbers', 'is_mwe': True, 'mwe_type': 'quantifier_phrase'}},
	{{'text': '囚车', 'tag': 'G2.1-/M3', 'desc': 'Crime / Vehicles and transport on land', 'is_mwe': True, 'mwe_type': 'compound_noun'}},
	{{'text': '，', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '冲风冒寒', 'tag': 'W4/A12-/O4.6-', 'desc': 'Weather / Difficult / Temperature: Cold', 'is_mwe': True, 'mwe_type': 'idiom'}},
	{{'text': '，', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '向北', 'tag': 'M6', 'desc': 'Location and direction', 'is_mwe': True, 'mwe_type': 'other_phrase'}},
	{{'text': '而', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '行', 'tag': 'M1', 'desc': 'Moving, coming and going', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '。', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
]

### Example 2:

Text**: "前面三辆囚车中分别监禁的是三个男子，都作书生打扮，一个是白发老者，两个是中年人。"

**Output JSON**:
[
    {{'text': '前面', 'tag': 'M6', 'desc': 'Location and direction', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '三辆', 'tag': 'N1', 'desc': 'Numbers', 'is_mwe': True, 'mwe_type': 'quantifier_phrase'}},
	{{'text': '囚车', 'tag': 'G2.1-/M3', 'desc': 'Crime / Vehicles and transport on land', 'is_mwe': True, 'mwe_type': 'compound_noun'}},
	{{'text': '中', 'tag': 'M6', 'desc': 'Location and direction', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '分别', 'tag': 'A6.1-', 'desc': 'Comparing: Different', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '监禁', 'tag': 'G2.1-', 'desc': 'Crime', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '的', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '是', 'tag': 'A3+', 'desc': 'Existing', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '三个', 'tag': 'N1', 'desc': 'Numbers', 'is_mwe': True, 'mwe_type': 'quantifier_phrase'}},
	{{'text': '男子', 'tag': 'S2.2', 'desc': 'People: Male', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '，', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '都', 'tag': 'N5.1+', 'desc': 'Entire; maximum', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '作', 'tag': 'A8', 'desc': 'Seem', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '书生', 'tag': 'P1/S5', 'desc': 'Education in general / Groups and affiliation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '打扮', 'tag': 'B5', 'desc': 'Clothes and personal belongings', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '，', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '一个', 'tag': 'N1', 'desc': 'Numbers', 'is_mwe': True, 'mwe_type': 'quantifier_phrase'}},
	{{'text': '是', 'tag': 'A3+', 'desc': 'Existing', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '白发', 'tag': 'B1/T3+', 'desc': 'Anatomy and physiology / Time: Old; grown-up', 'is_mwe': True, 'mwe_type': 'compound_noun'}},
	{{'text': '老者', 'tag': 'S2/T3+', 'desc': 'People / Time: Old; grown-up', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '，', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '两个', 'tag': 'N1', 'desc': 'Numbers', 'is_mwe': True, 'mwe_type': 'quantifier_phrase'}},
	{{'text': '是', 'tag': 'A3+', 'desc': 'Existing', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '中年人', 'tag': 'S2/T3+', 'desc': 'People / Time: Old; grown-up', 'is_mwe': True, 'mwe_type': 'noun_phrase'}},
	{{'text': '。', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
]

### Example 3:

Text**: "后面四辆囚车中坐的是女子，最后一辆囚车中是个少妇，怀中抱着个女婴。"

**Output JSON**:
[
    {{'text': '后面', 'tag': 'M6', 'desc': 'Location and direction', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '四辆', 'tag': 'N1', 'desc': 'Numbers', 'is_mwe': True, 'mwe_type': 'quantifier_phrase'}},
	{{'text': '囚车', 'tag': 'G2.1-/M3', 'desc': 'Crime / Vehicles and transport on land', 'is_mwe': True, 'mwe_type': 'compound_noun'}},
	{{'text': '中', 'tag': 'M6', 'desc': 'Location and direction', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '座', 'tag': 'M8', 'desc': 'Stationary', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '的', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '是', 'tag': 'A3+', 'desc': 'Existing', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '女子', 'tag': 'S2.1', 'desc': 'People: Female', 'is_mwe': True, 'mwe_type': 'compound_noun'}},
	{{'text': '，', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '最后', 'tag': 'N4', 'desc': 'Linear order', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '一辆', 'tag': 'N1', 'desc': 'Numbers', 'is_mwe': True, 'mwe_type': 'quantifier_phrase'}},
	{{'text': '囚车', 'tag': 'G2.1-/M3', 'desc': 'Crime / Vehicles and transport on land', 'is_mwe': True, 'mwe_type': 'compound_noun'}},
	{{'text': '中', 'tag': 'M6', 'desc': 'Location and direction', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '是', 'tag': 'A3+', 'desc': 'Existing', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '个', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '少妇', 'tag': 'S2.1/T3-/S4', 'desc': 'People: Female / Time: New and young / Kin', 'is_mwe': True, 'mwe_type': 'compound_noun'}},
	{{'text': '，', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '怀中', 'tag': 'B1', 'desc': 'Anatomy and physiology', 'is_mwe': True, 'mwe_type': 'compound_noun'}},
	{{'text': '抱着', 'tag': 'A9+', 'desc': 'Getting and possession', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '个', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '女婴', 'tag': 'S2.1/T3-', 'desc': 'People: Female / Time: New and young', 'is_mwe': True, 'mwe_type': 'compound_noun'}},
	{{'text': '。', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
]

### Example 4:

Text**: "女婴啼哭不休。 她母亲温言相呵，女婴只是大哭。"

**Output JSON**:
[
    {{'text': '女婴', 'tag': 'S2.1/T3-', 'desc': 'People: Female / Time: New and young', 'is_mwe': True, 'mwe_type': 'compound_noun'}},
	{{'text': '啼哭不休', 'tag': 'E4.1-/T1.3+', 'desc': 'Sad / Time period: long', 'is_mwe': True, 'mwe_type': 'idiom'}},
	{{'text': '。', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '她', 'tag': 'Z8', 'desc': 'Pronouns', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '母亲', 'tag': 'S4/S2.1', 'desc': 'Kin / People: Female', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '温言相呵', 'tag': 'E4.2+/Q2.2', 'desc': 'Contentment / Speech acts', 'is_mwe': True, 'mwe_type': 'idiom'}},
	{{'text': '，', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '女婴', 'tag': 'S2.1/T3-', 'desc': 'People: Female / Time: New and young', 'is_mwe': True, 'mwe_type': 'compound_noun'}},
	{{'text': '只是', 'tag': 'A14', 'desc': 'Exclusivizers/particularizers', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '大哭', 'tag': 'E4.1-/X3.2+', 'desc': 'Sad / Sound: Loud', 'is_mwe': True, 'mwe_type': 'verb_phrase'}},
	{{'text': '。', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
]

### Example 5:

Text**: "囚车旁一清兵恼了，伸腿在车上踢了一脚，喝道：“再哭，再哭！"

**Output JSON**:
[
    {{'text': '囚车', 'tag': 'G2.1-/M3', 'desc': 'Crime / Vehicles and transport on land', 'is_mwe': True, 'mwe_type': 'compound_noun'}},
	{{'text': '旁', 'tag': 'M6', 'desc': 'Location and direction', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '一', 'tag': 'N1', 'desc': 'Numbers', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '清兵', 'tag': 'G3/S2', 'desc': 'Warfare, defence and the army; weapons / People', 'is_mwe': True, 'mwe_type': 'compound_noun'}},
	{{'text': '恼', 'tag': 'E3-', 'desc': 'Violent/Angry', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '了', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '，', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '伸腿', 'tag': 'M1/B1', 'desc': 'Moving, coming and going / Anatomy and physiology', 'is_mwe': True, 'mwe_type': 'verb_phrase'}},
	{{'text': '在', 'tag': 'M6', 'desc': 'Location and direction', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '车上', 'tag': 'M3', 'desc': 'Vehicles and transport on land', 'is_mwe': True, 'mwe_type': 'noun_phrase'}},
	{{'text': '踢', 'tag': 'E3-', 'desc': 'Violent/Angry', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '了', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '一脚', 'tag': 'N1/B1', 'desc': 'Numbers / Anatomy and physiology', 'is_mwe': True, 'mwe_type': 'quantifier_phrase'}},
	{{'text': '，', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '喝道', 'tag': 'Q2.2/X3.2+', 'desc': 'Speech acts / Sound: Loud', 'is_mwe': True, 'mwe_type': 'verb_phrase'}},
	{{'text': '：', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '“', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '再', 'tag': 'Z7', 'desc': 'If', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '哭', 'tag': 'E4.1-', 'desc': 'Sad', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '，', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '再', 'tag': 'Z7', 'desc': 'If', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '哭', 'tag': 'E4.1-', 'desc': 'Sad', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '！', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '”', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
]

### Example 6:

Text**: "老子踢死你！”"

**Output JSON**:
[
    {{'text': '老子', 'tag': 'Z8/S1.2.3', 'desc': 'Pronouns / Egoism', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '踢死', 'tag': 'E3-/L1', 'desc': 'Violent/Angry / Life and living things', 'is_mwe': True, 'mwe_type': 'verb_complement'}},
	{{'text': '你', 'tag': 'Z8', 'desc': 'Pronouns', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '！', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '”', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
]

### Example 7:

Text**: "那女婴一惊，哭得更加响了。"

**Output JSON**:
[
    {{'text': '那', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '女婴', 'tag': 'S2.1/T3-', 'desc': 'People: Female / Time: New and young', 'is_mwe': True, 'mwe_type': 'compound_noun'}},
	{{'text': '一', 'tag': 'T1.2', 'desc': 'Time: Momentary', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '惊', 'tag': 'E5-', 'desc': 'Fear/shock', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '，', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '哭', 'tag': 'E4.1-', 'desc': 'Sad', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '得', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '更加', 'tag': 'A13.3', 'desc': 'Degree: Boosters', 'is_mwe': True, 'mwe_type': 'other_phrase'}},
	{{'text': '响', 'tag': 'X3.2+', 'desc': 'Sound: Loud', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '了', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '。', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
]

### Example 8:

Text**: "离开道路数十丈处有座大屋，屋檐下站着一个中年文士，一个十一二岁的小孩。"

**Output JSON**:
[
    {{'text': '离开', 'tag': 'N3.3', 'desc': 'Measurement: Distance', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '道路', 'tag': 'M3', 'desc': 'Vehicles and transport on land', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '数十', 'tag': 'N5+/A13.4', 'desc': 'Quantities: many/much / Degree: Approximators', 'is_mwe': True, 'mwe_type': 'quantifier_phrase'}},
	{{'text': '丈', 'tag': 'N3.3', 'desc': 'Measurement: Distance', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '处', 'tag': 'M7', 'desc': 'Places', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '有', 'tag': 'A3+', 'desc': 'Existing', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '座', 'tag': 'N5', 'desc': 'Quantities', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '大屋', 'tag': 'H1', 'desc': 'Architecture, houses and buildings', 'is_mwe': True, 'mwe_type': 'noun_phrase'}},
	{{'text': '，', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '屋檐', 'tag': 'H2', 'desc': 'Parts of buildings', 'is_mwe': True, 'mwe_type': 'compound_noun'}},
	{{'text': '下', 'tag': 'M6', 'desc': 'Location and direction', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '站着', 'tag': 'M8', 'desc': 'Stationary', 'is_mwe': True, 'mwe_type': 'verb_phrase'}},
	{{'text': '一个', 'tag': 'N1', 'desc': 'Numbers', 'is_mwe': True, 'mwe_type': 'quantifier_phrase'}},
	{{'text': '中年', 'tag': 'T3+', 'desc': 'Time: Old; grown-up', 'is_mwe': True, 'mwe_type': 'noun_phrase'}},
	{{'text': '文士', 'tag': 'P1/S2', 'desc': 'Education in general / People', 'is_mwe': True, 'mwe_type': 'compound_noun'}},
	{{'text': '，', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '一个', 'tag': 'N1', 'desc': 'Numbers', 'is_mwe': True, 'mwe_type': 'quantifier_phrase'}},
	{{'text': '十一二岁', 'tag': 'T3-/N1', 'desc': 'Time: New and young / Numbers ', 'is_mwe': True, 'mwe_type': 'quantifier_phrase'}},
	{{'text': '的', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '小孩', 'tag': 'S2/T3-', 'desc': 'People / Time: New and young', 'is_mwe': True, 'mwe_type': 'compound_noun'}},
	{{'text': '。', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
]

### Example 9:

Text**: "那文士见到这等情景，不禁长叹一声，眼眶也红了，说道：“可怜，可怜！”"

**Output JSON**:
[
    {{'text': '那', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '文士', 'tag': 'P1/S2', 'desc': 'Education in general / People', 'is_mwe': True, 'mwe_type': 'compound_noun'}},
	{{'text': '见到', 'tag': 'X3.4+', 'desc': 'Sensory: Sight / Seen', 'is_mwe': True, 'mwe_type': 'verb_phrase'}},
	{{'text': '这', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '等', 'tag': 'A4.1', 'desc': 'Generally kinds, groups, examples', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '情景', 'tag': 'X4.1', 'desc': 'Mental object: Conceptual object', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '，', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '不禁', 'tag': 'A1.7-', 'desc': 'No constraint', 'is_mwe': True, 'mwe_type': 'other_phrase'}},
	{{'text': '长叹', 'tag': 'E4.1-/Q2.2', 'desc': 'Sad / Speech acts', 'is_mwe': True, 'mwe_type': 'verb_phrase'}},
	{{'text': '一声', 'tag': 'N1/X3.2', 'desc': 'Numbers / Sensory: Sound', 'is_mwe': True, 'mwe_type': 'quantifier_phrase'}},
	{{'text': '，', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '眼眶', 'tag': 'B1', 'desc': 'Anatomy and physiology', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '也', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '红', 'tag': 'E4.1-/O4.3', 'desc': 'Sad / Colour and colour patterns', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '了', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '，', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '说道', 'tag': 'Q2.2', 'desc': 'Speech acts', 'is_mwe': True, 'mwe_type': 'verb_phrase'}},
	{{'text': '：', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '“', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '可怜', 'tag': 'E4.1-/E2-', 'desc': 'Sad / Dislike', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '，', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '可怜', 'tag': 'E4.1-/E2-', 'desc': 'Sad / Dislike', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '！', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '”', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
]

### Example 10:

Text**: "那小孩问道：“爹爹，他们犯了什么罪？"

**Output JSON**:
[
    {{'text': '那', 'tag': 'Z5', 'desc': 'Grammatical bin', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '小孩', 'tag': 'S2/T3-', 'desc': 'People / Time: New and young', 'is_mwe': True, 'mwe_type': 'compound_noun'}},
	{{'text': '问道', 'tag': 'Q2.2', 'desc': 'Speech acts', 'is_mwe': True, 'mwe_type': 'verb_phrase'}},
	{{'text': '：', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '“', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '爹爹', 'tag': 'S4', 'desc': 'Kin', 'is_mwe': True, 'mwe_type': 'compound_noun'}},
	{{'text': '，', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '他们', 'tag': 'Z8', 'desc': 'Pronouns', 'is_mwe': False, 'mwe_type': None}},
	{{'text': '犯了什么罪', 'tag': 'G2.1-', 'desc': 'Crime', 'is_mwe': True, 'mwe_type': 'separable_word'}},
	{{'text': '”', 'tag': 'PUNCT', 'desc': 'Punctuation', 'is_mwe': False, 'mwe_type': None}},
]
"""

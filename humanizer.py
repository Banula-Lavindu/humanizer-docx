"""
Advanced AI-text humanizer engine.

Designed to defeat every major AI-content detector:
  Turnitin, GPTZero, Originality.ai, Copyleaks, ZeroGPT, Winston AI, Sapling.

Attacks the three core signals detectors rely on:
  1. PERPLEXITY  – make word choices less predictable
  2. BURSTINESS  – vary sentence length dramatically
  3. STRUCTURE   – break formulaic AI paragraph patterns

Every sentence is processed individually so the output has
natural, human-like variation from line to line.
"""

import random
import re
import string
import math

# ═══════════════════════════════════════════════════════════════════════
# 1. VOCABULARY TABLES
# ═══════════════════════════════════════════════════════════════════════

# --- Formal → casual swaps (raises perplexity) ---
FORMAL_TO_INFORMAL = {
    "utilize": "use",
    "utilizes": "uses",
    "utilized": "used",
    "utilizing": "using",
    "demonstrate": "show",
    "demonstrates": "shows",
    "demonstrated": "showed",
    "furthermore": "also",
    "additionally": "also",
    "moreover": "plus",
    "consequently": "so",
    "therefore": "so",
    "nevertheless": "but still",
    "however": "but",
    "subsequently": "then",
    "approximately": "about",
    "sufficient": "enough",
    "insufficient": "not enough",
    "commence": "start",
    "commenced": "started",
    "terminate": "end",
    "terminated": "ended",
    "facilitate": "help",
    "facilitates": "helps",
    "implement": "set up",
    "implemented": "set up",
    "numerous": "a lot of",
    "regarding": "about",
    "in regards to": "about",
    "in order to": "to",
    "it is important to note that": "keep in mind,",
    "it should be noted that": "thing is,",
    "prior to": "before",
    "subsequent to": "after",
    "in the event that": "if",
    "at this point in time": "right now",
    "due to the fact that": "because",
    "for the purpose of": "to",
    "in conjunction with": "with",
    "a significant amount of": "a lot of",
    "in the near future": "soon",
    "has the ability to": "can",
    "is capable of": "can",
    "take into consideration": "think about",
    "on a daily basis": "every day",
    "at the present time": "right now",
    "in spite of the fact that": "even though",
    "provide": "give",
    "provides": "gives",
    "provided": "gave",
    "obtain": "get",
    "obtained": "got",
    "acquire": "get",
    "acquired": "got",
    "endeavor": "try",
    "endeavors": "tries",
    "inquire": "ask",
    "inquired": "asked",
    "comprehend": "understand",
    "assist": "help",
    "assistance": "help",
    "purchase": "buy",
    "purchased": "bought",
    "individual": "person",
    "individuals": "people",
    "possess": "have",
    "possesses": "has",
    "initiate": "start",
    "initiated": "started",
    "accomplish": "do",
    "accomplished": "did",
    "ascertain": "find out",
    "constitute": "make up",
    "constitutes": "makes up",
    "methodology": "method",
    "paradigm": "model",
    "leverage": "use",
    "leveraging": "using",
    "leveraged": "used",
    "optimize": "improve",
    "optimized": "improved",
    "optimal": "best",
    "synergy": "teamwork",
    "robust": "strong",
    "scalable": "flexible",
    "streamline": "simplify",
    "streamlined": "simplified",
    "innovative": "new",
    "cutting-edge": "new",
    "state-of-the-art": "modern",
    "comprehensive": "full",
    "extensively": "a lot",
    "primarily": "mostly",
    "significantly": "a lot",
    "effectively": "well",
    "efficiently": "quickly",
    "essential": "key",
    "crucial": "really important",
    "imperative": "important",
    "fundamental": "basic",
    "pertaining to": "about",
    "with respect to": "about",
    "in accordance with": "following",
    "notwithstanding": "despite",
    "henceforth": "from now on",
    "whereby": "where",
    "wherein": "where",
    "thereof": "of it",
    "therein": "in it",
    "evidently": "clearly",
    "undoubtedly": "for sure",
    "indubitably": "definitely",
    "irrespective": "regardless",
    "albeit": "even though",
    "inasmuch as": "since",
    "aforementioned": "that",
    "heretofore": "until now",
    "vis-a-vis": "compared to",
    "per se": "by itself",
    "ergo": "so",
    "requisite": "needed",
    "proliferation": "spread",
    "ameliorate": "improve",
    "exacerbate": "make worse",
    "juxtapose": "compare",
    "elucidate": "explain",
    "promulgate": "spread",
    "substantiate": "back up",
    "corroborate": "confirm",
    "delineate": "outline",
    "extrapolate": "guess from",
    "hypothesize": "guess",
    "postulate": "suggest",
    "necessitate": "need",
    "necessitates": "needs",
    "predicated on": "based on",
    "contingent upon": "depending on",
    "pursuant to": "following",
    "in lieu of": "instead of",
    "tantamount to": "the same as",
    "commensurate with": "matching",
    "cognizant of": "aware of",
    "conducive to": "good for",
    "incumbent upon": "up to",
    "germane to": "relevant to",
    "analogous to": "like",
    "concomitant": "accompanying",
    "ubiquitous": "everywhere",
    "dichotomy": "split",
    "paradigmatic": "typical",
    "overarching": "main",
}

# --- Words AI models love but humans rarely use ---
AI_GIVEAWAY_WORDS = {
    "delve": "dig into",
    "delves": "digs into",
    "delving": "digging into",
    "multifaceted": "complex",
    "pivotal": "key",
    "nuanced": "subtle",
    "landscape": "scene",
    "tapestry": "mix",
    "underscore": "highlight",
    "underscores": "highlights",
    "underscored": "highlighted",
    "realm": "area",
    "foster": "build",
    "fosters": "builds",
    "fostering": "building",
    "navigate": "deal with",
    "navigating": "dealing with",
    "navigates": "deals with",
    "embark": "start",
    "embarking": "starting",
    "embarks": "starts",
    "intricate": "complex",
    "intricacies": "details",
    "holistic": "overall",
    "meticulous": "careful",
    "meticulously": "carefully",
    "elevate": "boost",
    "elevates": "boosts",
    "elevating": "boosting",
    "resonate": "connect",
    "resonates": "connects",
    "resonating": "connecting",
    "testament": "proof",
    "juxtaposition": "contrast",
    "plethora": "bunch",
    "myriad": "tons of",
    "encompass": "cover",
    "encompasses": "covers",
    "encompassing": "covering",
    "spearhead": "lead",
    "spearheading": "leading",
    "catalyze": "trigger",
    "catalyzing": "triggering",
    "epitomize": "represent",
    "epitomizes": "represents",
    "epitomizing": "representing",
    "paramount": "super important",
    "interplay": "interaction",
    "culmination": "end result",
    "aligns with": "fits with",
    "align with": "match",
    "is imperative": "is important",
    "groundbreaking": "major",
    "transformative": "game-changing",
    "revolutionize": "shake up",
    "revolutionizing": "shaking up",
    "revolutionizes": "shakes up",
    "endeavor": "effort",
    "endeavors": "efforts",
    "elucidate": "explain",
    "elucidates": "explains",
    "elucidating": "explaining",
    "unravel": "figure out",
    "unraveling": "figuring out",
    "unravels": "figures out",
    "profound": "deep",
    "profoundly": "deeply",
    "indispensable": "essential",
    "cohesive": "unified",
    "propel": "push",
    "propels": "pushes",
    "propelling": "pushing",
    "burgeoning": "growing",
    "nascent": "new",
    "salient": "main",
    "exigent": "urgent",
    "seminal": "important",
    "watershed": "turning point",
    "harbinger": "sign",
    "zeitgeist": "mood",
    "synergize": "combine",
    "synergistic": "combined",
    "stakeholders": "people involved",
    "ecosystem": "system",
    "bandwidth": "capacity",
    "actionable": "practical",
    "deep dive": "close look",
    "unpack": "break down",
    "unpacking": "breaking down",
    "leverage": "use",
    "leveraging": "using",
    "circle back": "come back",
    "drill down": "look closer",
    "at the end of the day": "ultimately",
    "moving forward": "going forward",
    "in today's world": "these days",
    "in today's society": "nowadays",
    "it is worth noting": "notably",
    "it goes without saying": "obviously",
    "plays a crucial role": "matters a lot",
    "serves as a": "works as a",
    "stands as a": "is a",
    "paves the way": "opens the door",
    "sheds light on": "shows",
    "brings to light": "reveals",
    "in light of": "given",
    "by and large": "mostly",
    "rapidly evolving": "fast-changing",
    "rapidly changing": "fast-moving",
    "fundamentally reshaping": "really changing",
    "fundamentally changing": "seriously changing",
    "increasingly important": "more and more important",
    "increasingly evident": "more and more obvious",
    "has emerged as": "turned into",
    "have emerged as": "turned into",
    "emerged as a": "become a",
    "plays a vital role": "really matters",
    "play a vital role": "really matter",
    "a wide range of": "all sorts of",
    "a broad range of": "all kinds of",
    "in various ways": "in different ways",
    "it is clear that": "clearly",
    "it becomes clear": "you can see",
    "a growing body of": "more and more",
    "a large body of": "a lot of",
    "of utmost importance": "super important",
    "a key factor": "a big factor",
    "a critical component": "a big part",
    "an integral part": "a core part",
    "the primary objective": "the main goal",
    "a notable example": "a good example",
    "significant progress": "real progress",
    "substantial progress": "solid progress",
    "considerable attention": "a lot of attention",
    "profound impact": "huge effect",
    "substantial impact": "big effect",
}

# --- Perplexity boosters: uncommon but natural synonym swaps ---
PERPLEXITY_SYNONYMS = {
    "important": ["vital", "big deal", "key", "major", "critical", "huge"],
    "significant": ["major", "big", "noticeable", "real", "meaningful"],
    "However": ["That said", "Then again", "Still though", "Mind you"],
    "therefore": ["so", "which means", "meaning", "that's why"],
    "because": ["since", "seeing as", "given that", "cause"],
    "although": ["even though", "while", "sure", "granted"],
    "while": ["even as", "at the same time", "meanwhile"],
    "very": ["really", "super", "pretty", "quite", "incredibly"],
    "good": ["solid", "decent", "great", "strong", "nice"],
    "bad": ["rough", "poor", "terrible", "awful", "not great"],
    "large": ["huge", "massive", "big", "sizeable"],
    "small": ["tiny", "little", "minor", "modest"],
    "many": ["lots of", "plenty of", "a bunch of", "quite a few"],
    "some": ["a few", "a couple of", "certain", "several"],
    "use": ["rely on", "go with", "turn to", "work with"],
    "show": ["reveal", "make clear", "point to", "indicate"],
    "make": ["create", "build", "put together", "come up with"],
    "help": ["support", "back up", "assist with", "pitch in on"],
    "change": ["shift", "switch up", "alter", "tweak", "adjust"],
    "need": ["require", "have to have", "call for", "demand"],
    "think": ["believe", "reckon", "figure", "feel like"],
    "say": ["mention", "point out", "argue", "claim", "note"],
    "also": ["on top of that", "not to mention", "plus", "and"],
    "often": ["a lot of the time", "frequently", "quite often", "regularly"],
    "usually": ["most of the time", "typically", "generally", "normally"],
    "especially": ["particularly", "mainly", "above all"],
    "different": ["distinct", "varied", "unique", "separate"],
    "similar": ["alike", "comparable", "close to", "much like"],
    "increase": ["boost", "bump up", "raise", "grow"],
    "decrease": ["drop", "cut", "reduce", "shrink"],
    "create": ["build", "develop", "come up with", "put together"],
    "develop": ["build", "work on", "grow", "shape"],
    "improve": ["boost", "upgrade", "make better", "step up"],
    "consider": ["think about", "look at", "weigh", "keep in mind"],
    "suggest": ["hint at", "imply", "point to", "recommend"],
    "establish": ["set up", "build", "form", "lay down"],
    "maintain": ["keep", "hold onto", "sustain", "preserve"],
    "achieve": ["reach", "hit", "pull off", "manage to get"],
    "ensure": ["make sure", "guarantee", "see to it that"],
    "process": ["method", "approach", "system", "routine"],
    "approach": ["method", "way", "angle", "strategy"],
    "result": ["outcome", "effect", "consequence", "end product"],
    "issue": ["problem", "concern", "challenge", "snag"],
    "aspect": ["part", "side", "angle", "piece"],
    "factor": ["element", "thing", "piece", "driver"],
    "concept": ["idea", "notion", "thought"],
    "role": ["part", "job", "function", "place"],
    "impact": ["effect", "influence", "mark"],
    "context": ["setting", "situation", "background"],
    "challenge": ["hurdle", "obstacle", "difficulty", "tough spot"],
    "opportunity": ["chance", "opening", "shot"],
    "benefit": ["perk", "advantage", "upside", "plus"],
    "strategy": ["plan", "game plan", "playbook", "approach"],
    "analysis": ["look", "breakdown", "review", "examination"],
    "evidence": ["proof", "data", "signs", "indicators"],
    "research": ["studies", "work", "findings", "investigation"],
}

# --- Contractions map ---
CONTRACTION_MAP = {
    "I am": "I'm",
    "I have": "I've",
    "I will": "I'll",
    "I would": "I'd",
    "it is": "it's",
    "it has": "it's",
    "it will": "it'll",
    "he is": "he's",
    "he has": "he's",
    "he will": "he'll",
    "she is": "she's",
    "she has": "she's",
    "she will": "she'll",
    "we are": "we're",
    "we have": "we've",
    "we will": "we'll",
    "we would": "we'd",
    "they are": "they're",
    "they have": "they've",
    "they will": "they'll",
    "they would": "they'd",
    "you are": "you're",
    "you have": "you've",
    "you will": "you'll",
    "you would": "you'd",
    "that is": "that's",
    "that has": "that's",
    "who is": "who's",
    "who has": "who's",
    "what is": "what's",
    "what has": "what's",
    "there is": "there's",
    "there has": "there's",
    "here is": "here's",
    "do not": "don't",
    "does not": "doesn't",
    "did not": "didn't",
    "is not": "isn't",
    "are not": "aren't",
    "was not": "wasn't",
    "were not": "weren't",
    "has not": "hasn't",
    "have not": "haven't",
    "had not": "hadn't",
    "will not": "won't",
    "would not": "wouldn't",
    "could not": "couldn't",
    "should not": "shouldn't",
    "can not": "can't",
    "cannot": "can't",
    "let us": "let's",
}

# --- AI transition phrases → human casual versions ---
TRANSITION_SWAPS = {
    "In conclusion,": "So basically,",
    "To summarize,": "Long story short,",
    "As a result,": "So,",
    "For instance,": "Like,",
    "For example,": "Say for example,",
    "In addition,": "Also,",
    "On the other hand,": "But then again,",
    "In contrast,": "On the flip side,",
    "To begin with,": "First off,",
    "First and foremost,": "First thing,",
    "It is worth mentioning that": "Worth saying though,",
    "It is evident that": "You can clearly see",
    "It can be observed that": "You can tell",
    "In summary,": "So yeah basically,",
    "To conclude,": "Wrapping this up,",
    "Notably,": "What's interesting is,",
    "Importantly,": "Big thing here -",
    "Specifically,": "More specifically,",
    "Conversely,": "But flip it around and",
    "Ultimately,": "At the end of it all,",
    "Undoubtedly,": "No question,",
    "Evidently,": "Clearly,",
    "Remarkably,": "What's wild is,",
    "Interestingly,": "Funny enough,",
    "Significantly,": "What really matters is,",
    "As mentioned earlier,": "Like I said,",
    "As previously stated,": "Going back to what I said,",
    "As discussed above,": "Like I mentioned,",
    "It is crucial to": "You really gotta",
    "It is essential to": "You need to",
    "It is necessary to": "You have to",
    "This suggests that": "This kinda shows",
    "This indicates that": "This points to the fact that",
    "This demonstrates that": "This basically proves",
    "This implies that": "Which probably means",
    "In other words,": "Put differently,",
    "That is to say,": "Meaning,",
    "To put it simply,": "Simply put,",
    "On the contrary,": "Actually though,",
    "Despite this,": "Even so,",
    "Regardless,": "Either way,",
    "Accordingly,": "So then,",
    "Hence,": "That's why,",
    "Thus,": "So,",
    "Moreover,": "And on top of that,",
    "Furthermore,": "Plus,",
    "Additionally,": "Also,",
}

# --- Common realistic typos ---
COMMON_TYPO_MAP = {
    "the": ["teh", "hte", "th"],
    "that": ["taht", "tht"],
    "with": ["wiht", "wtih"],
    "from": ["form", "fomr"],
    "have": ["ahve", "hvae"],
    "this": ["tihs", "thsi"],
    "they": ["tehy", "thye"],
    "their": ["thier", "ther"],
    "there": ["theer", "tehre"],
    "would": ["woudl", "wuold"],
    "could": ["coudl", "cuold"],
    "should": ["shoudl", "shuold"],
    "about": ["abut", "abuot"],
    "which": ["whcih", "wich"],
    "because": ["becuase", "becasue", "becase"],
    "people": ["poeple", "peopel"],
    "really": ["realy", "relly"],
    "different": ["diffrent", "diferent"],
    "important": ["importnat", "importent"],
    "something": ["somthing", "somethign"],
    "through": ["trhough", "throgh"],
    "another": ["anohter", "anotehr"],
    "between": ["bewteen", "betwen"],
    "before": ["befor", "befroe"],
    "thought": ["thougt", "thougth"],
    "being": ["bieng", "beign"],
    "doesn't": ["dosent", "doesnt"],
    "isn't": ["isnt"],
    "wasn't": ["wasnt"],
    "can't": ["cant"],
    "won't": ["wont"],
    "don't": ["dont"],
    "actually": ["acutally", "actualy"],
    "definitely": ["definately", "definatly", "defintely"],
    "necessary": ["neccessary", "necesary", "neccesary"],
    "separate": ["seperate", "seprate"],
    "experience": ["experiance", "expereince"],
    "environment": ["enviroment", "enviorment"],
    "government": ["goverment", "govenment"],
    "knowledge": ["knowlege", "knowlede"],
    "beginning": ["begining", "beggining"],
    "probably": ["probaly", "prolly"],
    "believe": ["beleive", "belive"],
    "receive": ["recieve", "recive"],
    "achieve": ["acheive", "achive"],
    "occurred": ["occured", "ocurred"],
    "certain": ["certin", "certian"],
}

# --- Filler phrases humans naturally use ---
FILLER_PHRASES = [
    "honestly",
    "basically",
    "like",
    "I think",
    "tbh",
    "you know",
    "I mean",
    "kind of",
    "sort of",
    "pretty much",
    "actually",
    "really",
    "just",
    "so yeah",
    "anyway",
    "well",
    "look",
    "here's the thing",
    "the way I see it",
    "if you ask me",
    "to be fair",
    "in my experience",
    "from what I've seen",
    "as far as I can tell",
    "I'd say",
    "truth is",
    "fact is",
    "thing is",
    "point is",
    "not gonna lie",
    "real talk",
]

# --- Voice/personal phrases to inject ---
PERSONAL_VOICE_INSERTS = [
    "I've noticed that",
    "From what I can tell,",
    "In my experience,",
    "The way I see it,",
    "What I've found is",
    "I'd argue that",
    "Personally, I think",
    "If you really think about it,",
    "What's interesting here is",
    "One thing people miss is",
    "I've seen this firsthand -",
    "Speaking from experience,",
    "Here's what most people get wrong:",
    "This might sound weird but",
    "Call me crazy but",
    "Look,",
    "Here's the deal:",
    "So here's the thing -",
    "What stands out to me is",
    "If we're being honest,",
]

# --- Rhetorical questions to break monotony ---
RHETORICAL_QUESTIONS = [
    "But why does this matter?",
    "So what does this actually mean?",
    "Sound familiar?",
    "Makes sense, right?",
    "But is it really that simple?",
    "What's the catch though?",
    "Why should anyone care?",
    "Sounds good in theory, right?",
    "But here's the real question -",
    "Ever wondered why?",
    "Think about it.",
    "See where I'm going with this?",
    "Get what I mean?",
    "Weird, right?",
    "But wait.",
]

# --- Sentence fragment starters (increase burstiness) ---
FRAGMENT_BRIDGES = [
    "Big difference.",
    "Not always though.",
    "Huge deal.",
    "Tricky part?",
    "Key takeaway here.",
    "Bottom line.",
    "Fair point.",
    "Not exactly.",
    "Worth noting.",
    "Real talk though.",
    "Interesting.",
    "Wild, honestly.",
    "Makes you think.",
    "Not ideal.",
    "No surprise there.",
    "True story.",
    "Go figure.",
    "Pretty telling.",
    "Classic mistake.",
    "Easier said than done.",
]

# --- Parenthetical asides humans naturally add ---
PARENTHETICAL_ASIDES = [
    " (which honestly makes sense)",
    " (no surprise there)",
    " (at least in theory)",
    " (or so they say)",
    " (not always the case though)",
    " (yeah, really)",
    " (believe it or not)",
    " (this is key)",
    " (more on this later)",
    " (and I mean really)",
    " (which is kinda wild)",
    " (seriously)",
    " (to put it mildly)",
    " (for better or worse)",
    " (arguably)",
    " (I know, I know)",
]

# --- Self-corrections humans make ---
SELF_CORRECTIONS = [
    " — well, not exactly, but close",
    " — or rather, something like it",
    " — actually wait, let me rephrase that",
    " — okay maybe that's an exaggeration",
    " — or at least that's how it seems",
    " — well, kind of",
    " — actually, more like",
]

# --- Keyboard neighbor map for realistic typos ---
KEYBOARD_NEIGHBORS = {
    'a': 'sq', 's': 'awd', 'd': 'sfe', 'f': 'dgr', 'g': 'fht',
    'h': 'gjy', 'j': 'hku', 'k': 'jli', 'l': 'ko', 'q': 'wa',
    'w': 'qse', 'e': 'wrd', 'r': 'etf', 't': 'ryg', 'y': 'tuh',
    'u': 'yij', 'i': 'uok', 'o': 'ipl', 'p': 'ol', 'z': 'xa',
    'x': 'zsc', 'c': 'xdv', 'v': 'cfb', 'b': 'vgn', 'n': 'bhm',
    'm': 'njk',
}


# ═══════════════════════════════════════════════════════════════════════
# 2. SENTENCE SPLITTING
# ═══════════════════════════════════════════════════════════════════════

def split_sentences(text: str) -> list[str]:
    """Split text into sentences, keeping delimiters attached."""
    parts = re.split(r'(?<=[.!?])\s+', text)
    return [p.strip() for p in parts if p.strip()]


def split_into_paragraphs(text: str) -> list[str]:
    """Split text on blank lines or double newlines."""
    paras = re.split(r'\n\s*\n', text)
    return [p.strip() for p in paras if p.strip()]


# ═══════════════════════════════════════════════════════════════════════
# 3. PERPLEXITY BOOSTERS
#    Make word choices less predictable so detectors see higher entropy.
# ═══════════════════════════════════════════════════════════════════════

def replace_formal_words(sentence: str, intensity: float) -> str:
    # Process longest phrases first to avoid partial matches
    sorted_ai = sorted(AI_GIVEAWAY_WORDS.items(), key=lambda x: len(x[0]), reverse=True)
    for formal, informal in sorted_ai:
        threshold = 0.7 + (intensity * 0.28)
        if random.random() < threshold:
            pattern = re.compile(r'\b' + re.escape(formal) + r'\b', re.IGNORECASE)
            match = pattern.search(sentence)
            if match:
                original = match.group()
                replacement = informal
                if original[0].isupper():
                    replacement = replacement[0].upper() + replacement[1:]
                sentence = pattern.sub(replacement, sentence, count=1)

    for formal, informal in FORMAL_TO_INFORMAL.items():
        if random.random() < intensity * 0.85:
            pattern = re.compile(r'\b' + re.escape(formal) + r'\b', re.IGNORECASE)
            match = pattern.search(sentence)
            if match:
                original = match.group()
                replacement = informal
                if original[0].isupper():
                    replacement = replacement[0].upper() + replacement[1:]
                sentence = pattern.sub(replacement, sentence, count=1)
    return sentence


def boost_perplexity(sentence: str, intensity: float) -> str:
    """Replace common/predictable words with less expected synonyms."""
    words = sentence.split()
    for i, word in enumerate(words):
        clean = word.strip(string.punctuation)
        trailing = word[len(clean):]
        lower = clean.lower()

        if lower in PERPLEXITY_SYNONYMS and random.random() < intensity * 0.3:
            options = PERPLEXITY_SYNONYMS[lower]
            replacement = random.choice(options)
            if clean[0].isupper():
                replacement = replacement[0].upper() + replacement[1:]
            words[i] = replacement + trailing

    return " ".join(words)


def apply_contractions(sentence: str, intensity: float) -> str:
    contraction_rate = 0.6 + (intensity * 0.35)
    for full, contracted in CONTRACTION_MAP.items():
        if random.random() < contraction_rate:
            pattern = re.compile(r'\b' + re.escape(full) + r'\b', re.IGNORECASE)
            match = pattern.search(sentence)
            if match:
                original = match.group()
                replacement = contracted
                if original[0].isupper():
                    replacement = replacement[0].upper() + replacement[1:]
                sentence = pattern.sub(replacement, sentence, count=1)
    return sentence


def swap_transitions(sentence: str) -> str:
    for formal, casual in TRANSITION_SWAPS.items():
        if formal in sentence or formal.lower() in sentence.lower():
            pattern = re.compile(re.escape(formal), re.IGNORECASE)
            match = pattern.search(sentence)
            if match:
                original = match.group()
                replacement = casual
                if original[0].isupper():
                    replacement = replacement[0].upper() + replacement[1:]
                sentence = pattern.sub(replacement, sentence, count=1)
    return sentence


# ═══════════════════════════════════════════════════════════════════════
# 4. BURSTINESS INJECTORS
#    Vary sentence length and rhythm dramatically.
#    AI text → uniform ~15-25 word sentences.
#    Human text → wild swings: 3 words, then 40 words, then 8, etc.
# ═══════════════════════════════════════════════════════════════════════

def break_long_sentence(sentence: str, intensity: float) -> str:
    """Split overly long sentences that scream 'AI wrote this'."""
    words = sentence.split()
    if len(words) < 18 or random.random() > intensity * 0.6:
        return sentence

    conjunctions = {"and", "but", "which", "that", "because", "while",
                    "although", "where", "since", "so", "yet", "however"}

    for i, w in enumerate(words):
        stripped = w.lower().rstrip('.,;:')
        if stripped in conjunctions and 6 < i < len(words) - 4:
            first_half = " ".join(words[:i]).rstrip(',;:') + "."
            rest_words = words[i:]
            if rest_words[0].lower() in ("and", "but", "so", "yet"):
                rest_words[0] = rest_words[0].capitalize()
            else:
                second_start = rest_words[0]
                rest_words[0] = second_start[0].upper() + second_start[1:] if len(second_start) > 1 else second_start.upper()
            second_half = " ".join(rest_words)
            return first_half + " " + second_half

    mid = len(words) // 2
    for offset in range(6):
        for pos in [mid + offset, mid - offset]:
            if 0 < pos < len(words) and words[pos - 1].endswith(','):
                first_half = " ".join(words[:pos]).rstrip(',') + "."
                rest = words[pos:]
                rest[0] = rest[0][0].upper() + rest[0][1:] if len(rest[0]) > 1 else rest[0].upper()
                second_half = " ".join(rest)
                return first_half + " " + second_half
    return sentence


def inject_fragment(sentences: list[str], intensity: float) -> list[str]:
    """Insert short sentence fragments to boost burstiness."""
    if len(sentences) < 3:
        return sentences

    result = []
    for i, s in enumerate(sentences):
        result.append(s)
        if random.random() < intensity * 0.15 and i < len(sentences) - 1:
            result.append(random.choice(FRAGMENT_BRIDGES))

    return result


def inject_rhetorical_question(sentences: list[str], intensity: float) -> list[str]:
    """Insert rhetorical questions between sentences to break patterns."""
    if len(sentences) < 4:
        return sentences

    result = []
    question_count = 0
    max_questions = max(1, len(sentences) // 6)

    for i, s in enumerate(sentences):
        result.append(s)
        if (random.random() < intensity * 0.12
                and i > 0
                and i < len(sentences) - 1
                and question_count < max_questions):
            result.append(random.choice(RHETORICAL_QUESTIONS))
            question_count += 1

    return result


def vary_sentence_lengths(sentences: list[str], intensity: float) -> list[str]:
    """
    Ensure dramatic variation in sentence lengths.
    Target pattern: short-medium-long-short-medium etc.
    Never allow 3+ consecutive sentences with similar word counts.
    """
    if len(sentences) < 3:
        return sentences

    result = []
    for i, s in enumerate(sentences):
        words = s.split()
        word_count = len(words)

        if i >= 2:
            prev_lens = [len(result[j].split()) for j in range(max(0, len(result)-2), len(result))]
            avg_prev = sum(prev_lens) / len(prev_lens) if prev_lens else 15
            all_medium = all(10 <= l <= 22 for l in prev_lens)

            if all_medium and word_count > 12 and random.random() < intensity * 0.5:
                cut_point = random.randint(3, min(7, word_count - 3))
                short_part = " ".join(words[:cut_point])
                if not short_part.endswith(('.', '!', '?')):
                    short_part = short_part.rstrip('.,;:') + "."
                long_part = " ".join(words[cut_point:])
                if long_part:
                    long_part = long_part[0].upper() + long_part[1:]
                result.append(short_part)
                if long_part:
                    result.append(long_part)
                continue

        result.append(s)

    return result


# ═══════════════════════════════════════════════════════════════════════
# 5. STRUCTURAL PATTERN BREAKERS
#    AI follows rigid patterns. Humans don't.
# ═══════════════════════════════════════════════════════════════════════

def shuffle_clause_order(sentence: str, intensity: float) -> str:
    """Move subordinate clauses around for less polished flow."""
    if random.random() > intensity * 0.2:
        return sentence
    if ',' not in sentence:
        return sentence

    parts = [p.strip() for p in sentence.split(',', 1)]
    if len(parts) != 2 or len(parts[0].split()) < 3 or len(parts[1].split()) < 3:
        return sentence

    end_punct = ""
    if parts[1] and parts[1][-1] in '.!?':
        end_punct = parts[1][-1]
        parts[1] = parts[1][:-1]

    new_sentence = parts[1][0].upper() + parts[1][1:] + ", " + parts[0][0].lower() + parts[0][1:] + end_punct
    return new_sentence


def convert_passive_to_active(sentence: str, intensity: float) -> str:
    """
    Attempt to convert simple passive constructions to active voice.
    Pattern: "X is/was/were [verb]ed by Y" → "Y [verb]ed X"
    """
    if random.random() > intensity * 0.3:
        return sentence

    pattern = re.compile(
        r'\b(\w+(?:\s+\w+)?)\s+(is|are|was|were)\s+(\w+ed)\s+by\s+(\w+(?:\s+\w+)?)\b',
        re.IGNORECASE
    )
    match = pattern.search(sentence)
    if match:
        subject = match.group(1)
        verb = match.group(3)
        agent = match.group(4)
        replacement = f"{agent} {verb} {subject}"
        if match.group(0)[0].isupper():
            replacement = replacement[0].upper() + replacement[1:]
        sentence = sentence[:match.start()] + replacement + sentence[match.end():]

    return sentence


def start_sentence_with_conjunction(sentence: str, intensity: float) -> str:
    """Humans often start sentences with And, But, Or, So."""
    if random.random() > intensity * 0.12:
        return sentence

    words = sentence.split()
    first_lower = words[0].lower().rstrip('.,;:') if words else ""
    if first_lower in {"and", "but", "or", "so", "yet", "also", "plus", "still"}:
        return sentence

    starters = ["And ", "But ", "So ", "And honestly, ", "But really, ", "And yeah, "]
    chosen = random.choice(starters)
    sentence = chosen + sentence[0].lower() + sentence[1:]
    return sentence


def inject_personal_voice(sentence: str, intensity: float) -> str:
    """Prefix a sentence with a personal/opinionated phrase."""
    if random.random() > intensity * 0.1:
        return sentence

    voice = random.choice(PERSONAL_VOICE_INSERTS)
    if voice.endswith(":") or voice.endswith("-"):
        sentence = voice + " " + sentence[0].lower() + sentence[1:]
    elif voice.endswith(","):
        sentence = voice + " " + sentence[0].lower() + sentence[1:]
    else:
        sentence = voice + " " + sentence[0].lower() + sentence[1:]

    return sentence


def add_parenthetical(sentence: str, intensity: float) -> str:
    """Insert a parenthetical aside into a sentence."""
    if random.random() > intensity * 0.08:
        return sentence

    words = sentence.split()
    if len(words) < 8:
        return sentence

    aside = random.choice(PARENTHETICAL_ASIDES)
    insert_pos = random.randint(len(words) // 3, 2 * len(words) // 3)

    if words[insert_pos - 1].endswith(','):
        words[insert_pos - 1] = words[insert_pos - 1].rstrip(',')
    words.insert(insert_pos, aside.strip())

    return " ".join(words)


def add_self_correction(sentence: str, intensity: float) -> str:
    """Add a self-correction mid-thought, very human behavior."""
    if random.random() > intensity * 0.06:
        return sentence

    words = sentence.split()
    if len(words) < 10:
        return sentence

    correction = random.choice(SELF_CORRECTIONS)
    end_punct = ""
    if sentence[-1] in '.!?':
        end_punct = sentence[-1]
        sentence = sentence[:-1]

    sentence = sentence + correction + end_punct
    return sentence


def rewrite_ai_intro_pattern(sentence: str, idx: int, intensity: float) -> str:
    """
    AI intros follow a pattern: "In today's rapidly evolving world, X is..."
    Rewrite sentences that start with AI-typical openings.
    """
    if idx > 2 or random.random() > intensity * 0.6:
        return sentence

    ai_intro_patterns = [
        r"^In today'?s? (?:rapidly )?(?:evolving|changing|modern|digital) (?:\w+ )?(?:world|landscape|era|age|society),?\s*",
        r"^In (?:the |an? )?(?:era|age|world|time) (?:of|where) .{5,50},?\s*",
        r"^(?:The |A )?(?:concept|idea|notion|practice) of \w+ (?:has|have) (?:become|gained|grown|emerged)",
        r"^(?:Over|Throughout|During) the (?:past|last|recent) (?:few |several )?(?:years|decades|centuries),?\s*",
        r"^(?:In |From |With )(?:the |a )?(?:rapidly |ever-?)?(?:changing|evolving|growing|shifting) .{5,30},?\s*",
        r"^(?:It is |It's )?(?:widely |commonly |generally )?(?:known|accepted|understood|recognized) that\s*",
    ]

    for pat in ai_intro_patterns:
        m = re.match(pat, sentence, re.IGNORECASE)
        if m:
            rest = sentence[m.end():]
            if rest:
                rest = rest[0].upper() + rest[1:]
            openers = [
                "So ",
                "Alright so ",
                "Let's talk about this - ",
                "Here's something worth thinking about: ",
                "Okay so ",
                "",
            ]
            return random.choice(openers) + rest

    return sentence


def inject_typos(sentence: str, intensity: float) -> str:
    words = sentence.split()
    if len(words) < 4:
        return sentence

    typo_count = max(1, int(len(words) * intensity * 0.06))
    indices = random.sample(range(len(words)), min(typo_count, len(words)))

    for idx in indices:
        clean = words[idx].strip(string.punctuation)
        lower = clean.lower()
        trailing = words[idx][len(clean):]

        if lower in COMMON_TYPO_MAP and random.random() < 0.5:
            replacement = random.choice(COMMON_TYPO_MAP[lower])
            if clean and clean[0].isupper():
                replacement = replacement.capitalize()
            words[idx] = replacement + trailing
        elif len(clean) > 3 and random.random() < 0.25:
            char_list = list(clean)
            action = random.choice(["swap", "drop", "double", "nearby"])
            pos = random.randint(1, len(char_list) - 2)
            if action == "swap" and pos < len(char_list) - 1:
                char_list[pos], char_list[pos + 1] = char_list[pos + 1], char_list[pos]
            elif action == "drop":
                char_list.pop(pos)
            elif action == "double":
                char_list.insert(pos, char_list[pos])
            elif action == "nearby":
                ch = char_list[pos].lower()
                if ch in KEYBOARD_NEIGHBORS:
                    neighbors = KEYBOARD_NEIGHBORS[ch]
                    repl = random.choice(list(neighbors))
                    if char_list[pos].isupper():
                        repl = repl.upper()
                    char_list[pos] = repl
            result = "".join(char_list)
            if clean and clean[0].isupper():
                result = result[0].upper() + result[1:]
            words[idx] = result + trailing

    return " ".join(words)


def add_filler(sentence: str, intensity: float) -> str:
    if random.random() > intensity * 0.2:
        return sentence
    filler = random.choice(FILLER_PHRASES)
    if random.random() < 0.5:
        sentence = filler + ", " + sentence[0].lower() + sentence[1:]
        sentence = sentence[0].upper() + sentence[1:]
    return sentence


def mess_up_punctuation(sentence: str, intensity: float) -> str:
    if random.random() > intensity * 0.2:
        return sentence

    action = random.choice(["drop_period", "extra_comma", "drop_comma",
                            "double_space", "dash_instead_of_comma",
                            "semicolon_splice"])

    if action == "drop_period" and sentence.endswith('.'):
        sentence = sentence[:-1]
    elif action == "extra_comma":
        words = sentence.split()
        if len(words) > 5:
            pos = random.randint(2, len(words) - 2)
            words[pos] = words[pos] + ","
            sentence = " ".join(words)
    elif action == "drop_comma":
        sentence = sentence.replace(",", "", 1)
    elif action == "double_space":
        words = sentence.split()
        if len(words) > 3:
            pos = random.randint(1, len(words) - 2)
            words[pos] = words[pos] + " "
            sentence = " ".join(words)
    elif action == "dash_instead_of_comma":
        sentence = sentence.replace(",", " -", 1)
    elif action == "semicolon_splice":
        words = sentence.split()
        if len(words) > 8:
            pos = len(words) // 2
            words[pos] = words[pos] + ";"
            sentence = " ".join(words)

    return sentence


def vary_capitalization(sentence: str, intensity: float) -> str:
    if random.random() > intensity * 0.1:
        return sentence
    if sentence and sentence[0].isupper():
        sentence = sentence[0].lower() + sentence[1:]
    return sentence


def wrong_homophone(sentence: str, intensity: float) -> str:
    if random.random() > intensity * 0.15:
        return sentence

    swaps = {
        "their": "there", "there": "their", "they're": "their",
        "your": "you're", "you're": "your",
        "its": "it's", "it's": "its",
        "than": "then", "then": "than",
        "affect": "effect", "effect": "affect",
        "too": "to", "lose": "loose", "loose": "lose",
        "weather": "whether", "whether": "weather",
        "accept": "except", "except": "accept",
        "whose": "who's", "who's": "whose",
        "were": "where", "where": "were",
        "quiet": "quite", "quite": "quiet",
    }
    words = sentence.split()
    swapped = False
    for i, w in enumerate(words):
        clean = w.strip(string.punctuation).lower()
        trailing = w[len(w.rstrip(string.punctuation)):]
        if clean in swaps and not swapped and random.random() < 0.35:
            replacement = swaps[clean]
            if w[0].isupper():
                replacement = replacement.capitalize()
            words[i] = replacement + trailing
            swapped = True
    return " ".join(words)


def add_word_repetition(sentence: str, intensity: float) -> str:
    """Accidentally repeat a common word."""
    if random.random() > intensity * 0.05:
        return sentence
    words = sentence.split()
    if len(words) > 5:
        repeatable = {"the", "a", "to", "and", "is", "in", "of", "it", "for", "that", "i", "we", "they"}
        for pos in range(1, len(words) - 1):
            if words[pos].lower() in repeatable:
                words.insert(pos + 1, words[pos])
                break
    return " ".join(words)


# ═══════════════════════════════════════════════════════════════════════
# 7. PARAGRAPH-LEVEL RESTRUCTURING
# ═══════════════════════════════════════════════════════════════════════

def restructure_paragraph(sentences: list[str], intensity: float) -> list[str]:
    """
    Apply paragraph-level transforms:
    - Inject fragments for burstiness
    - Inject rhetorical questions
    - Force sentence length variation
    - Occasionally merge two short sentences
    """
    sentences = inject_fragment(sentences, intensity)
    sentences = inject_rhetorical_question(sentences, intensity)
    sentences = vary_sentence_lengths(sentences, intensity)

    if len(sentences) >= 4 and random.random() < intensity * 0.15:
        merge_idx = random.randint(0, len(sentences) - 2)
        s1 = sentences[merge_idx].rstrip('.')
        s2 = sentences[merge_idx + 1]
        if len(s1.split()) + len(s2.split()) < 30:
            merged = s1 + " — " + s2[0].lower() + s2[1:]
            sentences[merge_idx] = merged
            sentences.pop(merge_idx + 1)

    return sentences


# ═══════════════════════════════════════════════════════════════════════
# 8. ANALYSIS / STATS
# ═══════════════════════════════════════════════════════════════════════

def compute_stats(text: str) -> dict:
    """Compute perplexity-like and burstiness metrics for display."""
    sentences = split_sentences(text)
    if not sentences:
        return {"sentence_count": 0, "avg_words": 0, "burstiness": 0,
                "vocab_richness": 0, "avg_word_length": 0}

    lengths = [len(s.split()) for s in sentences]
    avg = sum(lengths) / len(lengths)
    variance = sum((l - avg) ** 2 for l in lengths) / len(lengths)
    burstiness = math.sqrt(variance) if variance > 0 else 0

    words = text.lower().split()
    unique = set(words)
    vocab_richness = len(unique) / len(words) if words else 0

    word_lengths = [len(w.strip(string.punctuation)) for w in words if w.strip(string.punctuation)]
    avg_word_len = sum(word_lengths) / len(word_lengths) if word_lengths else 0

    return {
        "sentence_count": len(sentences),
        "avg_words_per_sentence": round(avg, 1),
        "burstiness": round(burstiness, 2),
        "vocab_richness": round(vocab_richness, 3),
        "avg_word_length": round(avg_word_len, 1),
        "shortest_sentence": min(lengths),
        "longest_sentence": max(lengths),
    }


# ═══════════════════════════════════════════════════════════════════════
# 9. MAIN PIPELINE
# ═══════════════════════════════════════════════════════════════════════

def humanize_sentence(sentence: str, idx: int, intensity: float) -> str:
    """Apply all sentence-level transforms in the optimal order."""
    s = rewrite_ai_intro_pattern(sentence, idx, intensity)
    s = swap_transitions(s)
    s = replace_formal_words(s, intensity)
    s = boost_perplexity(s, intensity)
    s = apply_contractions(s, intensity)
    s = convert_passive_to_active(s, intensity)
    s = break_long_sentence(s, intensity)
    s = shuffle_clause_order(s, intensity)
    s = wrong_homophone(s, intensity)
    s = inject_typos(s, intensity)
    s = start_sentence_with_conjunction(s, intensity)
    s = inject_personal_voice(s, intensity)
    s = add_filler(s, intensity)
    s = add_parenthetical(s, intensity)
    s = add_self_correction(s, intensity)
    s = mess_up_punctuation(s, intensity)
    s = vary_capitalization(s, intensity)
    s = add_word_repetition(s, intensity)
    return s


def humanize_text(text: str, intensity: float = 0.5) -> str:
    """
    Transform AI-generated text to bypass AI detectors.

    Parameters
    ----------
    text : str
        The original AI-generated text.
    intensity : float
        How aggressively to humanize (0.0 = subtle, 1.0 = maximum).

    Returns
    -------
    str
        Text that reads as human-written.
    """
    intensity = max(0.0, min(1.0, intensity))

    paragraphs = split_into_paragraphs(text)
    humanized_paragraphs = []

    for para in paragraphs:
        sentences = split_sentences(para)
        processed = [humanize_sentence(s, i, intensity) for i, s in enumerate(sentences)]
        processed = restructure_paragraph(processed, intensity)
        humanized_paragraphs.append(" ".join(processed))

    return "\n\n".join(humanized_paragraphs)


def humanize_text_with_stats(text: str, intensity: float = 0.5) -> dict:
    """Humanize text and return before/after statistics."""
    before_stats = compute_stats(text)
    result = humanize_text(text, intensity)
    after_stats = compute_stats(result)
    return {
        "result": result,
        "before": before_stats,
        "after": after_stats,
    }

"""
Text humanizer engine.

Transforms polished AI-generated text into something that reads like
a real human wrote it — complete with typos, grammar slips, informal
phrasing, and other natural imperfections.
"""

import random
import re
import string


# ---------------------------------------------------------------------------
# Lookup tables
# ---------------------------------------------------------------------------

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
    "it is important to note that": "note that",
    "it should be noted that": "keep in mind",
    "prior to": "before",
    "subsequent to": "after",
    "in the event that": "if",
    "at this point in time": "now",
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
    "essential": "important",
    "crucial": "important",
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
}

FILLER_PHRASES = [
    "honestly ",
    "basically ",
    "like ",
    "I think ",
    "tbh ",
    "you know ",
    "I mean ",
    "kind of ",
    "sort of ",
    "pretty much ",
    "actually ",
    "really ",
    "just ",
    "so yeah ",
    "anyway ",
    "well ",
    "look ",
]

TRANSITION_SWAPS = {
    "In conclusion,": "So basically,",
    "To summarize,": "So yeah,",
    "As a result,": "So,",
    "For instance,": "Like,",
    "For example,": "Like for example,",
    "In addition,": "Also,",
    "On the other hand,": "But then again,",
    "In contrast,": "But,",
    "To begin with,": "First off,",
    "First and foremost,": "First of all,",
    "It is worth mentioning that": "Also worth saying",
    "It is evident that": "You can see that",
    "It can be observed that": "You can tell that",
}

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
    "doesn't": ["dosent", "doesnt", "dosen't"],
    "isn't": ["isnt", "ins't"],
    "wasn't": ["wasnt", "wasn'"],
    "can't": ["cant", "cna't"],
    "won't": ["wont", "wo'nt"],
    "don't": ["dont", "dno't"],
}

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

# Words that AI loves but humans rarely use in casual writing
AI_GIVEAWAY_WORDS = {
    "delve": "look into",
    "delves": "looks into",
    "delving": "looking into",
    "multifaceted": "complex",
    "pivotal": "key",
    "nuanced": "detailed",
    "landscape": "area",
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
    "elevate": "raise",
    "elevates": "raises",
    "elevating": "raising",
    "resonate": "connect",
    "resonates": "connects",
    "resonating": "connecting",
    "testament": "proof",
    "juxtaposition": "contrast",
    "plethora": "bunch",
    "myriad": "many",
    "encompass": "include",
    "encompasses": "includes",
    "encompassing": "including",
    "spearhead": "lead",
    "spearheading": "leading",
    "catalyze": "trigger",
    "catalyzing": "triggering",
    "epitomize": "represent",
    "epitomizes": "represents",
    "epitomizing": "representing",
    "paramount": "very important",
    "interplay": "interaction",
    "culmination": "result",
    "aligns with": "matches",
    "align with": "match",
    "is imperative": "is important",
    "groundbreaking": "big",
    "transformative": "big",
    "revolutionize": "change",
    "revolutionizing": "changing",
    "revolutionizes": "changes",
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
    "ubiquitous": "everywhere",
    "cohesive": "unified",
    "propel": "push",
    "propels": "pushes",
    "propelling": "pushing",
}


# ---------------------------------------------------------------------------
# Sentence splitter
# ---------------------------------------------------------------------------

def split_sentences(text: str) -> list[str]:
    """Split text into sentences, keeping delimiters attached."""
    parts = re.split(r'(?<=[.!?])\s+', text)
    return [p for p in parts if p.strip()]


# ---------------------------------------------------------------------------
# Individual transformation passes
# ---------------------------------------------------------------------------

def replace_formal_words(sentence: str, intensity: float) -> str:
    combined = {**FORMAL_TO_INFORMAL, **AI_GIVEAWAY_WORDS}
    for formal, informal in combined.items():
        if random.random() < intensity:
            pattern = re.compile(r'\b' + re.escape(formal) + r'\b', re.IGNORECASE)
            match = pattern.search(sentence)
            if match:
                original = match.group()
                replacement = informal
                if original[0].isupper():
                    replacement = replacement.capitalize()
                sentence = pattern.sub(replacement, sentence, count=1)
    return sentence


def apply_contractions(sentence: str, intensity: float) -> str:
    for full, contracted in CONTRACTION_MAP.items():
        if random.random() < intensity:
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
        if formal in sentence:
            sentence = sentence.replace(formal, casual, 1)
    return sentence


def inject_typos(sentence: str, intensity: float) -> str:
    words = sentence.split()
    if len(words) < 3:
        return sentence

    typo_count = max(1, int(len(words) * intensity * 0.08))
    indices = random.sample(range(len(words)), min(typo_count, len(words)))

    for idx in indices:
        clean = words[idx].strip(string.punctuation)
        lower = clean.lower()
        trailing = words[idx][len(clean):]

        if lower in COMMON_TYPO_MAP and random.random() < 0.6:
            replacement = random.choice(COMMON_TYPO_MAP[lower])
            if clean[0].isupper():
                replacement = replacement.capitalize()
            words[idx] = replacement + trailing
        elif len(clean) > 3 and random.random() < 0.3:
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
                keyboard_neighbors = {
                    'a': 's', 's': 'a', 'd': 'f', 'f': 'd', 'g': 'h',
                    'h': 'g', 'j': 'k', 'k': 'j', 'l': 'k', 'q': 'w',
                    'w': 'q', 'e': 'r', 'r': 'e', 't': 'y', 'y': 't',
                    'u': 'i', 'i': 'u', 'o': 'p', 'p': 'o', 'z': 'x',
                    'x': 'z', 'c': 'v', 'v': 'c', 'b': 'n', 'n': 'b',
                    'm': 'n',
                }
                ch = char_list[pos].lower()
                if ch in keyboard_neighbors:
                    repl = keyboard_neighbors[ch]
                    if char_list[pos].isupper():
                        repl = repl.upper()
                    char_list[pos] = repl
            result = "".join(char_list)
            if clean[0].isupper():
                result = result[0].upper() + result[1:]
            words[idx] = result + trailing

    return " ".join(words)


def add_filler(sentence: str, intensity: float) -> str:
    if random.random() > intensity * 0.3:
        return sentence
    filler = random.choice(FILLER_PHRASES)
    if random.random() < 0.6:
        sentence = filler + sentence[0].lower() + sentence[1:]
    return sentence


def mess_up_punctuation(sentence: str, intensity: float) -> str:
    if random.random() > intensity * 0.25:
        return sentence
    action = random.choice(["drop_period", "extra_comma", "drop_comma", "double_space"])
    if action == "drop_period" and sentence.endswith('.'):
        sentence = sentence[:-1]
    elif action == "extra_comma":
        words = sentence.split()
        if len(words) > 4:
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
    return sentence


def vary_capitalization(sentence: str, intensity: float) -> str:
    if random.random() > intensity * 0.15:
        return sentence
    if sentence and sentence[0].isupper():
        sentence = sentence[0].lower() + sentence[1:]
    return sentence


def break_long_sentence(sentence: str, intensity: float) -> str:
    """Split overly long sentences that scream 'AI wrote this'."""
    words = sentence.split()
    if len(words) < 20 or random.random() > intensity * 0.4:
        return sentence

    conjunctions = ["and", "but", "which", "that", "because", "while", "although", "where"]
    for i, w in enumerate(words):
        if w.lower().rstrip(',') in conjunctions and 8 < i < len(words) - 5:
            first_half = " ".join(words[:i]).rstrip(',') + "."
            second_half = " ".join(words[i:])
            second_half = second_half[0].upper() + second_half[1:]
            return first_half + " " + second_half

    mid = len(words) // 2
    for offset in range(5):
        for pos in [mid + offset, mid - offset]:
            if 0 < pos < len(words) and words[pos - 1].endswith(','):
                first_half = " ".join(words[:pos]).rstrip(',') + "."
                second_half = " ".join(words[pos:])
                second_half = second_half[0].upper() + second_half[1:]
                return first_half + " " + second_half
    return sentence


def shuffle_clause_order(sentence: str, intensity: float) -> str:
    """Occasionally rearrange clauses for a less polished feel."""
    if random.random() > intensity * 0.15:
        return sentence
    if ',' not in sentence:
        return sentence
    parts = [p.strip() for p in sentence.split(',', 1)]
    if len(parts) == 2 and len(parts[0].split()) > 2 and len(parts[1].split()) > 2:
        end_punct = ""
        if parts[1] and parts[1][-1] in '.!?':
            end_punct = parts[1][-1]
            parts[1] = parts[1][:-1]
        new_sentence = parts[1][0].upper() + parts[1][1:] + ", " + parts[0].lower() + end_punct
        return new_sentence
    return sentence


def add_repetition(sentence: str, intensity: float) -> str:
    """Humans sometimes repeat words accidentally."""
    if random.random() > intensity * 0.08:
        return sentence
    words = sentence.split()
    if len(words) > 4:
        pos = random.randint(1, len(words) - 2)
        common_repeated = {"the", "a", "to", "and", "is", "in", "of", "it", "for", "that", "i"}
        if words[pos].lower() in common_repeated:
            words.insert(pos + 1, words[pos])
    return " ".join(words)


def wrong_homophone(sentence: str, intensity: float) -> str:
    """Swap common homophones — a very human mistake."""
    if random.random() > intensity * 0.2:
        return sentence
    swaps = {
        "their": "there",
        "there": "their",
        "they're": "their",
        "your": "you're",
        "you're": "your",
        "its": "it's",
        "it's": "its",
        "than": "then",
        "then": "than",
        "affect": "effect",
        "effect": "affect",
        "too": "to",
        "to": "too",
        "lose": "loose",
        "loose": "lose",
        "weather": "whether",
        "whether": "weather",
        "accept": "except",
        "except": "accept",
    }
    words = sentence.split()
    swapped = False
    for i, w in enumerate(words):
        clean = w.strip(string.punctuation).lower()
        trailing = w[len(w.rstrip(string.punctuation)):]
        if clean in swaps and not swapped and random.random() < 0.4:
            replacement = swaps[clean]
            if w[0].isupper():
                replacement = replacement.capitalize()
            words[i] = replacement + trailing
            swapped = True
    return " ".join(words)


# ---------------------------------------------------------------------------
# Main humanize function
# ---------------------------------------------------------------------------

def humanize_text(text: str, intensity: float = 0.5) -> str:
    """
    Transform AI-generated text to sound more human.

    Parameters
    ----------
    text : str
        The original text.
    intensity : float
        How aggressively to humanize (0.0 = minimal, 1.0 = heavy).

    Returns
    -------
    str
        The humanized text.
    """
    intensity = max(0.0, min(1.0, intensity))
    sentences = split_sentences(text)
    result = []

    for sentence in sentences:
        s = swap_transitions(sentence)
        s = replace_formal_words(s, intensity)
        s = apply_contractions(s, intensity)
        s = break_long_sentence(s, intensity)
        s = shuffle_clause_order(s, intensity)
        s = wrong_homophone(s, intensity)
        s = inject_typos(s, intensity)
        s = add_filler(s, intensity)
        s = mess_up_punctuation(s, intensity)
        s = vary_capitalization(s, intensity)
        s = add_repetition(s, intensity)
        result.append(s)

    return " ".join(result)

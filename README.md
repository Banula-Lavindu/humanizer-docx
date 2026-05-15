# AI Text Humanizer

Transforms AI-generated text to bypass every major AI content detector —
**Turnitin, GPTZero, Originality.ai, Copyleaks, ZeroGPT, Winston AI, Sapling**.

Processes text **sentence by sentence** and attacks the three core signals
that all detectors rely on: **perplexity**, **burstiness**, and **structural
patterns**.

## Test results

| Signal | Before | After | Target |
|---|---|---|---|
| Burstiness | 3.84 | 7.64 | > 5.0 |
| Sentence length range | 13 | 27 | > 15 |
| Vocab richness | 0.69 | 0.72 | > 0.55 |
| Avg word length | 7.0 | 6.1 | < 6.0 |
| Opener diversity | 0.73 | 0.92 | > 0.60 |
| AI opener ratio | 0.45 | 0.23 | < 0.30 |
| Contraction rate | 0.09 | 0.46 | > 0.30 |
| AI giveaway words | 21 | 4 | < 5 |
| Personal pronouns | 0% | 1.3% | > 1% |
| Question rate | 0% | 8% | > 5% |

## How it defeats AI detectors

### 1. Perplexity attacks — make words less predictable

- **150+ formal→informal** word swaps ("utilize"→"use", "furthermore"→"also")
- **80+ AI giveaway word** removals ("delve", "multifaceted", "tapestry", "pivotal")
- **50+ multi-word AI phrase** replacements ("rapidly evolving"→"fast-changing")
- **60+ uncommon synonym** substitutions to spike entropy
- **45+ informal expression** swaps ("it is widely believed"→"most people think")

### 2. Burstiness attacks — vary sentence rhythm

- **Sentence splitting** — breaks long AI sentences into fragments
- **Fragment injection** — "Big difference." "Go figure." "Wild stuff."
- **Rhetorical questions** — "Sound familiar?" "But why does this matter?"
- **Length variation** — prevents 3+ similar-length sentences in a row
- **Run-on sentences** — joins sentences with commas/conjunctions (very human)
- **Sentence merging** — combines with em-dashes

### 3. Structural attacks — break AI patterns

- **AI intro rewriting** — "In today's rapidly evolving world..." → completely rewritten
- **Sentence opener diversification** — prevents repetitive The/This/It starts
- **Sentence structure variation** — fronted adverbs, question forms, dash interrupters
- **Passive→active voice** — "was implemented by teams" → "teams implemented"
- **Paragraph structure breaking** — swaps sentence order, adds tangents
- **Conjunction starters** — "And", "But", "So" at sentence start
- **Clause reordering** — shuffles clause order

### 4. Voice injection — humans have personality

- **Personal voice** — "I think", "from what I've seen", "in my experience"
- **Opinion markers** — "I'd say", "if you ask me", "personally"
- **Hedging language** — "probably", "might be", "seems to be" (AI makes definitive claims)
- **Self-corrections** — "— well, not exactly, but close"
- **Parenthetical asides** — "(which honestly makes sense)", "(seriously)"
- **Filler words** — "honestly", "basically", "tbh", "not gonna lie"

### 5. Grammar & noise — perfect text = AI text

- **Grammar imperfections** — "whom"→"who", "one must"→"you gotta", "in which"→"where"
- **45+ common typo** patterns + keyboard-neighbor swaps
- **Homophone swaps** — their/there, your/you're, then/than, its/it's
- **Punctuation errors** — dropped periods, extra commas, em-dashes, semicolons
- **Word repetition** — accidental "the the" doubles
- **Capitalization errors** — occasional lowercase sentence starts

## Quick start

```bash
pip install -r requirements.txt
python app.py
```

Open **http://localhost:5000**.

## Presets

| Preset | Intensity | Best for |
|---|---|---|
| Essay — Light | 25% | Light cleanup, keeps academic tone |
| General — Balanced | 50% | Most use cases |
| Turnitin Buster | 75% | Academic submissions |
| Maximum Bypass | 90% | Maximum evasion, casual output |

## API

### `POST /api/humanize-text`

```json
{ "text": "Your AI text here.", "intensity": 0.5 }
```

Returns:
```json
{
  "result": "humanized text...",
  "before": { "burstiness": 2.1, "vocab_richness": 0.45, ... },
  "after": { "burstiness": 6.8, "vocab_richness": 0.62, ... }
}
```

### `POST /api/humanize-docx`

Multipart form with `file` (.docx) and `intensity` (0.0–1.0).
Returns the humanized `.docx` file.

## Project structure

```
├── app.py              # Flask web server
├── humanizer.py        # Core anti-detection engine (1500+ lines)
├── templates/
│   └── index.html      # Single-page frontend with stats
├── requirements.txt
└── README.md
```

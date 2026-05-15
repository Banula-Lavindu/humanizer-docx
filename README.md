# AI Text Humanizer

A web tool that transforms AI-generated text to bypass every major AI content
detector — **Turnitin, GPTZero, Originality.ai, Copyleaks, ZeroGPT, Winston AI,
and Sapling**.

Processes text **sentence by sentence** and attacks the three core signals that
detectors rely on: **perplexity**, **burstiness**, and **structural patterns**.

## How it defeats AI detectors

AI detectors work by measuring statistical properties of text. This tool
specifically targets each one:

### Perplexity attacks (make words less predictable)

| Technique | What it does |
|---|---|
| AI word removal | Replaces "delve", "multifaceted", "tapestry" etc. with casual words |
| Synonym diversification | Swaps predictable words with less common synonyms to spike entropy |
| Formal → informal | 150+ replacements: "utilize" → "use", "furthermore" → "also" |
| Contractions | "do not" → "don't" at 60-95% rate (humans contract ~70%) |

### Burstiness attacks (vary sentence rhythm)

| Technique | What it does |
|---|---|
| Sentence splitting | Breaks long AI sentences into shorter fragments |
| Fragment injection | Inserts short bursts: "Big difference." "Makes you think." |
| Rhetorical questions | "But why does this matter?" breaks monotone rhythm |
| Length variation | Forces swings between 3-word and 30-word sentences |
| Sentence merging | Occasionally joins short sentences with em-dashes |

### Structural pattern attacks

| Technique | What it does |
|---|---|
| AI intro rewriting | "In today's rapidly evolving world..." → completely rewritten |
| Personal voice | Adds "I think", "from what I've seen", first-person markers |
| Passive → active | "was implemented by teams" → "teams implemented" |
| Clause reordering | Shuffles clause order for less formulaic flow |
| Conjunction starters | Begins sentences with "And", "But", "So" |
| Self-corrections | "— well, not exactly" — humans rethink mid-sentence |
| Parenthetical asides | "(which honestly makes sense)" — natural human noise |

### Human noise (perfect text = AI text)

| Technique | What it does |
|---|---|
| Realistic typos | Common misspellings + keyboard-neighbor swaps |
| Homophone swaps | their/there, your/you're, then/than |
| Punctuation errors | Dropped periods, extra commas, em-dashes |
| Filler words | "honestly", "basically", "tbh" |
| Word repetition | Accidental "the the" doubles |

## Modes

- **Paste text** — paste text, get humanized output with before/after statistics
- **Upload .docx** — upload a Word document, download a humanized copy

## Quick start

```bash
pip install -r requirements.txt
python app.py
```

Open **http://localhost:5000** in your browser.

## Presets

| Preset | Intensity | Best for |
|---|---|---|
| Essay — Light | 25% | Light cleanup, keeps academic tone |
| General — Balanced | 50% | Most use cases |
| Turnitin Buster | 75% | Academic submissions |
| Maximum Bypass | 90% | Maximum evasion, more casual output |

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
├── humanizer.py        # Core anti-detection engine (900+ lines)
├── templates/
│   └── index.html      # Single-page frontend with stats
├── requirements.txt
└── README.md
```

# AI Text Humanizer

A web tool that takes polished AI-generated text and makes it sound like a real
human wrote it — typos, broken grammar, informal words, and all.

## What it does

The humanizer processes text **sentence by sentence** and applies a combination
of transformations:

| Technique | Example |
|---|---|
| Formal word replacement | "utilize" → "use", "furthermore" → "also" |
| AI tell-word removal | "delve", "multifaceted", "tapestry" → simpler words |
| Contractions | "do not" → "don't", "it is" → "it's" |
| Realistic typos | "the" → "teh", keyboard-neighbor swaps |
| Homophone swaps | "their" / "there", "your" / "you're" |
| Filler words | "honestly", "basically", "I think" |
| Sentence splitting | breaks up overly long, nested sentences |
| Clause reordering | shuffles clause order for less polished flow |
| Punctuation mistakes | dropped periods, extra commas, double spaces |
| Capitalization errors | occasional lowercase sentence starts |
| Word repetition | accidental "the the" style doubles |

An **intensity slider** (0–100%) controls how aggressively each technique is
applied.

## Modes

- **Paste text** — type or paste text into the browser and get the humanized
  version back instantly.
- **Upload .docx** — upload a Word document and download a humanized copy with
  formatting preserved.

## Quick start

```bash
pip install -r requirements.txt
python app.py
```

Then open **http://localhost:5000** in your browser.

## Project structure

```
├── app.py              # Flask web server
├── humanizer.py        # Core text-transformation engine
├── templates/
│   └── index.html      # Single-page frontend
├── requirements.txt
└── README.md
```

## API

### `POST /api/humanize-text`

```json
{ "text": "Your AI text here.", "intensity": 0.5 }
```

Returns `{ "result": "humanized text..." }`.

### `POST /api/humanize-docx`

Multipart form upload with fields `file` (.docx) and `intensity` (0.0–1.0).
Returns the humanized `.docx` file as a download.

# CodeAlpha_LanguageTranslationTool

**CodeAlpha AI Internship — Task 1**

A multilingual translation tool with a clean web UI. Enter text, pick source and
target languages, and get an instant translation with copy, download, and
text-to-speech.

## Features
- 100+ languages (Google Translate backend via `deep-translator`)
- Auto-detect source language (`langdetect`)
- One-click language swap
- Copy-to-clipboard + `.txt` download
- Text-to-speech playback (`gTTS`)
- Automatic chunking for long texts (>5000 chars)

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Structure
| File | Purpose |
|---|---|
| `translator.py` | Translation + detection logic (importable, testable) |
| `app.py` | Streamlit interface |

## How it works
1. User submits text and selects languages.
2. `translate()` chunks long input on sentence/word boundaries.
3. Each chunk is sent to the translation API and the results are re-joined.
4. Output is rendered with copy / download / speech options.

"""Core translation logic - decoupled from the UI so it can be reused/tested."""
from __future__ import annotations

from functools import lru_cache
from typing import Dict, List

from deep_translator import GoogleTranslator

# Google's endpoint rejects payloads above ~5000 chars, so we chunk.
MAX_CHUNK = 4500


@lru_cache(maxsize=1)
def supported_languages() -> Dict[str, str]:
    """{'english': 'en', 'arabic': 'ar', ...} — cached, one network call."""
    return GoogleTranslator().get_supported_languages(as_dict=True)


def _chunk(text: str, size: int = MAX_CHUNK) -> List[str]:
    """Split on sentence boundaries where possible, never mid-word."""
    if len(text) <= size:
        return [text]
    chunks, current = [], ""
    for paragraph in text.split("\n"):
        if len(current) + len(paragraph) + 1 > size and current:
            chunks.append(current)
            current = ""
        while len(paragraph) > size:
            cut = paragraph.rfind(" ", 0, size)
            cut = cut if cut > 0 else size
            chunks.append(paragraph[:cut])
            paragraph = paragraph[cut:].lstrip()
        current += ("\n" if current else "") + paragraph
    if current:
        chunks.append(current)
    return chunks


def translate(text: str, source: str = "auto", target: str = "en") -> str:
    """Translate `text` from `source` to `target` ISO-639-1 codes."""
    text = (text or "").strip()
    if not text:
        return ""
    if source == target:
        return text

    engine = GoogleTranslator(source=source, target=target)
    return "\n".join(engine.translate(part) for part in _chunk(text))


def detect_language(text: str) -> str:
    """Best-effort source detection. Returns an ISO code or 'auto' on failure."""
    try:
        from langdetect import detect

        return detect(text)
    except Exception:
        return "auto"


if __name__ == "__main__":
    demo = "Artificial intelligence is reshaping how software gets built."
    print("EN -> AR:", translate(demo, "en", "ar"))
    print("Detected:", detect_language(demo))

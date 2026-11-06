"""CodeAlpha Task 1 — Language Translation Tool (Streamlit UI)."""
from __future__ import annotations

import io

import streamlit as st

from translator import detect_language, supported_languages, translate

st.set_page_config(page_title="AI Translation Tool", page_icon="🌐", layout="centered")

st.title("🌐 Language Translation Tool")
st.caption("CodeAlpha AI Internship — Task 1")

# --- language options -------------------------------------------------------
try:
    LANGS = supported_languages()  # {'english': 'en', ...}
except Exception as exc:  # offline / blocked network
    st.error(f"Couldn't load the language list: {exc}")
    st.stop()

NAMES = sorted(LANGS.keys())
CODE_TO_NAME = {code: name for name, code in LANGS.items()}


def _index(name: str) -> int:
    return NAMES.index(name) if name in NAMES else 0


# --- session state ----------------------------------------------------------
st.session_state.setdefault("source", "english")
st.session_state.setdefault("target", "arabic")
st.session_state.setdefault("result", "")


def swap() -> None:
    st.session_state.source, st.session_state.target = (
        st.session_state.target,
        st.session_state.source,
    )


# --- controls ---------------------------------------------------------------
col_a, col_swap, col_b = st.columns([5, 1, 5])
with col_a:
    source_name = st.selectbox(
        "From", NAMES, index=_index(st.session_state.source), key="source"
    )
with col_swap:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    st.button("⇄", on_click=swap, use_container_width=True, help="Swap languages")
with col_b:
    target_name = st.selectbox(
        "To", NAMES, index=_index(st.session_state.target), key="target"
    )

auto_detect = st.checkbox("Auto-detect source language", value=False)

text = st.text_area("Text to translate", height=180, placeholder="Type or paste text here…")

# --- translate --------------------------------------------------------------
if st.button("Translate", type="primary", use_container_width=True):
    if not text.strip():
        st.warning("Enter some text first.")
    else:
        src = "auto" if auto_detect else LANGS[source_name]
        tgt = LANGS[target_name]
        with st.spinner("Translating…"):
            try:
                st.session_state.result = translate(text, src, tgt)
                if auto_detect:
                    guessed = detect_language(text)
                    st.info(f"Detected source: **{CODE_TO_NAME.get(guessed, guessed)}**")
            except Exception as exc:
                st.error(f"Translation failed: {exc}")
                st.session_state.result = ""

# --- output -----------------------------------------------------------------
result = st.session_state.result
if result:
    st.subheader("Translation")
    # st.code gives a native copy-to-clipboard button for free.
    st.code(result, language=None, wrap_lines=True)

    tts_col, dl_col = st.columns(2)

    with tts_col:
        if st.button("🔊 Read aloud", use_container_width=True):
            try:
                from gtts import gTTS
                buffer = io.BytesIO()
                gTTS(text=result, lang=LANGS[target_name]).write_to_fp(buffer)
                buffer.seek(0)
                st.audio(buffer.read(), format="audio/mpeg")
                

            except Exception as exc:
                st.warning(f"Text-to-speech unavailable for this language ({exc}).")

    with dl_col:
        st.download_button(
            "⬇️ Download .txt",
            data=result.encode("utf-8"),
            file_name="translation.txt",
            mime="text/plain",
            use_container_width=True,
        )

    st.metric("Characters", f"{len(text)} → {len(result)}")

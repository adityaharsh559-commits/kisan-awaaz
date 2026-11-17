import os
import tempfile
from io import BytesIO

import streamlit as st
import whisper
from gtts import gTTS
from deep_translator import GoogleTranslator

from knowledge import get_answer
from topics import find_topics
from db import init_db, log_request

HINT_HI = "किसान की फसल की समस्या: मेरे गेहूं के पत्ते पीले, कीड़े, खाद, सिंचाई, बीज।"

# One line per language. To add a language later, add one more line here.
LANGUAGES = {
    "हिन्दी (Hindi)":      "hi",
    "मराठी (Marathi)":     "mr",
    "தமிழ் (Tamil)":        "ta",
    "ਪੰਜਾਬੀ (Punjabi)":     "pa",
    "తెలుగు (Telugu)":      "te",
    "বাংলা (Bengali)":      "bn",
    "ગુજરાતી (Gujarati)":   "gu",
    "ಕನ್ನಡ (Kannada)":      "kn",
    "മലയാളം (Malayalam)":   "ml",
    "English":             "en",
}

st.set_page_config(page_title="Kisan Awaaz", page_icon="🌾")
init_db()


@st.cache_resource
def load_model():
    return whisper.load_model("medium")


def translate(text, source, target):
    """Returns the translated text, or None if translation failed."""
    if source == target:
        return text
    try:
        return GoogleTranslator(source=source, target=target).translate(text)
    except Exception:
        return None


st.title("🌾 किसान आवाज़")
st.caption("Inspired by Swami Sahajanand Saraswati")
st.info(
    "हम आपका नाम, फ़ोन नंबर या आवाज़ सेव नहीं करते। "
    "(We do not save your name, phone number, or voice. Your words are sent to Google's "
    "translation and speech services only to produce the answer.)"
)

choice = st.selectbox("अपनी भाषा चुनिए / Choose your language", list(LANGUAGES.keys()))
code = LANGUAGES[choice]

audio = st.audio_input("Mic button dabaiye, boliye, phir roak dijiye")

if audio:
    with st.spinner("Listening..."):
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(audio.getvalue())
            path = f.name
        try:
            result = load_model().transcribe(
                path,
                language=code,
                initial_prompt=HINT_HI if code == "hi" else None,
            )
        finally:
            os.remove(path)   # the voice file is deleted right away
        text = result["text"].strip()

    st.write("**You said:**", text)

    hindi_text = translate(text, code, "hi")
    if hindi_text is None:
        st.error("Translation failed. Please check the internet connection and try again.")
        st.stop()

    answer_hi = get_answer(hindi_text)
    crop, problems = find_topics(hindi_text)
    log_request(code, crop, problems, bool(problems))   # only anonymous facts are saved

    answer = translate(answer_hi, "hi", code)
    if answer is None:
        answer = answer_hi
        code_out = "hi"
        st.warning("Could not translate the answer, so it is shown in Hindi.")
    else:
        code_out = code

    st.success(answer)

    buf = BytesIO()
    gTTS(text=answer, lang=code_out).write_to_fp(buf)
    st.audio(buf.getvalue(), format="audio/mp3")
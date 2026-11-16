import os
import tempfile
from io import BytesIO

import streamlit as st
import whisper
from gtts import gTTS

from knowledge import get_answer
from topics import find_topics
from db import init_db, log_request

HINT_HI = "किसान की फसल की समस्या: मेरे गेहूं के पत्ते पीले, कीड़े, खाद, सिंचाई, बीज।"

st.set_page_config(page_title="Kisan Awaaz", page_icon="🌾")
init_db()


@st.cache_resource
def load_model():
    return whisper.load_model("medium")   # loads once, not on every click


st.title("🌾 किसान आवाज़")
st.caption("Inspired by Swami Sahajanand Saraswati")
st.info("हम आपका नाम, फ़ोन नंबर या आवाज़ सेव नहीं करते।")

audio = st.audio_input("बोलने के लिए माइक का बटन दबाइए, और बात ख़त्म होने पर रोक दीजिए")

if audio:
    with st.spinner("आपकी बात सुन रहा हूँ..."):
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(audio.getvalue())
            path = f.name
        try:
            result = load_model().transcribe(path, language="hi", initial_prompt=HINT_HI)
        finally:
            os.remove(path)   # the voice file is deleted right away
        text = result["text"].strip()

    st.write("**आपने कहा:**", text)

    answer = get_answer(text)
    crop, problems = find_topics(text)
    log_request("hi", crop, problems, bool(problems))

    st.success(answer)

    buf = BytesIO()
    gTTS(text=answer, lang="hi").write_to_fp(buf)
    st.audio(buf.getvalue(), format="audio/mp3")
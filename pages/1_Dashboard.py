import random
import sqlite3
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

DB_FILE = "requests.db"

st.set_page_config(page_title="Dashboard", page_icon="📊")
st.title("📊 Kisan Awaaz Dashboard")
st.caption("Anonymous usage data. No names, phone numbers, voices, or sentences are stored.")

use_demo = st.toggle("Show DEMO data (fake, for testing the charts)", value=False)


def load_real():
    try:
        with sqlite3.connect(DB_FILE) as con:
            return pd.read_sql_query("SELECT * FROM requests", con)
    except Exception:
        return pd.DataFrame(columns=["id", "created_at", "language", "crop", "topics", "answered"])


def make_demo(n=250):
    random.seed(1)
    crops = ["गेहूं", "चावल", "टमाटर", "चना", "unknown"]
    topics = ["yellow", "insects", "water", "fertilizer", "irrigation", ""]
    langs = ["hi", "hi", "hi", "mr", "ta", "pa", "en"]
    rows = []
    for i in range(n):
        topic = random.choice(topics)
        when = datetime.now() - timedelta(days=random.randint(0, 29), hours=random.randint(0, 23))
        rows.append((i, when.isoformat(timespec="seconds"), random.choice(langs),
                     random.choice(crops), topic, int(topic != "")))
    return pd.DataFrame(rows, columns=["id", "created_at", "language", "crop", "topics", "answered"])


df = make_demo() if use_demo else load_real()

if use_demo:
    st.warning("You are looking at FAKE demo data, not real farmer questions.")

if df.empty:
    st.info("No questions logged yet. Ask a few questions on the main page, or switch on demo data above.")
    st.stop()

df["created_at"] = pd.to_datetime(df["created_at"])
df["date"] = df["created_at"].dt.date

# ---------- Key numbers ----------
c1, c2, c3 = st.columns(3)
c1.metric("Total questions", len(df))
c2.metric("Answered", f"{df['answered'].mean() * 100:.0f}%")
c3.metric("Languages used", df["language"].nunique())

# ---------- Charts ----------
st.subheader("Questions per day")
st.line_chart(df.groupby("date").size())

st.subheader("Topics asked about")
topic_counts = df["topics"].str.split(",").explode()
topic_counts = topic_counts[topic_counts.fillna("") != ""].value_counts()
if len(topic_counts):
    st.bar_chart(topic_counts)

st.subheader("Crops")
st.bar_chart(df["crop"].value_counts())

st.subheader("Languages")
st.bar_chart(df["language"].value_counts())

# ---------- The most useful insight ----------
st.subheader("Questions the app could not understand")
missed = df[df["answered"] == 0]
st.write(f"{len(missed)} of {len(df)} questions ({len(missed) / len(df) * 100:.0f}%) had no matching topic.")
st.caption("A high number means the knowledge base needs more topics, crops, or spelling variants.")
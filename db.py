import sqlite3
from datetime import datetime

DB_FILE = "requests.db"


def init_db():
    with sqlite3.connect(DB_FILE) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT,
                language TEXT,
                crop TEXT,
                topics TEXT,
                answered INTEGER
            )
        """)


def log_request(language, crop, topics, answered):
    """Saves only anonymous facts: no name, no voice, no sentence."""
    with sqlite3.connect(DB_FILE) as con:
        con.execute(
            "INSERT INTO requests (created_at, language, crop, topics, answered) VALUES (?, ?, ?, ?, ?)",
            (datetime.now().isoformat(timespec="seconds"), language,
             crop or "unknown", ",".join(topics), int(answered)),
        )
# database.py
import sqlite3
import json
from datetime import datetime

DB_FILE = "chat_history.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            user_id TEXT PRIMARY KEY,
            messages TEXT,
            last_updated TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_chat(user_id: str, messages: list):
    conn = sqlite3.connect(DB_FILE)
    messages_json = json.dumps(messages)
    conn.execute("""
        INSERT OR REPLACE INTO chat_history (user_id, messages, last_updated)
        VALUES (?, ?, ?)
    """, (user_id, messages_json, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def load_chat(user_id: str) -> list:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.execute("SELECT messages FROM chat_history WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return json.loads(row[0])
    return []

init_db()  # Inicializar base de datos
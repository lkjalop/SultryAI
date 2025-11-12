import sqlite3
from pathlib import Path
from typing import Dict, Any, Optional
import json

DB_PATH = Path(__file__).parent.parent / 'data' / 'sultry.db'

def ensure_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS events (
        event_id TEXT PRIMARY KEY,
        timestamp TEXT,
        sensor_id TEXT,
        sensor_type TEXT,
        event_type TEXT,
        raw JSON
    )
    ''')
    conn.commit()
    conn.close()

def insert_event(event: Dict[str, Any]) -> None:
    ensure_db()
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.execute(
        'INSERT OR REPLACE INTO events (event_id,timestamp,sensor_id,sensor_type,event_type,raw) VALUES (?,?,?,?,?,?)',
        (event.get('event_id'), event.get('timestamp'), event.get('sensor_id'), event.get('sensor_type'), event.get('event_type'), json.dumps(event))
    )
    conn.commit()
    conn.close()

def get_event(event_id: str) -> Optional[Dict[str, Any]]:
    if not DB_PATH.exists():
        return None
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.execute('SELECT raw FROM events WHERE event_id = ?', (event_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return json.loads(row[0])

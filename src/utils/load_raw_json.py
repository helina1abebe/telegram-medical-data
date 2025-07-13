import json
import psycopg2
from pathlib import Path

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    dbname="telegram_db",
    user="postgres",
    password="yourpassword",
    port=5432
)
cur = conn.cursor()

raw_data_dir = Path("data/raw/telegram_messages/2025-07-12")
for json_file in raw_data_dir.glob("*.json"):
    with open(json_file, "r", encoding="utf-8") as f:
        messages = json.load(f)
        for msg in messages:
            cur.execute("""
                INSERT INTO raw.telegram_messages (message_id, message_json)
                VALUES (%s, %s::jsonb)
                ON CONFLICT DO NOTHING
            """, (msg['id'], json.dumps(msg)))
conn.commit()
cur.close()
conn.close()

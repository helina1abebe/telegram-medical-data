import json
import os
import csv
import psycopg2
from dotenv import load_dotenv

# Load DB credentials from .env
load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("PGDATABASE"),
    "user": os.getenv("PGUSER"),
    "password": os.getenv("PGPASSWORD"),
    "host": os.getenv("PGHOST"),
    "port": os.getenv("PGPORT")
}
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "../data/raw/telegram_messages/2025-07-09")


def connect_db():
    return psycopg2.connect(**DB_CONFIG)

def create_raw_schema_and_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE SCHEMA IF NOT EXISTS raw;

            CREATE TABLE IF NOT EXISTS raw.telegram_messages (
                id SERIAL PRIMARY KEY,
                channel_name TEXT,
                message_json JSONB
            );
        """)
        conn.commit()

def insert_json_messages(conn):
    with conn.cursor() as cur:
        for filename in os.listdir(DATA_DIR):
            if filename.endswith(".json"):
                channel = filename.replace(".json", "")
                with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
                    messages = json.load(f)
                    for msg in messages:
                        cur.execute("""
                            INSERT INTO raw.telegram_messages (channel_name, message_json)
                            VALUES (%s, %s);
                        """, (channel, json.dumps(msg)))
        conn.commit()

def main():
    conn = connect_db()
    create_raw_schema_and_table(conn)
    insert_json_messages(conn)
    conn.close()
    print("✅ Raw messages loaded into raw.telegram_messages")

if __name__ == "__main__":
    main()

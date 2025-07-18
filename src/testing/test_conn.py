import os
import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv

load_dotenv()

try:
    conn = psycopg2.connect(
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT")
    )
    cur = conn.cursor()
    cur.execute("SELECT 1;")  # Force query to validate connection
    result = cur.fetchone()
    print("✅ Connection test passed. Result:", result)

    conn.close()
except OperationalError as e:
    print("❌ Connection failed:")
    print(e)

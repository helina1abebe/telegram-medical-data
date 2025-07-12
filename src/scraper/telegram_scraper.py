from dotenv import load_dotenv
import os

load_dotenv() # loads the .env file from the project root

api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")

print(f"API ID: {api_id}")
print(f"API Hash: {api_hash}")

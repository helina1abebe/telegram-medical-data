from dotenv import load_dotenv
import os

# Load the .env file in the same folder as this script
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

DATABASE_URL = os.getenv("DATABASE_URL")
print("✅ DATABASE_URL loaded:", DATABASE_URL)

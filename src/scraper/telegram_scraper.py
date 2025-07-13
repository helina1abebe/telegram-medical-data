from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto
from dotenv import load_dotenv
import os, json
from datetime import datetime
from pathlib import Path

# Load secrets
load_dotenv()
api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")

# Channels to scrape
channels = ["lobelia4cosmetics", "tikvahpharma"]  # Add more usernames here

# Today's date for folder naming
date_str = datetime.today().strftime("%Y-%m-%d")

# Initialize client
with TelegramClient("anon", api_id, api_hash) as client:
    for channel in channels:
        print(f"\n📥 Scraping channel: {channel}")
        try:
            # Prepare message storage
            message_dir = Path(f"data/raw/telegram_messages/{date_str}")
            message_dir.mkdir(parents=True, exist_ok=True)
            message_path = message_dir / f"{channel}.json"

            # Prepare image storage
            image_dir = Path(f"data/raw/images/{channel}/{date_str}")
            image_dir.mkdir(parents=True, exist_ok=True)

            # Scrape messages
            messages = []
            for msg in client.iter_messages(channel, limit=100):
                messages.append(msg.to_dict())

                # If message has image, download it
                if msg.media and isinstance(msg.media, MessageMediaPhoto):
                    filename = image_dir / f"{msg.id}.jpg"
                    client.download_media(msg.media, file=filename)
                    print(f"📸 Downloaded image: {filename.name}")

            # Save messages as JSON
            with open(message_path, "w", encoding="utf-8") as f:
                json.dump(messages, f, ensure_ascii=False, indent=2)

            print(f"✅ Saved {len(messages)} messages to {message_path.name}")

        except Exception as e:
            print(f"❌ Error scraping {channel}: {e}")

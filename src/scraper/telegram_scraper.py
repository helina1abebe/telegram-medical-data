import os
import csv
import json
import time
import argparse
import logging
from datetime import datetime
from typing import List
from dotenv import load_dotenv
from telethon import TelegramClient

# Load environment variables
load_dotenv()
api_id = int(os.getenv("Tg_API_ID"))
api_hash = os.getenv("Tg_API_HASH")

# Today's date
today = datetime.today().strftime("%Y-%m-%d")

# Setup logger
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, f"scrape_{today}.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

async def scrape_channel(client: TelegramClient, channel: str, writer: csv.writer, csv_media_dir: str, json_media_dir: str, json_save_dir: str):
    try:
        entity = await client.get_entity(channel)
        channel_title = entity.title
        messages = []

        # Create media dir per channel
        os.makedirs(csv_media_dir, exist_ok=True)
        os.makedirs(json_media_dir, exist_ok=True)

        async for message in client.iter_messages(entity, limit=1000):
            media_path = None
            if message.media and hasattr(message.media, "photo"):
                filename = f"{channel.strip('@')}_{message.id}.jpg"
                media_path = os.path.join(csv_media_dir, filename)
                await client.download_media(message.media, media_path)

            message_dict = {
                "channel_title": channel_title,
                "channel_username": channel,
                "id": message.id,
                "message": message.message,
                "date": str(message.date),
                "media_path": media_path
            }

            # Write to CSV
            writer.writerow([
                channel_title,
                channel,
                message.id,
                message.message,
                message.date,
                media_path
            ])

            # Append for JSON
            messages.append(message_dict)

        # Save JSON
        json_path = os.path.join(json_save_dir, f"{channel.strip('@')}.json")
        with open(json_path, "w", encoding="utf-8") as jf:
            json.dump(messages, jf, ensure_ascii=False, indent=2)

        logging.info(f"✅ Finished scraping {channel} ({len(messages)} messages)")
        time.sleep(3)  # 🔐 Sleep to avoid Telegram ban

    except Exception as e:
        logging.error(f"❌ Error scraping {channel}: {e}")

async def obtain_channel_ads(client: TelegramClient, telegram_channels: List[str], base_path: str):
    await client.start()

    # Setup paths
    csv_dir = os.path.join(base_path, "raw", "csv", today)
    json_dir = os.path.join(base_path, "raw", "telegram_messages", today)
    media_base = os.path.join(base_path, "raw", "media", today)

    os.makedirs(csv_dir, exist_ok=True)
    os.makedirs(json_dir, exist_ok=True)

    csv_file_path = os.path.join(csv_dir, "telegram_data.csv")
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['channel_title', 'channel_username', 'id', 'message', 'date', 'media_path'])

        for channel in telegram_channels:
            print(f"📡 Scraping {channel}...")
            csv_media_dir = os.path.join(media_base, channel.strip('@'))
            json_media_dir = os.path.join(media_base, channel.strip('@'))
            await scrape_channel(client, channel, writer, csv_media_dir, json_media_dir, json_dir)
            print(f"✅ Done with {channel}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Telegram Scraper for Ethiopian Medical Channels")
    parser.add_argument("--path", type=str, default="data", help="Base data directory")
    args = parser.parse_args()

    client = TelegramClient("telegram_scraper_session", api_id, api_hash)
    print("🚀 Telegram client initialized")

    target_channels = ['@cheMed123', '@lobelia4cosmetics', '@tikvahpharma', '@Thequorachannel']

    with client:
        client.loop.run_until_complete(obtain_channel_ads(client, target_channels, args.path))

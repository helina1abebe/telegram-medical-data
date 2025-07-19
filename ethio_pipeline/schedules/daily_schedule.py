from dagster import op
import subprocess

@op
def scrape_telegram_data():
    subprocess.run(["python", "scripts/scrape_telegram.py"], check=True)

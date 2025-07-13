# telegram-medical-data

**From Raw Telegram Data to an Analytical API**  
This project builds a complete data pipeline that scrapes data from Ethiopian Telegram channels about medical businesses, transforms it into structured data using dbt, enriches it using YOLOv8 image detection, and exposes it via a FastAPI endpoint. Dagster is used for orchestration and scheduling.

---

## 🧩 Project Structure

telegram-medical-data/
│
├── .env # Environment variables (API keys, DB credentials)
├── .gitignore
├── requirements.txt # Python dependencies
├── Dockerfile
├── docker-compose.yml # Docker setup for local development
│
├── src/
│ ├── scraper/ # Telegram scraping logic using Telethon
│ │ └── telegram_scraper.py
│ └── utils/
│ └── logger.py
│
└── data/
└── raw/ # Raw Telegram messages and media


## ⚙️ Tech Stack

| Layer          | Tool / Library           |
|----------------|--------------------------|
| **Scraping**   | [Telethon](https://github.com/LonamiWebs/Telethon)        |
| **ETL Logic**  | Python, dbt              |
| **Orchestration** | Dagster               |
| **Enrichment** | YOLOv8 (for media/image analysis) |
| **Storage**    | PostgreSQL               |
| **API**        | FastAPI                  |
| **DevOps**     | Docker, docker-compose   |

---

## 🚀 Getting Started

### 1. Clone the repo

git clone https://github.com/helina1abebe/telegram-medical-data.git
cd telegram-medical-data
### 2. Set up your virtual environment

python -m venv .venv
.venv\Scripts\activate  # On Windows
# or
source .venv/bin/activate  # On Mac/Linux
### 3. Install dependencies
bash
Copy code
pip install -r requirements.txt
### 4. Create a .env file
dotenv
TELEGRAM_API_ID= ______________
TELEGRAM_API_HASH= ______________

POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_DB=telegram_db
### 5. Run the Telegram scraper
python src/scraper/telegram_scraper.py
📈 Data Pipeline Overview
Scrape messages and media from selected Telegram channels.

Store raw data in the /data/raw/ folder.

Transform the data into a star schema using dbt.

Enrich product/media data using YOLOv8 (e.g., detect packaging, products).

Serve data through a FastAPI endpoint for downstream apps.

📅 Roadmap
 Basic Telegram scraping

 Raw data storage

 dbt transformations to dimensional model

 Image enrichment with YOLOv8

 API serving with FastAPI

 Scheduled pipeline with Dagster

🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

🛡️ License
MIT

✨ Author
Helina Abebe Bekele
Built as part of the Kifiya AI Mastery Program
# data-discovery-llm
Leveraging LLM to do data discovery on any data set (for now we are just using TFT data).


# **TFT Match Data Pipeline**
*A scalable data ingestion pipeline for Teamfight Tactics (TFT) match history using Riot Games API.*

![Python](https://img.shields.io/badge/python-3.9%2B-brightgreen)
![PostgreSQL](https://img.shields.io/badge/database-PostgreSQL-orange)

---

## 📌 Overview
This project automates the retrieval, processing, and storage of **TFT match data** from the Riot Games API.  
It efficiently paginates through match history, extracts key game details, and loads structured data into a PostgreSQL database.

---

## 🚀 Features
✅ **Batch Data Collection** – Fetch match history using Riot's API with pagination.  
✅ **Time-Filtered Queries** – Retrieve matches from the last two months using epoch timestamps.  
✅ **Scalable Storage** – Store parsed match data in a relational database.  
✅ **Automated Migrations** – Manage schema changes using **Alembic**.  
✅ **CSV Export** – Save processed json file match data for further analysis.  
✅ **Efficient Rate-Limiting** – Optimize API calls while respecting Riot’s limits.  

---

## 🛠️ Tech Stack
| Category        | Technology |
|----------------|-----------|
| **Language**   | Python (3.9+) |
| **Database**   | PostgreSQL |
| **API**        | Riot Games API |
| **ORM**        | SQLAlchemy |
| **Migrations** | Alembic |
| **Testing**    | Pytest |
| **Data Export** | CSV |

---

## 📦 Installation

#### 1️⃣ Clone the Repository

#### 2️⃣ Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
#### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
#### 4️⃣ Configure Environment Variables
Create a .env file and add:

```ini


API_KEY=your-riot-api-key
DATABASE_URL=postgresql://user:password@localhost/tft_db
```
## 📊 Database Schema  

The pipeline extracts and stores data into five tables:  

| Table        | Description                                |
|-------------|--------------------------------------------|
| **matches**      | Stores match metadata (game time, version, queue, etc.). |
| **participants** | Contains player and performance data.      |
| **traits**       | Tracks player traits (synergies).      |
| **units**        | Records champions used in the match.   |
| **items**        | Logs items equipped by units.         |

## 🖥️ Usage
#### 1️⃣ Fetch & Store Matches
```bash


python main.py
```
#### 2️⃣ Run Migrations (Alembic)
```bash


alembic upgrade head
```
#### 3️⃣ Export Data to CSV
```bash


python export.py
```
#### 4️⃣ Run Tests (Pytest)
```bash


pytest --cov=src tests/
```
## 📈 Example API Call
Retrieve match history for PPG Rex from the past 2 months:

python


from src.riot_api import get_match_ids

puuid = "DqNKF8vPZ9JKsUhKOQ39ijH2p3w660wHowxqnBPnihBgeHyj4Ws7LS9xlHm2lY9claiP_ztgZcDjDQ"
matches = get_match_ids(puuid, startTime=TWO_MONTHS_AGO, count=100)
print(matches)

## 👥 Contributors
👤 Ethan Ho
👤 Francis Ho
👤 Carolette Saguil

📧 ethan.ho4181@gmail.com

## 🌟 Acknowledgments
Riot Games API for providing match data.

SQLAlchemy & Alembic for seamless database management.

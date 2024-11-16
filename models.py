# models.py
import sqlite3
from datetime import datetime, timedelta
import random


# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Create tables for IntradayData and NewsData
    cursor.execute('''CREATE TABLE IF NOT EXISTS IntradayData (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT,
                        price REAL,
                        volume INTEGER,
                        symbol TEXT
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS NewsData (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT,
                        headline TEXT,
                        sentiment_score REAL,
                        relevance REAL,
                        source TEXT
                    )''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS GoldPrices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            price REAL,
            volume INTEGER
        )
    ''')

    # Insert dummy data
    cursor.execute("INSERT INTO IntradayData (timestamp, price, volume, symbol) VALUES (?, ?, ?, ?)",
                   (datetime.now().isoformat(), 100.5, 1500, 'AAPL'))

    news_data = [
        (datetime.now().isoformat(), "Apple releases new product", 0.8, 0.9, "Reuters"),
        ((datetime.now() - timedelta(days=1)).isoformat(), "Google faces antitrust lawsuit", -0.6, 0.85, "Bloomberg"),
        ((datetime.now() - timedelta(days=2)).isoformat(), "Tesla announces new self-driving update", 0.7, 0.75,
         "TechCrunch"),
        ((datetime.now() - timedelta(days=3)).isoformat(), "Amazon to expand drone delivery", 0.9, 0.8, "CNBC"),
        ((datetime.now() - timedelta(days=4)).isoformat(), "Microsoft to acquire gaming company", 0.6, 0.7,
         "Wall Street Journal"),
        ((datetime.now() - timedelta(days=5)).isoformat(), "Netflix stock drops after earnings report", -0.5, 0.65,
         "Yahoo Finance"),
        ((datetime.now() - timedelta(days=6)).isoformat(), "Meta faces privacy concerns", -0.4, 0.8, "The Guardian"),
        ((datetime.now() - timedelta(days=7)).isoformat(), "NVIDIA unveils new AI chip", 0.85, 0.9, "Reuters"),
        ((datetime.now() - timedelta(days=8)).isoformat(), "Alibaba reports record sales on Singles' Day", 0.75, 0.85,
         "South China Morning Post"),
        ((datetime.now() - timedelta(days=9)).isoformat(), "Samsung releases new Galaxy series", 0.6, 0.7, "BBC"),
    ]

    for news in news_data:
        cursor.execute(
            "INSERT INTO NewsData (timestamp, headline, sentiment_score, relevance, source) VALUES (?, ?, ?, ?, ?)",
            news
        )

    base_price = 1800
    days = 365
    data = []
    for i in range(days):
        # Generate date starting from today going back
        date = (datetime.now() - timedelta(days=i)).isoformat()
        # Generate a random price with some fluctuation
        price = round(base_price + random.uniform(-50, 50), 2)
        # Generate a random volume
        volume = random.randint(1000, 5000)  # in ounces
        data.append((date, price, volume))

    # Insert generated data into the GoldPrices table
    cursor.executemany('''
        INSERT INTO GoldPrices (date, price, volume) VALUES (?, ?, ?)
    ''', data)

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS DataTags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag TEXT,
            dataset TEXT
        )
    ''')

    data = [
        ("gold", "GoldPrices"),
        ("commodities", "GoldPrices"),
        ("stocks", "IntradayData"),
        ("equities", "IntradayData"),
        ("apple", "IntradayData"),
        ("news", "NewsData")
    ]

    # Insert data into MyTable
    cursor.executemany('''
        INSERT INTO DataTags (tag, dataset) VALUES (?, ?)
    ''', data)

    conn.commit()
    conn.close()


# Connect to database
def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

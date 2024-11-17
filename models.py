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

    stock_symbols = ["TSLA", "GOOGL", "AMZN", "MSFT"]

    # Generate and insert dummy data
    num_entries_per_stock = 10  # Number of entries per stock symbol
    base_time = datetime.now()

    for symbol in stock_symbols:
        for i in range(num_entries_per_stock):
            # Generate a timestamp for each entry, spaced 5 minutes apart
            timestamp = (base_time - timedelta(minutes=i * 5)).isoformat()
            # Generate a random price between 100 and 1500
            price = round(random.uniform(100, 1500), 2)
            # Generate a random volume between 1000 and 5000
            volume = random.randint(1000, 5000)

            # Insert the generated data into the IntradayData table
            cursor.execute('''
                INSERT INTO IntradayData (timestamp, price, volume, symbol)
                VALUES (?, ?, ?, ?)
            ''', (timestamp, price, volume, symbol))

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
            dataset TEXT,
            metadata TEXT
        )
    ''')

    data = [
        ("gold", "GoldPrices", "[gold commodities inflation]"),
        ("stocks", "IntradayData", "[equities shares intraday]"),
        ("equities", "IntradayData", "[equities shares intraday]"),
        ("apple", "IntradayData", "[apple, equities shares intraday]"),
        ("news", "NewsData", "[news sentiment twitter x politics]")
    ]

    # Insert data into MyTable
    cursor.executemany('''
        INSERT INTO DataTags (tag, dataset, metadata) VALUES (?, ?, ?)
    ''', data)

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ClientTransactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            transaction_date TEXT,
            transaction_amount REAL,
            transaction_type TEXT
        )
    ''')

    # Create StockHoldings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS StockHoldings (
            holding_id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            stock_symbol TEXT,
            quantity INTEGER,
            purchase_price REAL,
            purchase_date TEXT
        )
    ''')

    # Create RiskAssessments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS RiskAssessments (
            assessment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            risk_score INTEGER,
            liquidity_ratio REAL,
            leverage_ratio REAL,
            credit_rating TEXT
        )
    ''')

    # Commit the table creation
    conn.commit()

    # Step 3: Populate the Tables with Dummy Data

    # Generate some sample client IDs
    client_ids = [101, 102, 103, 104, 105]

    # Populate ClientTransactions table with dummy data
    transaction_types = ["deposit", "withdrawal", "purchase", "sale"]
    for _ in range(50):  # 50 transactions
        client_id = random.choice(client_ids)
        transaction_date = (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat()
        transaction_amount = round(random.uniform(1000, 50000), 2)
        transaction_type = random.choice(transaction_types)
        cursor.execute('''
            INSERT INTO ClientTransactions (client_id, transaction_date, transaction_amount, transaction_type)
            VALUES (?, ?, ?, ?)
        ''', (client_id, transaction_date, transaction_amount, transaction_type))

    # Populate StockHoldings table with dummy data
    stock_symbols = ["AAPL", "TSLA", "GOOGL", "AMZN", "MSFT"]
    for _ in range(30):  # 30 stock holdings
        client_id = random.choice(client_ids)
        stock_symbol = random.choice(stock_symbols)
        quantity = random.randint(10, 200)
        purchase_price = round(random.uniform(100, 1500), 2)
        purchase_date = (datetime.now() - timedelta(days=random.randint(1, 730))).isoformat()  # Up to 2 years ago
        cursor.execute('''
            INSERT INTO StockHoldings (client_id, stock_symbol, quantity, purchase_price, purchase_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (client_id, stock_symbol, quantity, purchase_price, purchase_date))

    # Populate RiskAssessments table with dummy data
    credit_ratings = ["AAA", "AA", "A", "BBB", "BB", "B", "CCC"]
    for client_id in client_ids:
        risk_score = random.randint(1, 100)
        liquidity_ratio = round(random.uniform(0.5, 2.0), 2)
        leverage_ratio = round(random.uniform(0.1, 1.5), 2)
        credit_rating = random.choice(credit_ratings)
        cursor.execute('''
            INSERT INTO RiskAssessments (client_id, risk_score, liquidity_ratio, leverage_ratio, credit_rating)
            VALUES (?, ?, ?, ?, ?)
        ''', (client_id, risk_score, liquidity_ratio, leverage_ratio, credit_rating))

    conn.commit()
    conn.close()


# Connect to database
def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

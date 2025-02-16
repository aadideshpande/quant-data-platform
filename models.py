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
                        source TEXT,
                        symbol TEXT
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
        (datetime.now().isoformat(), "Apple releases new product", 0.8, 0.9, "Reuters", "AAPL"),
        ((datetime.now() - timedelta(days=1)).isoformat(), "Google faces antitrust lawsuit", -0.6, 0.85, "Bloomberg", "GOOG"),
        ((datetime.now() - timedelta(days=2)).isoformat(), "Tesla announces new self-driving update", 0.7, 0.75,
         "TechCrunch", "TSLA"),
        ((datetime.now() - timedelta(days=3)).isoformat(), "Amazon to expand drone delivery", 0.9, 0.8, "CNBC", "AMZN"),
        ((datetime.now() - timedelta(days=4)).isoformat(), "Microsoft to acquire gaming company", 0.6, 0.7,
         "Wall Street Journal", "MSFT"),
        ((datetime.now() - timedelta(days=5)).isoformat(), "Netflix stock drops after earnings report", -0.5, 0.65,
         "Yahoo Finance", "NFLX"),
        ((datetime.now() - timedelta(days=6)).isoformat(), "Meta faces privacy concerns", -0.4, 0.8, "The Guardian", "META"),
        ((datetime.now() - timedelta(days=7)).isoformat(), "AMD unveils new AI chip", 0.85, 0.9, "Reuters", "AMD"),
        ((datetime.now() - timedelta(days=8)).isoformat(), "Alibaba reports record sales on Singles' Day", 0.75, 0.85,
         "South China Morning Post", "BABA"),
        ((datetime.now() - timedelta(days=9)).isoformat(), "Samsung releases new Galaxy series", 0.6, 0.7, "BBC", "SSNLF"),
    ]

    for news in news_data:
        cursor.execute(
            "INSERT INTO NewsData (timestamp, headline, sentiment_score, relevance, source, symbol) "
            "VALUES (?, ?, ?, ?, ?, ?)",
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
            metadata TEXT,
            source TEXT,
            origin_date TEXT,
            description TEXT
            
        )
    ''')

    # Create EconomicIndicators table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS EconomicIndicators (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            country TEXT NOT NULL,
            indicator_name TEXT NOT NULL,
            date TEXT NOT NULL,
            value REAL NOT NULL,
            unit TEXT NOT NULL
        )
    ''')

    # Sample economic indicator data
    current_date = datetime.now().isoformat()
    economic_data = [
        # GDP Growth Rate Data
        ('USA', 'GDP Growth Rate', current_date, 2.5, '%'),
        ('EUR', 'GDP Growth Rate', current_date, 1.8, '%'),
        ('JPN', 'GDP Growth Rate', current_date, 1.2, '%'),
        ('GBR', 'GDP Growth Rate', current_date, 1.9, '%'),
        ('CHN', 'GDP Growth Rate', current_date, 5.2, '%'),
        
        # Inflation Rate Data
        ('USA', 'Inflation Rate', current_date, 3.1, '%'),
        ('EUR', 'Inflation Rate', current_date, 2.8, '%'),
        ('JPN', 'Inflation Rate', current_date, 2.0, '%'),
        ('GBR', 'Inflation Rate', current_date, 4.0, '%'),
        ('CHN', 'Inflation Rate', current_date, 2.3, '%'),
        
        # Unemployment Rate Data
        ('USA', 'Unemployment Rate', current_date, 3.7, '%'),
        ('EUR', 'Unemployment Rate', current_date, 6.5, '%'),
        ('JPN', 'Unemployment Rate', current_date, 2.5, '%'),
        ('GBR', 'Unemployment Rate', current_date, 4.2, '%'),
        ('CHN', 'Unemployment Rate', current_date, 5.0, '%'),
        
        # Interest Rate Data
        ('USA', 'Interest Rate', current_date, 5.50, '%'),
        ('EUR', 'Interest Rate', current_date, 4.50, '%'),
        ('JPN', 'Interest Rate', current_date, -0.10, '%'),
        ('GBR', 'Interest Rate', current_date, 5.25, '%'),
        ('CHN', 'Interest Rate', current_date, 3.45, '%'),
        
        # Trade Balance Data (in billions USD)
        ('USA', 'Trade Balance', current_date, -62.2, 'B USD'),
        ('EUR', 'Trade Balance', current_date, 23.5, 'B USD'),
        ('JPN', 'Trade Balance', current_date, -8.2, 'B USD'),
        ('GBR', 'Trade Balance', current_date, -15.4, 'B USD'),
        ('CHN', 'Trade Balance', current_date, 70.2, 'B USD')
    ]

    cursor.executemany('''
        INSERT INTO EconomicIndicators (country, indicator_name, date, value, unit)
        VALUES (?, ?, ?, ?, ?)
    ''', economic_data)

    data = [
        ("gold", "GoldPrices", "[gold commodities inflation]",
         "yahoo", f'{datetime.now().date()}', "daily prices of gold"),
        ("stocks", "IntradayData", "[equities shares intraday]",
         "bloomberg", f'{datetime.now().date()}', "intraday data for stocks"),
        ("equities", "IntradayData", "[equities shares intraday]",
         "yahoo", f'{datetime.now().date()}', "intraday data for equities/stocks"),
        ("apple", "IntradayData", "[apple, equities shares intraday]",
         "iex", f'{datetime.now().date()}', "intraday data for tech stocks"),
        ("news", "NewsData", "[news sentiment twitter x politics]",
         "quandl", f'{datetime.now().date()}', "news headlines data for sentiment analysis"),
    ]

    # Insert data into MyTable
    cursor.executemany('''
        INSERT INTO DataTags (tag, dataset, metadata, source, origin_date, description) VALUES (?, ?, ?, ?, ?, ?)
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

    # Generate dummy news data for NVIDIA with sentiment and relevance
    symbol = "NVDA"
    news_data = [
        # Positive news (increases stock price)
        (datetime.now().replace(hour=10, minute=30, second=50, microsecond=0)).isoformat(),
        "NVIDIA announces breakthrough in AI technology",
        0.8, 0.9, "Reuters", symbol,
        (datetime.now().replace(hour=11, minute=30, second=40, microsecond=0)).isoformat(),
        "NVIDIA partners with major tech firm to expand GPU production", 0.7, 0.85, "Bloomberg", symbol,

        # Negative news (decreases stock price)
        (datetime.now().replace(hour=13, minute=30, second=0, microsecond=0)).isoformat(),
        "NVIDIA faces regulatory scrutiny over data privacy",
        -0.6, 0.8, "TechCrunch", symbol,
        (datetime.now().replace(hour=15, minute=30, second=0, microsecond=0)).isoformat(),
        "NVIDIA recalls certain GPU models due to overheating issues", -0.7, 0.75, "CNBC", symbol
    ]

    # Insert the dummy news data into the NewsData table
    cursor.executemany('''
        INSERT INTO NewsData (timestamp, headline, sentiment_score, relevance, source, symbol)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', [(news_data[i], news_data[i + 1], news_data[i + 2], news_data[i + 3], news_data[i + 4], news_data[i + 5]) for i in
          range(0, len(news_data), 6)])

    # Generate dummy intraday data for the past 5 days for NVIDIA
    num_intraday_entries_per_day = 20  # Number of 5-minute intervals per day (for simplicity)
    symbol = "NVDA"
    intraday_data = []

    # Define a baseline price and simulate changes due to news sentiment
    base_price = 280

    # Timestamps for the positive and negative news events
    news_events = {
        "positive": [
            (datetime.now().replace(hour=10, minute=30, second=50, microsecond=0)),
            (datetime.now().replace(hour=11, minute=30, second=40, microsecond=0)),
        ],
        "negative": [
            (datetime.now().replace(hour=13, minute=30, second=0, microsecond=0)),
            (datetime.now().replace(hour=15, minute=30, second=0, microsecond=0)),
        ]
    }

    start_time = datetime.now().replace(hour=9, minute=30, second=0, microsecond=0)
    end_time = start_time.replace(hour=16, minute=0)
    current_time = start_time
    while current_time <= end_time:
        # Adjust price based on proximity to news events
        if any(abs((current_time - event).total_seconds()) < 3600 for event in news_events["positive"]):
            price = round(base_price + random.uniform(3, 6), 2)  # Positive impact
        elif any(abs((current_time - event).total_seconds()) < 3600 for event in news_events["negative"]):
            price = round(base_price - random.uniform(3, 6), 2)  # Negative impact
        else:
            price = round(base_price + random.uniform(-2, 2), 2)  # Normal fluctuation

        # Generate random volume between 1000 and 5000
        volume = random.randint(1000, 5000)

        # Append to intraday_data list
        intraday_data.append((current_time.isoformat(), price, volume, symbol))

        # Move to the next minute
        current_time += timedelta(minutes=5)

    # Insert the dummy intraday data into the IntradayData table
    cursor.executemany('''
        INSERT INTO IntradayData (timestamp, price, volume, symbol)
        VALUES (?, ?, ?, ?)
    ''', intraday_data)

    conn.commit()
    conn.close()


# Connect to database
def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

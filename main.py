import uvicorn
from fastapi import FastAPI, Depends, Query
import models
from datetime import datetime, timedelta
from DataCatalog import DataCatalog
from DataLake import DataLake
from fastapi.security import OAuth2PasswordBearer
from security import router as security_router, has_permission
from helper_classes import Body
import yfinance as yf
from typing import Optional
import os

db_path = 'data.db'
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"Database '{db_path}' existed and has been deleted.")
else:
    print(f"Database '{db_path}' does not exist.")

app = FastAPI()
models.init_db()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app.include_router(security_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/proprietary-info")
async def get_proprietary_info(user: dict = Depends(has_permission(["prop_view"]))):
    data_lake = DataLake()
    return data_lake.get_data('StockHoldings')


@app.get('/api/intraday/recent/{symbol}')
def get_recent_intraday_data(symbol):
    data_catalog = DataCatalog()
    data_lake = DataLake()
    return data_catalog.get_intraday_data(data_lake, symbol)


@app.get('/api/news/recent', deprecated=True)
def get_recent_news():
    days = 5
    recent_timestamp = (datetime.now() - timedelta(days=days)).isoformat()
    conn = models.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM NewsData WHERE timestamp >= ?", (recent_timestamp,))
    data = cursor.fetchall()
    conn.close()
    return {"data": [dict(row) for row in data]}


@app.get('/api/news/sentiment_score_filter')
def get_news_by_sentiment(sentiment_score_filter: float, symbol: str):
    data_catalog = DataCatalog()
    data_lake = DataLake()
    return data_catalog.get_sentiment_scored_news(data_lake, sentiment_score_filter, symbol)

@app.get("/api/get-stock-data")
async def get_stock_data(
    symbol: str = Query(..., description="Stock symbol (e.g., AAPL, GOOGL)"),
    start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(..., description="End date in YYYY-MM-DD format"),
    interval: str = Query(
        "1d",
        description="Data frequency: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo"
    )
):
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        ticker = yf.Ticker(symbol)
        hist = ticker.history(
            start=start,
            end=end,
            interval=interval
        )
        
        # Store data in database
        conn = models.get_db_connection()
        cursor = conn.cursor()
        
        for index, row in hist.iterrows():
            cursor.execute('''
                INSERT INTO StockData (symbol, timestamp, open, high, low, close, volume, interval)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                symbol,
                index.isoformat(),
                row['Open'],
                row['High'],
                row['Low'],
                row['Close'],
                row['Volume'],
                interval
            ))
        
        conn.commit()
        conn.close()
        
        # Convert the data for response
        data = hist.reset_index().to_dict(orient='records')
        
        return {
            "symbol": symbol,
            "start_date": start_date,
            "end_date": end_date,
            "interval": interval,
            "data": data
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "message": "Failed to fetch or store data"
        }

@app.get('/api/intraday/aggregate', deprecated=True)
def aggregate_intraday_data():
    interval = 15
    symbol = 'APPL'
    conn = models.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM IntradayData WHERE symbol = ?", (symbol,))
    data = cursor.fetchall()

    # Aggregate by interval (dummy logic, just returning fetched data for simplicity)
    # Actual logic would involve grouping by timestamp intervals and averaging
    aggregated_data = [dict(row) for row in data]
    conn.close()
    return {"data": aggregated_data}


@app.get('/api/db/list')
def get_data_list():
    conn = models.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()
    return {"data": tables}


@app.get('/api/datasets/{tag_name}')
def get_dataset_based_on_tag_name(tag_name):
    data_catalog = DataCatalog()
    data_lake = DataLake()
    return data_catalog.get_dataset_tag(tag_name, data_lake)


@app.get('/api/data/filtered_data', deprecated=True)
def get_filtered_date():
    data_lake = DataLake()
    return data_lake.get_data_filtered('NewsData', datetime.now() - timedelta(days=1)).isoformat()


@app.get('/api/advanced_search/')
def get_advanced_search(search_term):
    data_catalog = DataCatalog()
    data_lake = DataLake()
    return data_catalog.get_advanced_search_datasets(search_term, data_lake)


@app.post('/api/advanced_sentence_search/')
def get_advanced_search(body: Body):
    data_catalog = DataCatalog()
    data_lake = DataLake()
    return data_catalog.get_advanced_sentence_search(body, data_lake)
    # return {"error_message": "An unexpected error occurred"}


@app.get('/api/metadata')
def get_database_metadata():
    conn = models.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM DataTags;")
    tables = cursor.fetchall()
    conn.close()
    return {"data": tables}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

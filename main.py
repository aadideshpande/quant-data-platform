import uvicorn
from fastapi import FastAPI
import models
from datetime import datetime, timedelta

from DataCatalog import DataCatalog, DataTag
from DataLake import DataLake

# from flask import jsonify, request

app = FastAPI()
models.init_db()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get('/api/intraday/recent')
def get_recent_intraday_data():
    days = 1
    recent_timestamp = (datetime.now() - timedelta(days=days)).isoformat()
    conn = models.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM IntradayData WHERE timestamp >= ?", (recent_timestamp,))
    data = cursor.fetchall()
    conn.close()
    return {"data": [dict(row) for row in data]}


@app.get('/api/news/recent')
def get_recent_news():
    days = 5
    recent_timestamp = (datetime.now() - timedelta(days=days)).isoformat()
    conn = models.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM NewsData WHERE timestamp >= ?", (recent_timestamp,))
    data = cursor.fetchall()
    conn.close()
    return {"data": [dict(row) for row in data]}


@app.get('/api/news/filter')
def get_news_by_sentiment():
    threshold = 0.5
    conn = models.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM NewsData WHERE sentiment_score >= ?", (threshold,))
    data = cursor.fetchall()
    conn.close()
    return {"data": [dict(row) for row in data]}


@app.get('/api/intraday/aggregate')
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


@app.get('/api/data/filtered_data')
def get_filtered_date():
    data_lake = DataLake()
    return data_lake.get_data_filtered('NewsData', datetime.now() - timedelta(days=1)).isoformat()


@app.get('/api/advanced_search/')
def get_advanced_search(search_term):
    data_catalog = DataCatalog()
    data_lake = DataLake()
    return data_catalog.get_advanced_search_datasets(search_term, data_lake)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

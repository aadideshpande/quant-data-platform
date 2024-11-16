# app.py
from flask import Flask, jsonify, request
from fastapi import FastAPI
from datetime import datetime, timedelta
import models

app = FastAPI()

# Initialize the database
# models.init_db()


@app.get('/api/intro')
def get_intro():
    return jsonify("This is the intro")


# Route to get recent intraday data
@app.get('/api/intraday/recent')
def get_recent_intraday_data():
    days = int(request.args.get('days', 1))
    recent_timestamp = (datetime.now() - timedelta(days=days)).isoformat()
    conn = models.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM IntradayData WHERE timestamp >= ?", (recent_timestamp,))
    data = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in data])


# Route to aggregate intraday data by interval
@app.get('/api/intraday/aggregate')
def aggregate_intraday_data():
    interval = int(request.args.get('interval', 15))  # in minutes
    symbol = request.args.get('symbol', 'AAPL')
    conn = models.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM IntradayData WHERE symbol = ?", (symbol,))
    data = cursor.fetchall()

    # Aggregate by interval (dummy logic, just returning fetched data for simplicity)
    # Actual logic would involve grouping by timestamp intervals and averaging
    aggregated_data = [dict(row) for row in data]
    conn.close()
    return jsonify(aggregated_data)


# Route to get news data filtered by sentiment
@app.get('/api/news/filter')
def get_news_by_sentiment():
    threshold = float(request.args.get('threshold', 0.5))
    conn = models.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM NewsData WHERE sentiment_score >= ?", (threshold,))
    data = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in data])


# Route to get recent news
@app.get('/api/news/recent')
def get_recent_news():
    days = int(request.args.get('days', 1))
    recent_timestamp = (datetime.now() - timedelta(days=days)).isoformat()
    conn = models.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM NewsData WHERE timestamp >= ?", (recent_timestamp,))
    data = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in data])




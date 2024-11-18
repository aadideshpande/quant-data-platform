import requests
import pandas as pd
from datetime import datetime, timedelta

# Constants
DATA_LAKE_URL = "http://localhost:8000"
EVENT_WINDOW = 5  # Event window in minutes, e.g., -60 to +60 minutes around the news event
STOCK_SYMBOL = "NVDA"  # Example stock symbol


# Helper function to retrieve intraday data
def get_intraday_data(symbol: str):
    url = f"{DATA_LAKE_URL}/api/intraday/recent/{symbol}"
    response = requests.get(url)
    response.raise_for_status()
    return pd.DataFrame(response.json())


# Helper function to retrieve news data
def get_news_data(symbol: str):
    url = f"{DATA_LAKE_URL}/api/news/sentiment_score_filter"
    params = {"symbol": symbol, "sentiment_score_filter": -1}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return pd.DataFrame(response.json())


# Step 1: Retrieve Intraday Data
start_date = (datetime.now() - timedelta(days=7)).isoformat()  # Get data for the last week
end_date = datetime.now().isoformat()

intraday_data = get_intraday_data(STOCK_SYMBOL)
intraday_data['timestamp'] = pd.to_datetime(intraday_data['timestamp'])
intraday_data.set_index('timestamp', inplace=True)

# Step 2: Retrieve News Data
news_data = get_news_data(STOCK_SYMBOL)
news_data['timestamp'] = pd.to_datetime(news_data['timestamp'])
# news_data.set_index('timestamp', inplace=True)

# Step 3: Tag Events (e.g., categorize news by sentiment)
news_data = news_data[news_data['sentiment_score'].notnull()]  # Filter news with sentiment score
positive_news = news_data[news_data['sentiment_score'] > 0.5]
negative_news = news_data[news_data['sentiment_score'] < -0.5]


# Step 4: Perform Event Study Analysis

def analyze_event_impact(news_event, intraday_data):
    event_time = news_event['timestamp']
    event_window_start = event_time - timedelta(minutes=EVENT_WINDOW)
    event_window_end = event_time + timedelta(minutes=EVENT_WINDOW)

    start_timestamp = pd.Timestamp(event_window_start)
    end_timestamp = pd.Timestamp(event_window_end)

    # Filter using conditional selection
    window_data = intraday_data[(intraday_data.index >= start_timestamp) & (intraday_data.index <= end_timestamp)]
    if window_data.empty:
        return None  # No data in the event window

    # Calculate returns and abnormal returns
    window_data['return'] = window_data['price'].pct_change()
    baseline_return = window_data['return'].mean()  # Example baseline return calculation
    window_data['abnormal_return'] = window_data['return'] - baseline_return

    return window_data[['return', 'abnormal_return']]


# Analyze impact for each news event and store results
event_study_results = []

for _, news_event in positive_news.iterrows():
    event_result = analyze_event_impact(news_event, intraday_data)
    if event_result is not None:
        event_study_results.append({
            "news_id": news_event['id'],
            "timestamp": news_event['timestamp'],
            "sentiment_score": news_event['sentiment_score'],
            "impact_data": event_result
        })

for _, news_event in negative_news.iterrows():
    event_result = analyze_event_impact(news_event, intraday_data)
    if event_result is not None:
        event_study_results.append({
            "news_id": news_event['id'],
            "timestamp": news_event['timestamp'],
            "sentiment_score": news_event['sentiment_score'],
            "impact_data": event_result
        })

# Step 5: Summarize and Output Results
# Display event study results for each positive and negative event
for result in event_study_results:
    print(f"News ID: {result['news_id']}")
    print(f"Timestamp: {result['timestamp']}")
    print(f"Sentiment Score: {result['sentiment_score']}")
    print("Impact Data:")
    print(result["impact_data"])
    print("\n" + "-" * 40 + "\n")

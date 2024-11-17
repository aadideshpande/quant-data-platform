from datetime import datetime


class BaseDataModel:
    def __init__(self, id, timestamp, symbol=None):
        self.id = id
        self.timestamp = timestamp if isinstance(timestamp, datetime) else datetime.now()
        self.symbol = symbol

    def __repr__(self):
        return f"BaseDataModel(Timestamp: {self.timestamp}, Symbol: {self.symbol})"

    def is_recent(self, days=7):
        delta = datetime.now() - self.timestamp
        return delta.days <= days

    def is_above_threshold(self, value, threshold):
        return value > threshold


class IntradayDataModel(BaseDataModel):
    def __init__(self, id, timestamp, price, volume, symbol):
        super().__init__(id, timestamp, symbol)
        self.price = price
        self.volume = volume

    def __repr__(self):
        return f"IntradayDataModel({self.symbol}, {self.timestamp}, Price: {self.price}, Volume: {self.volume})"

    def aggregate_by_interval(self, interval, data):
        pass

    @classmethod
    def from_row(cls, row):
        # Initialize an instance from a database row (tuple)
        return cls(id=row[0], timestamp=row[1], price=row[2], volume=row[3], symbol=row[4])


class NewsDataModel(BaseDataModel):
    def __init__(self, timestamp, headline, sentiment_score, relevance, source):
        super().__init__(timestamp)
        self.headline = headline
        self.sentiment_score = sentiment_score
        self.relevance = relevance
        self.source = source

    def __repr__(self):
        return f"NewsDataModel(Timestamp: {self.timestamp}, Headline: {self.headline[:30]}, Sentiment: {self.sentiment_score})"

    def filter_by_sentiment(self, threshold):
        return self.is_above_threshold(self.sentiment_score, threshold)

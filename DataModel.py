from datetime import datetime


class BaseDataModel:
    def __init__(self, id, timestamp, symbol=None):
        self.id = id
        if timestamp is not None:
            timestamp_dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
            self.timestamp = timestamp_dt if isinstance(timestamp_dt, datetime) else datetime.now()
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
        super().__init__(id, symbol=symbol, timestamp=None)
        try:
            timestamp_dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f")
        except ValueError:
            timestamp_dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
        self.timestamp = timestamp_dt if isinstance(timestamp_dt, datetime) else datetime.now()
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
    def __init__(self, id, timestamp, headline, sentiment_score, relevance, source, symbol):
        super().__init__(id, timestamp=None)
        try:
            timestamp_dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f")
        except ValueError:
            timestamp_dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
        self.timestamp = timestamp_dt if isinstance(timestamp_dt, datetime) else datetime.now()
        self.headline = headline
        self.sentiment_score = sentiment_score
        self.relevance = relevance
        self.source = source
        self.symbol = symbol

    @classmethod
    def from_row(cls, row):
        # Initialize an instance from a database row (tuple)
        return cls(id=row[0], timestamp=row[1], headline=row[2],
                   sentiment_score=row[3], relevance=row[4], source=row[5], symbol=row[6])

    def __repr__(self):
        return f"NewsDataModel(Timestamp: {self.timestamp}, Headline: {self.headline[:30]}, Sentiment: {self.sentiment_score})"

    def filter_by_sentiment(self, threshold):
        return self.is_above_threshold(self.sentiment_score, threshold)


class EconomicIndicatorDataModel(BaseDataModel):
    def __init__(self, country, indicator_name, date, value, unit):
        super().__init__(date)  # Pass date to BaseDataModel as timestamp
        self.country = country
        self.indicator_name = indicator_name
        self.value = value
        self.unit = unit

    @classmethod
    def from_row(cls, row):
        return cls(
            country=row[1],
            indicator_name=row[2],
            date=row[3],
            value=row[4],
            unit=row[5]
        )

    def __repr__(self):
        return f"EconomicIndicator({self.country}, {self.indicator_name}, Value: {self.value} {self.unit})"

    def is_above_threshold(self, threshold):
        return super().is_above_threshold(self.value, threshold)
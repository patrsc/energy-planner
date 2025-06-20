"""Module for obtaining electricity prices. Outputs values in cent/kWh."""
import os
import statistics
from datetime import datetime, timedelta
from .util import get_file, read_json, clone_repo, pull_repo


class PriceAdapter:
    """Defines how prices are read and processed."""
    def __init__(self, storage_dir: str, url: str):
        self.prices_dir = os.path.join(storage_dir, "prices")
        self.data_dir = os.path.join(self.prices_dir, "data")
        self.repo_url = url

    def update(self):
        """Update price repository."""
        if not os.path.isdir(self.prices_dir):
            clone_repo(self.repo_url, self.prices_dir)
        else:
            pull_repo(self.prices_dir)

    def transform(self, price: float) -> float:
        """Transform raw price value."""
        return price

    def get_hourly_prices(self, start_time: datetime) -> list[float] | None:
        """Get all hourly prices of day."""
        file = self._get_file(start_time)
        values = self._read_prices_from_file(file)
        if len(values) == 0:
            return None
        return [value['price'] for value in values]

    def get_price(self, time: datetime) -> float:
        """Return electricity price at given time."""
        file = self._get_file(time)
        data = self._read_prices_from_file(file)
        return self._get_price_at_time(data, time)

    def get_prices_in_range(self, start_time: datetime, end_time: datetime) -> list[float]:
        """Get prices in given time range."""
        t = start_time
        t_start = start_time.timestamp()
        t_end = end_time.timestamp()
        prices = []
        while t.timestamp() <= t_end:
            file = self._get_file(t)
            data = self._read_prices_from_file(file)
            for item in data:
                if t_start <= item['start_timestamp'] < t_end:
                    prices.append(item['price'])
            t = t + timedelta(days=1)
        return prices

    def _read_prices_from_file(self, file: str) -> list[dict]:
        if not os.path.isfile(file):
            return []
        content = read_json(file)
        data = content["data"]
        values = []
        for value in data:
            price_eur_per_mwh = float(value['marketprice'])
            price_ct_per_kwh = price_eur_per_mwh / 10
            price = self.transform(price_ct_per_kwh)
            values.append({
                'start_timestamp': value['start_timestamp'] / 1000,
                'end_timestamp':value['end_timestamp'] / 1000,
                'price': price,
            })
        return values

    def _get_price_at_time(self, data, time: datetime) -> float:
        """Returns price at given timestamp."""
        timestamp = time.timestamp()
        for entry in data:
            start = entry['start_timestamp']
            end = entry['end_timestamp']
            if start <= timestamp < end:
                return entry['price']
        raise ValueError("Timestamp not found in any price interval.")

    def get_statistical_price(self, time: datetime, operation: str, days: int) -> float:
        """Return statistical electricity price (mean, max, min) over given past days."""
        end_time = time
        start_time = datetime.fromtimestamp(time.timestamp() - days * 24 * 3600, tz=time.tzinfo)
        prices = self.get_prices_in_range(start_time, end_time)
        if operation == "mean":
            value = statistics.mean(prices)
        elif operation == "min":
            value = min(prices)
        elif operation == "max":
            value = max(prices)
        else:
            raise ValueError("unknown operation")
        return value

    def _get_file(self, time: datetime):
        return get_file(self.data_dir, time)

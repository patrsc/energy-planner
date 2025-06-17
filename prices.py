import os
from datetime import datetime
from util import get_file, read_json, clone_repo, pull_repo


class PriceAdapter:
    def __init__(self, storage_dir: str, url: str):
        self.prices_dir = os.path.join(storage_dir, "prices")
        self.data_dir = os.path.join(self.prices_dir, "data")
        self.repo_url = url

    def update(self):
        if not os.path.isdir(self.prices_dir):
            clone_repo(self.repo_url, self.prices_dir)
        else:
            pull_repo(self.prices_dir)

    def get_hourly_prices(self, start_time: datetime) -> list[float] | None:
        file = self._get_file(start_time)
        if not os.path.isfile(file):
            return None
        content = read_json(file)
        data = content["data"]
        prices = []
        for value in data:
            price_eur_per_mwh = float(value['marketprice'])
            price_ct_per_kwh = price_eur_per_mwh / 10
            prices.append(self.transform(price_ct_per_kwh))
        return prices

    def transform(self, price: float) -> float:
        """Account for fixed offset and tax."""
        return (price + 1.5) * 1.2

    def _get_file(self, start_time: datetime):
        return get_file(self.data_dir, start_time)

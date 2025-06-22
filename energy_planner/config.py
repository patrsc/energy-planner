"""Your custom configuration."""
from .core import Device
from .devices.boiler import Boiler
from .prices import PriceAdapter
import os


# Your custom settings that you can overwrite
class Settings:
    devices: list[Device] = [
        Boiler('boiler', pretty_name='Boiler'),
        Boiler('boiler2', pretty_name='Boiler 2'),
        Boiler('boiler3', pretty_name='Boiler 3'),
    ]
    storage_dir = os.environ.get("STORAGE_DIR", "data")
    timezone = os.environ.get("TZ", "Europe/Vienna")
    price_repo_url = "https://github.com/patrsc/EPEX-AT-History.git"
    fallback_deadline_seconds = 2 * 3600


# Your customized PriceAdapter.
class CustomPriceAdapter(PriceAdapter):
    """Custom price adapter."""
    # Here you could override some methods if needed.

    def transform(self, price: float) -> float:
        """Account for fixed offset and tax."""
        return (price + 1.5) * 1.2

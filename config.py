"""Your custom configuration."""
from devices.boiler import Boiler
from prices import PriceAdapter
import os


# Your custom settings that you can overwrite
class Settings:
    devices = [
        Boiler('boiler'),
    ]
    storage_dir = os.environ.get("STORAGE_DIR", "data")
    timezone = "Europe/Vienna"
    price_repo_url = "https://github.com/patrsc/EPEX-AT-History.git"
    fallback_deadline_seconds = 2 * 3600


# Your customized PriceAdapter.
class CustomPriceAdapter(PriceAdapter):
    """Custom price adapter."""
    # Here you could override some methods if needed.
    pass

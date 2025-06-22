"""Energy Planner web interface and API."""
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import FastAPI
from fastapi.responses import FileResponse

from energy_planner.config import Settings, CustomPriceAdapter
from energy_planner.core import Planner

app = FastAPI(title="Energy Planner")


@app.get("/")
def read_root():
    """Read main index.html file."""
    return FileResponse("web/index.html", media_type="text/html")


@app.get("/api/devices")
def get_devices():
    """Get list of devices."""
    return [{
        'name': d.name,
        'pretty_name': d.pretty_name,
        'type': d.__class__.__name__,
    } for d in Settings.devices]


@app.get("/api/plans/{device}/{date}")
def get_device_plan(device: str, date: str):
    """Get the plan file of a device for the given date or None if plan does not exist."""
    planner = Planner(
        price_adapter=CustomPriceAdapter(Settings.storage_dir, Settings.price_repo_url),
        devices=Settings.devices,
        storage_dir=Settings.storage_dir,
        timezone=Settings.timezone,
        deadline_seconds=Settings.fallback_deadline_seconds,
    )
    try:
        data = planner.read_plan(device, get_day_start_time(date))
    except FileNotFoundError:
        data = None
    return data


@app.get("/api/prices/{date}")
def get_prices(date: str) -> list[dict] | None:
    """Get hourly prices for the given day as list or None."""
    price_adapter = CustomPriceAdapter(Settings.storage_dir, Settings.price_repo_url)
    day_start = get_day_start_time(date)
    prices = price_adapter.get_hourly_prices(day_start)
    if prices is None:
        return None
    return [{"time": iso_time(day_start, i), "price": p} for i, p in enumerate(prices)]


def iso_time(start: datetime, hours: int):
    """Get ISO timestamp using start time and offset in hours."""
    return datetime.fromtimestamp(start.timestamp() + hours * 3600, tz=ZoneInfo(Settings.timezone))


def get_day_start_time(date: str) -> datetime:
    """Get 0:00:00 of given date in format YYYY-MM-YY."""
    year, month, day = [int(item) for item in date.split("-")]
    time = datetime(year, month, day, 0, 0, 0, tzinfo=ZoneInfo(Settings.timezone))
    return time

"""Sensor helper functions."""
import sys
from .config import Settings, CustomPriceAdapter
from .core import Planner
from .util import get_current_time


def main():
    """Print sensor value and exit."""
    try:
        target = sys.argv[1]
        time = get_current_time(Settings.timezone)
        price_adapter = CustomPriceAdapter(Settings.storage_dir, Settings.price_repo_url)
        planner = Planner(
            price_adapter=price_adapter,
            devices=Settings.devices,
            storage_dir=Settings.storage_dir,
            timezone=Settings.timezone,
            deadline_seconds=Settings.fallback_deadline_seconds,
        )
        if target == "price":
            if len(sys.argv) == 2:
                value = price_adapter.get_price(time)
            else:
                operation = sys.argv[2]
                days = int(sys.argv[3])
                value = price_adapter.get_statistical_price(time, operation, days)
        elif target == "plan":
            device_name = sys.argv[2]
            value = planner.get_device_plan(device_name, time)
        elif target == "info":
            device_name = sys.argv[2]
            value = planner.get_device_info(device_name, time)
        else:
            raise ValueError(f"unknown argument: {target}")
        print(value)
    except Exception as e:
        print(f"error: {str(e)}")
        sys.exit(1)

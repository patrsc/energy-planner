"""Sensor helper functions."""
import sys
import os
from datetime import datetime
from zoneinfo import ZoneInfo

from .config import Settings, CustomPriceAdapter
from .util import read_json


def main():
    """Print sensor value and exit."""
    try:
        target = sys.argv[1]
        dt = datetime.now(tz=ZoneInfo(Settings.timezone))
        if target == "price":
            adapter = CustomPriceAdapter(Settings.storage_dir, Settings.price_repo_url)
            if len(sys.argv) == 2:
                value = adapter.get_price(dt)
            else:
                operation = sys.argv[2]
                days = int(sys.argv[3])
                value = adapter.get_statistical_price(dt, operation, days)
        elif target == "plan":
            device_name = sys.argv[2]
            value = get_device_plan(dt, device_name)
        elif target == "info":
            device_name = sys.argv[2]
            value = get_device_info(dt, device_name)
        else:
            raise ValueError(f"unknown argument: {target}")
        print(value)
    except Exception as e:
        print(f"error: {str(e)}")
        sys.exit(1)


def get_plan_dir(device_name):
    """Get dir of plan for device."""
    return os.path.join(Settings.storage_dir, "plans", device_name)


def get_device_plan(dt, device_name):
    """Return current plan state ("on" or "off") for device."""
    d = get_plan_dir(device_name)
    file = os.path.join(d, get_file(dt))
    data = read_json(file)
    default_state = "off"
    events = data['events']
    state = default_state
    t = dt.timestamp()
    for event in events:
        t_event = datetime.fromisoformat(event['time']).timestamp()
        if t_event > t:
            break
        state = event['state']
    return state


def get_device_info(dt, device_name):
    """Return current plan info ("optimal" or "fallback") for device."""
    d = get_plan_dir(device_name)
    file = os.path.join(d, get_file(dt))
    data = read_json(file)
    return data["info"]


def get_file(dt):
    """Get file of date."""
    return dt.strftime("%Y/%m/%d.json")

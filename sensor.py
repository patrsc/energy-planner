"""Standalone script to parse price data and device plans to create sensor values from them.

Usage:
python sensor.py price  # returns current price in cent/kWh
python sensor.py price mean DAYS  # returns mean price over the last DAYS days
python sensor.py price max DAYS   # returns maximum price over last DAYS days
python sensor.py price min DAYS   # returns minimum price over last DAYS days
python sensor.py plan DEVICENAME  # returns device plan state "on" or "off"
python sensor.py info DEVICENAME  # returns device plan info value "optimal" or "fallback"

If any value is not available, the string "error: {message}" is returned with exit code set to 1.
This makes the sensor "unavailable" in Home Assistant.
"""
import sys
import os
import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import statistics

STORAGE_DIR = "data"
TIMEZONE = "Europe/Vienna"


def main():
    """Print sensor value and exit."""
    try:
        target = sys.argv[1]
        dt = datetime.now(tz=ZoneInfo(TIMEZONE))
        if target == "price":
            if len(sys.argv) == 2:
                value = get_current_price(dt)
            else:
                operation = sys.argv[2]
                days = int(sys.argv[3])
                value = get_statistical_price(dt, operation, days)
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


def get_price_dir():
    """Get dir of prices."""
    return os.path.join(STORAGE_DIR, "prices", "data")


def get_plan_dir(device_name):
    """Get dir of plan for device."""
    return os.path.join(STORAGE_DIR, "plans", device_name)


def get_current_price(dt):
    """Return current electricity price."""
    d = get_price_dir()
    file = os.path.join(d, get_file(dt))
    return get_price_at_timestamp(read_json_file(file)['data'], dt.timestamp())


def get_price_at_timestamp(data, timestamp):
    """Returns price at given timestamp."""
    # TODO: This is duplicated code as in PriceAdapter
    # Maybe store adapted prices on price update in prices-hourly/YYYY/MM/DD.json in list format.
    for entry in data:

        start = entry['start_timestamp']
        end = entry['end_timestamp']
        if start <= timestamp * 1000 < end:
            price_eur_per_mwh = float(entry['marketprice'])
            price_ct_per_kwh = price_eur_per_mwh / 10
            return (price_ct_per_kwh + 1.5) * 1.2
    raise ValueError("Timestamp not found in any price interval.")


def read_json_file(file):
    """Read json file."""
    with open(file, 'r', encoding='utf8') as f:
        return json.load(f)


def get_statistical_price(dt, operation, days):
    """Return statistical electricity price (mean, max, min) over given past days."""
    data = collect_data(dt, days)
    hours = days * 24
    timestamp = dt.timestamp()
    prices = []
    for hour in range(hours):
        t = timestamp + (hour - hours + 1) * 3600
        prices.append(get_price_at_timestamp(data, t))
    if operation == "mean":
        value = statistics.mean(prices)
    elif operation == "min":
        value = min(prices)
    elif operation == "max":
        value = max(prices)
    else:
        raise ValueError("unknown operation")
    return value


def collect_data(dt, days):
    """Collect all data of previous days."""
    d = get_price_dir()
    all_data = []
    for i in range(days + 1):
        index = i - days
        file = os.path.join(d, get_file(dt + timedelta(days=index)))
        data = read_json_file(file)['data']
        all_data.extend(data)
    return all_data


def get_device_plan(dt, device_name):
    """Return current plan state ("on" or "off") for device."""
    d = get_plan_dir(device_name)
    file = os.path.join(d, get_file(dt))
    data = read_json_file(file)
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
    data = read_json_file(file)
    return data["info"]


def get_file(dt):
    """Get file of date."""
    return dt.strftime("%Y/%m/%d.json")


if __name__ == "__main__":
    main()

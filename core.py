from abc import abstractmethod
from datetime import datetime
from typing import Literal
from dataclasses import dataclass, asdict
import os

from util import get_file, date_str, write_json, get_next_day_start
from prices import PriceAdapter

@dataclass
class Event:
    time: datetime
    state: Literal["off", "on"]


@dataclass
class Plan:
    events: list[Event]


class Device:
    def __init__(self, name: str, **kwargs):
        self.name = name

    @abstractmethod
    def plan(self, start_time: datetime, prices: list[float]) -> Plan:
        """Execute planning."""
        pass


class Planner:
    def __init__(
        self,
        price_adapter = PriceAdapter,
        devices: list[Device] | None = None,
        storage_dir: str = "data",
        timezone: str = "Europe/Vienna",
    ):
        self.price_adapter = price_adapter
        if devices is None:
            devices = []
        self.devices = devices
        self.plans_dir = os.path.join(storage_dir, "plans")
        self.timezone = timezone

    def plan(self, start_time=None):
        """Execute planning for all devices."""
        if start_time is None:
            start_time = get_next_day_start(self.timezone)
        self.price_adapter.update()
        hourly_prices = self.price_adapter.get_hourly_prices(start_time)
        if hourly_prices is None:
            print(f"Prices for day {date_str(start_time)} are not yet available.")
            return
        for device in self.devices:
            if not self.exists_plan(device.name, start_time):
                plan = device.plan(start_time, hourly_prices)
                self.save_plan(device.name, start_time, plan)
                print(f"Planning for {device.name} done for day {date_str(start_time)}")
        print("Finished")

    def exists_plan(self, device_name: str, start_time: datetime) -> bool:
        return os.path.isfile(self.get_plan_file(device_name, start_time))

    def save_plan(self, device_name: str, start_time: datetime, plan: Plan):
        file = self.get_plan_file(device_name, start_time)
        plan_json = asdict(plan)
        for i, item in enumerate(plan_json['events']):
            plan_json['events'][i]['time'] = item['time'].isoformat()
        path = os.path.dirname(file)
        if not os.path.isdir(path):
            os.makedirs(path, exist_ok=True)
        write_json(file, plan_json)

    def get_plan_file(self, device_name: str, start_time: datetime) -> str:
        return get_file(os.path.join(self.plans_dir, device_name), start_time)

from abc import abstractmethod
from datetime import datetime, timedelta
from typing import Literal
from dataclasses import dataclass, asdict
import os
import logging

from util import get_file, date_str, write_json, get_next_day_start, get_current_time
from prices import PriceAdapter

logger = logging.getLogger(__name__)

@dataclass
class Event:
    time: datetime
    state: Literal["off", "on"]


@dataclass
class Plan:
    info: str
    events: list[Event]


class Device:
    def __init__(self, name: str, **kwargs):
        self.name = name

    @abstractmethod
    def plan(self, start_time: datetime, prices: list[float] | None) -> Plan:
        """Execute planning.
        
        If prices is None a fallback plan should be made.
        """
        pass


class Planner:
    def __init__(
        self,
        price_adapter = PriceAdapter,
        devices: list[Device] | None = None,
        storage_dir: str = "data",
        timezone: str = "Europe/Vienna",
        deadline_seconds: int = 3600,
    ):
        self.price_adapter = price_adapter
        if devices is None:
            devices = []
        self.devices = devices
        self.plans_dir = os.path.join(storage_dir, "plans")
        self.timezone = timezone
        self.deadline_seconds = deadline_seconds

    def plan(self, start_time=None):
        """Execute planning for all devices."""
        if start_time is None:
            start_time = get_next_day_start(self.timezone)
        logger.info(f"Run planning for {date_str(start_time)}.")
        logger.info("Updating prices.")
        try:
            self.price_adapter.update()
        except Exception as e:
            logger.error(str(e))
        try:
            hourly_prices = self.price_adapter.get_hourly_prices(start_time)
        except Exception as e:
            logger.error(str(e))
            hourly_prices = None
        if hourly_prices is None:
            logger.info(f"Prices for day {date_str(start_time)} are not yet available.")
            if self.has_deadline_passed(start_time):
                logger.warning("Deadline has passed. Will continue with fallback planning.")
            else:
                logger.info("Nothing to do.")
                return
        for device in self.devices:
            if not self.exists_plan(device.name, start_time):
                logger.info(f"Planning for device {device.name}")
                plan = device.plan(start_time, hourly_prices)
                self.save_plan(device.name, start_time, plan)
                logger.info(f"Planning for {device.name} done for day {date_str(start_time)}")
        logger.info("Finished planing.")

    def has_deadline_passed(self, start_time: datetime) -> bool:
        now = get_current_time(self.timezone)
        return now >= start_time - timedelta(seconds=self.deadline_seconds)

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

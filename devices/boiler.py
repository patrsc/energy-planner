from datetime import datetime, timedelta
from core import Device, Plan, Event


class Boiler(Device):
    def plan(self, start_time: datetime, prices: list[float]) -> Plan:
        """Execute planning."""
        # Turn on boiler for consecutively 3 hours
        # First hour has higher weight because boiler is more likely heating in the beginning
        weights = [1.0, 0.7, 0.4]
        turn_on_hours = len(weights)
        n_hours = len(prices)

        # Iterate over sliding window
        best_cost = float('inf')
        best_start_hour = 0
        for i_start, start_hour in enumerate(range(n_hours - turn_on_hours + 1)):
            window_prices = prices[i_start:(i_start + turn_on_hours)]
            cost = sum(w * p for w, p in zip(weights, window_prices))
            if cost < best_cost:
                best_cost = cost
                best_start_hour = start_hour
        best_end_hour = best_start_hour + turn_on_hours
        events = [
            Event(time=start_time + timedelta(hours=best_start_hour), state="on"),
            Event(time=start_time + timedelta(hours=best_end_hour), state="off"),
        ]
        plan = Plan(events=events)
        return plan

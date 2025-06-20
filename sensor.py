"""Parse price data and device plans to create sensor values from them.

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
from energy_planner.sensor import main

if __name__ == "__main__":
    main()

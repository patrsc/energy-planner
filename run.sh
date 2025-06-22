#!/bin/bash

# Start web interface in background
setsid poetry run fastapi run api.py --port 8000 >/dev/null 2>&1 < /dev/null &
sleep 5
nginx

# Run main scheduler for planner
poetry run python run_scheduler.py

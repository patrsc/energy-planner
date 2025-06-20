#!/bin/bash
export STORAGE_DIR=/config/data/energy_planner
export TZ=Europe/Vienna
python sensor.py "$@"

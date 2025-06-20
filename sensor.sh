#!/bin/bash
export STORAGE_DIR=/config/data/energy_planner
export TZ=Europe/Vienna
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$SCRIPT_DIR"
python sensor.py "$@"

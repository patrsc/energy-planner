"""Utility functions."""
import os
import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import subprocess


def get_next_day_start(timezone: str):
    """Get 00:00:00 of next day in given timezone."""
    now = datetime.now(tz=ZoneInfo(timezone))
    day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    return day_start + timedelta(days=1)


def date_str(dt: datetime) -> str:
    """Get day in format YYYY-MM-DD."""
    return dt.strftime("%Y-%m-%d")


def get_file(dir: str, start_time: datetime) -> str:
    year, month, day = date_str(start_time).split("-")
    return os.path.join(dir, year, month, f"{day}.json")


def read_json(file: str):
    with open(file, 'r', encoding='utf8') as f:
        return json.load(f)


def write_json(file: str, data):
    with open(file, 'w', encoding='utf8') as f:
        json.dump(data, f)


def clone_repo(repo_url: str, repo_dir: str):
    if os.path.exists(repo_dir):
        raise FileExistsError(f"The target directory '{repo_dir}' already exists.")
    try:
        subprocess.run(["git", "clone", repo_url, repo_dir], check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to clone the repository: {e}")


def pull_repo(repo_dir: str):
    if not os.path.isdir(repo_dir):
        raise FileNotFoundError(f"The directory '{repo_dir}' does not exist or is not a directory.")
    try:
        subprocess.run(["git", "-C", repo_dir, "pull"], check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to pull the repository: {e}")

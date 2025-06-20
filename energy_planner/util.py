"""Utility functions."""
import os
import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import subprocess


def get_current_time(timezone: str) -> datetime:
    """Get current time in given timezone."""
    return datetime.now(tz=ZoneInfo(timezone))


def get_current_day_start(timezone: str) -> datetime:
    """Get 00:00:00 of current day in given timezone."""
    now = get_current_time(timezone)
    day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    return day_start


def get_next_day_start(timezone: str) -> datetime:
    """Get 00:00:00 of next day in given timezone."""
    return get_current_day_start(timezone) + timedelta(days=1)


def date_str(dt: datetime) -> str:
    """Get day in format YYYY-MM-DD."""
    return dt.strftime("%Y-%m-%d")


def get_file(directory: str, time: datetime) -> str:
    """Get file in a YYYY/MM/DD.json directory tree."""
    year, month, day = date_str(time).split("-")
    return os.path.join(directory, year, month, f"{day}.json")


def read_json(file: str):
    """Read data from JSON file."""
    with open(file, 'r', encoding='utf8') as f:
        return json.load(f)


def write_json(file: str, data):
    """Write data to JSON file."""
    with open(file, 'w', encoding='utf8') as f:
        json.dump(data, f, separators=(",", ":"))


def clone_repo(repo_url: str, repo_dir: str):
    """Clone Git repository."""
    if os.path.exists(repo_dir):
        raise FileExistsError(f"The target directory '{repo_dir}' already exists.")
    try:
        run("git", "clone", repo_url, repo_dir)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to clone the repository: {e}") from e


def pull_repo(repo_dir: str):
    """Pull Git repository."""
    if not os.path.isdir(repo_dir):
        raise FileNotFoundError(f"The directory '{repo_dir}' does not exist or is not a directory.")
    try:
        run("git", "-C", repo_dir, "pull")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to pull the repository: {e}") from e


def run(*args):
    """Run a process."""
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

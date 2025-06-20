"""Run planning at the start of every hour."""
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from energy_planner.cli import main
from energy_planner.util import get_current_day_start
from energy_planner.config import Settings


if __name__ == "__main__":
    scheduler = BlockingScheduler()

    # Run at the start of every hour
    scheduler.add_job(main, CronTrigger(minute=0))

    # Run once at startup
    main(start_time=get_current_day_start(Settings.timezone))  # today
    main()  # tomorrow
    scheduler.start()

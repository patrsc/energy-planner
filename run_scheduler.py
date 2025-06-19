"""Run planning at the start of every hour."""
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from energy_planner.cli import main


if __name__ == "__main__":
    scheduler = BlockingScheduler()

    # Run at the start of every hour
    scheduler.add_job(main, CronTrigger(minute=0))

    # Run once at startup
    main()
    scheduler.start()

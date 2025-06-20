from .core import Planner
from .config import Settings, CustomPriceAdapter
from .log_config import setup_logging
import logging


def main(start_time=None):
    try:
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info("Started planning.")
        planner = Planner(
            price_adapter=CustomPriceAdapter(Settings.storage_dir, Settings.price_repo_url),
            devices=Settings.devices,
            storage_dir=Settings.storage_dir,
            timezone=Settings.timezone,
            deadline_seconds=Settings.fallback_deadline_seconds,
        )
        planner.plan(start_time=start_time)
    except Exception as e:
        logger.exception(e)
        exit(1)

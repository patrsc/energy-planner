import logging
from datetime import datetime


class ISOFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        self.local_tz = datetime.now().astimezone().tzinfo
        super().__init__(*args, **kwargs)

    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, tz=self.local_tz)
        return dt.isoformat()


def setup_logging(level=logging.DEBUG):
    log_format = "{asctime} | {name:20} | {levelname:8} | {message}"
    formatter = ISOFormatter(fmt=log_format, style='{')

    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    if not root_logger.handlers:
        root_logger.addHandler(handler)

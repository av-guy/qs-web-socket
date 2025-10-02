import logging
import sys

LOG_FORMAT = "%(levelprefix)s %(asctime)s | %(name)s | %(message)s"


class LevelFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        record.levelprefix = f"{record.levelname:>8} |"
        return super().format(record)


def configure_logging(level=logging.DEBUG) -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(LevelFormatter(LOG_FORMAT))

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers = [handler]

import asyncio
import logging
from logging import LogRecord
from config import Config


def set_logger(config: Config):
    logging_config = getattr(config, "data", {}).get("logging", {})

    formatter_str = logging_config.get("formatter", "%(asctime)s %(levelname)s - %(message)s")
    log_level_str = logging_config.get("log_level", "info").upper()

    formatter = logging.Formatter(formatter_str)

    old_factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs) -> LogRecord:
        record = old_factory(*args, **kwargs)
        try:
            ttt = asyncio.current_task()
            record.coproc = ttt.get_name()
        except:  # noqa: E722
            record.coproc = "unknown"
        return record

    logging.setLogRecordFactory(record_factory)

    numeric_level = getattr(logging, log_level_str, logging.INFO)
    if not isinstance(numeric_level, int):
        numeric_level = logging.INFO

    # odstraníme existující handlery, aby se nepřekrývaly
    logger = logging.getLogger()
    while logger.handlers:
        logger.handlers.pop()

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.setLevel(numeric_level)
    logger.debug("Logger initialized")

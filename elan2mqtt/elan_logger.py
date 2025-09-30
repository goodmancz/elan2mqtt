import asyncio
import logging
from logging import LogRecord

from config import Config


def set_logger(config: Config):
    # bezpečný přístup k logging sekci
    logging_config = config.data.get("logging", {}) if hasattr(config, "data") else {}

    formatter = logging_config.get("formatter", "%(asctime)s %(levelname)s - %(message)s")
    log_level = logging_config.get("log_level", "info").upper()

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

    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        numeric_level = logging.INFO

    logging.basicConfig(level=numeric_level, format=formatter)
    logging.debug("Logger initialized")

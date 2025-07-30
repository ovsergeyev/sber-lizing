import logging
import logging.config
import os

from settings import settings


def setup_logging():
    os.makedirs(settings.log.log_dir_path, exist_ok=True)

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "level": settings.log.log_level_console,
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": "logs/app.log",
                "formatter": "standard",
                "level": settings.log.log_level_file,
                "encoding": "utf-8"
            },
        },
        "loggers": {
            "app": {
                "handlers": ["console", "file"],
                "level": settings.log.log_level_file,
                # "propagate": False,
            },
        },
    }

    logging.config.dictConfig(logging_config)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
from logging.config import dictConfig

import os


project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)
log_directory = os.path.join(project_root, "logs")

if not os.path.exists(log_directory):
    os.makedirs(log_directory)


logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "main_format": {
            "format": "{asctime} - {levelname} - {module} - {filename} - {funcName} - {lineno} - {message}",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "main_format",
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "main_format",
            "filename": f"{log_directory}/logging.log",
        },
        "file_debug": {
            "class": "logging.FileHandler",
            "formatter": "main_format",
            "filename": f"{log_directory}/logging_debug.log",
        },
    },
    "loggers": {
        "main": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": False,
        },
        "debug": {
            "handlers": ["file_debug", "console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}


def init_logger():
    dictConfig(logging_config)

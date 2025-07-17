import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
import colorlog

def get_logger(name: str) -> logging.Logger:
    """Creates a colorized logger for console and file with daily rotation"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Avoid duplicate handlers
    if not logger.handlers:
        # Colored console handler
        console_handler = colorlog.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        console_formatter = colorlog.ColoredFormatter(
            "%(log_color)s[%(levelname)s] %(asctime)s - %(name)s: %(message)s",
            datefmt="%H:%M:%S",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red'
            }
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # File handler (logs/app.log, rotates daily, keeps last 7)
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        file_handler = TimedRotatingFileHandler(
            filename=log_dir / "app.log",
            when="midnight",
            interval=1,
            backupCount=7,
            encoding="utf-8"
        )
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter(
            "[%(levelname)s] %(asctime)s - %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger

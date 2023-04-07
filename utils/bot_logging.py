import logging
import os

PATH_LOGS = os.path.join(os.getcwd(), "config", "logs.log")

log_formatter = logging.Formatter("%(levelname)s|%(asctime)s|%(filename)s:%(lineno)d|%(message)s")
file_handler = logging.FileHandler(PATH_LOGS, "w", "utf-8")
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
console_handler.setLevel(logging.CRITICAL)

logging.basicConfig(
    format="%(levelname)s|%(asctime)s|%(filename)s:%(lineno)d|%(message)s ",
    handlers=[file_handler, console_handler]
)
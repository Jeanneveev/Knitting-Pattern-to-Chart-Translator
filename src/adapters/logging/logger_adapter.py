import json
import logging
import logging.config
from src.ports.logger.logger_port import LoggerPort

class LoggerAdapter(LoggerPort):
    def setup_logging(self):
        config_path = "src/adapters/logging/logging_config.json"
        with open(config_path) as f:
            logger_config = json.load(f)
        logging.config.dictConfig(logger_config)

    def __init__(self, logger_name:str):
        self.logger = logging.getLogger(logger_name)
        self.setup_logging()

    def debug(self, message:str):
        self.logger.debug(message)

    def info(self, message:str):
        self.logger.info(message)

    def warning(self, message:str):
        self.logger.warning(message)

    def error(self, message:str, **kwargs):
        self.logger.error(message, **kwargs, exc_info=True)

    def critical(self, message:str):
        self.logger.critical(message)

    def exception(self, message:str):
        self.logger.exception(message)

def get_logger(name:str) -> LoggerAdapter:
    return LoggerAdapter(name)
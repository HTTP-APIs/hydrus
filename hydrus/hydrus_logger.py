import logging
import logging.config
import structlog
import os

class HydrusLogger:
    def __init__(self):
        logging.basicConfig(level = os.environ.get('LOGLEVEL', 'DEBUG'))
        logging.config.fileConfig('LogConfig')
        structlog.wrap_logger(logging.getLogger())
        structlog.configure(logger_factory=structlog.stdlib.LoggerFactory())
        self.logger = structlog.get_logger()

    def get_logger(self):
        return self.logger

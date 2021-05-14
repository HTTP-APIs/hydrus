import logging
import logging.config
import structlog


class HydrusLogger:
    def __init__(self):
        logging.config.fileConfig('LogConfig')
        structlog.wrap_logger(logging.getLogger())
        structlog.configure(logger_factory=structlog.stdlib.LoggerFactory())
        self.logger = structlog.get_logger()

    def get_logger(self):
        return self.logger

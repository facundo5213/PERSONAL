import logging
import contextvars
from uuid import uuid4

request_id_ctx_var = contextvars.ContextVar('request_id', default=None)


class Logging:
    def __init__(self):
        self.request_id = None
        logging.basicConfig(
            format="%(asctime)s [%(levelname)s] %(message)s",
            level=logging.INFO
        )
        self.logger = logging.getLogger(__name__)

    def get_request_id(self):
        self.request_id = request_id_ctx_var.get()
        if self.request_id is None:
            self.request_id = str(uuid4())
            request_id_ctx_var.set(self.request_id)

    def info(self, message: str):
        self.get_request_id()
        self.logger.info(f"{self.request_id}: {message}")

    def error(self, message: str):
        self.get_request_id()
        self.logger.error(f"{self.request_id}: {message}")

    def debug(self, message: str):
        self.get_request_id()
        self.logger.debug(f"{self.request_id}: {message}")

    def warning(self, message: str):
        self.get_request_id()
        self.logger.warning(f"{self.request_id}: {message}")

    def critical(self, message: str):
        self.get_request_id()
        self.logger.critical(f"{self.request_id}: {message}")

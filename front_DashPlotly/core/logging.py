import logging

format='%(asctime)s | %(levelname)s | %(filename)s:%(funcName)s:%(lineno)d | %(message)s'

# Get gunicorn.access logger
class HealthFilter(logging.Filter):
    def filter(self, record):
        return "/health" not in record.getMessage()

logging.getLogger("gunicorn.access").addFilter(HealthFilter())

# Get app logger

logging.basicConfig(level=logging.INFO, format=format)

logger = logging.getLogger(__name__)

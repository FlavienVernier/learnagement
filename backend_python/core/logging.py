import logging
import re

format='%(asctime)s | %(levelname)s | %(filename)s:%(funcName)s:%(lineno)d | %(message)s'

# Get "uvicorn.access" logger
access_logger = logging.getLogger("uvicorn.access")
class HealthFilter(logging.Filter):
    def filter(self, record):
        return "/health" not in record.getMessage()

access_logger.addFilter(HealthFilter())

formatter = logging.Formatter(
    fmt=format
)

for handler in access_logger.handlers:
    handler.setFormatter(formatter)

logging.basicConfig(level=logging.INFO, format=format)

logger = logging.getLogger(__name__)

_WHITESPACE_RE = re.compile(r"\s+")

def compact_sql(sql: str) -> str:
    """Remplace tout enchaînement d'espaces, tabulations et retours à la ligne par un seul espace."""
    return _WHITESPACE_RE.sub(" ", sql).strip()
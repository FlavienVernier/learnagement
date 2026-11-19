import logging
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(filename)s:%(funcName)s:%(lineno)d - %(message)s')

logger = logging.getLogger(__name__)

_WHITESPACE_RE = re.compile(r"\s+")

def compact_sql(sql: str) -> str:
    """Remplace tout enchaînement d'espaces, tabulations et retours à la ligne par un seul espace."""
    return _WHITESPACE_RE.sub(" ", sql).strip()
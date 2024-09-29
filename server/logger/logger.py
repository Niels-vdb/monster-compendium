import sys
from loguru import logger

logger.remove()
logger.add(
    sys.stdout,
    format="<level>{level}</level>: {message}",
    level="DEBUG",
)
logger.add(
    "server/logs/COMPENDIUM.log",
    format="{time:MMMM D, YYYY HH:mm:ss} - <level>{level}</level> - {module}/{file}/{function}/{line}: {message} - {exception}",
    level="INFO",
)

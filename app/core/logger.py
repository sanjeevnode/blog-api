import sys
from loguru import logger as _lg_logger

def get_logger():
    """Return the configured loguru logger instance"""
    return _lg_logger


def escape_log_braces(message:str | Exception) -> str:
    """Escapes curly braces in log messages to prevent Loguru from trying to format them."""
    return str(message).replace("{", "{{").replace("}", "}}")



# Remove default Loguru handler first
_lg_logger.remove()
    
# Single stderr sink – clean for Docker log drivers
_lg_logger.add(
    sys.stderr,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    ),
    level="DEBUG",
    colorize=True,
    enqueue=True,
)

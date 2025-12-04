import logging
import os
from logging.handlers import RotatingFileHandler

# Define default configuration constants
LOG_LEVEL_DEFAULT = os.environ.get("LOG_LEVEL", "info").upper()
LOG_FILE_ENABLED = os.environ.get("LOG_FILE_ENABLED", "false").lower() in ('true', 'yes', '1')
LOG_FILE_PATH = os.environ.get("LOG_FILE_PATH", "application.log")
MAX_BYTES = 10 * 1024 * 1024  # 10 MB
BACKUP_COUNT = 5

def setup_logging():
    """
    Sets up the root logger configuration for the application.

    This function configures a console handler and a rotating file handler.
    It should be called once at the start of the application.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVEL_DEFAULT)

    # Prevent running this setup multiple times if imported repeatedly
    if root_logger.hasHandlers():
        return

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Setup Console Handler (for development/monitoring)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    if LOG_FILE_ENABLED:
        try:
            file_handler = RotatingFileHandler(
                LOG_FILE_PATH,
                maxBytes=MAX_BYTES,
                backupCount=BACKUP_COUNT
            )
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        except IOError as e:
            # Log to console if we can't write to the file system (e.g., permissions error)
            logging.error(f"Failed to set up file logger: {e}")
    else:
        logging.info("File logging is disabled via configuration.")

def get_logger(name: str) -> logging.Logger:
    """
    Provides a standardized way for other modules to get their specific logger.
    """
    return logging.getLogger(name)

# Call setup automatically when the module is imported
setup_logging()

# Example of using the logger from within this module
if __name__ == "__main__":
    # This block runs only when you execute logger.py directly
    logger = get_logger(__name__)
    logger.info("Logger system initialized and tested.")
    logger.debug(f"Default log level set to: {LOG_LEVEL_DEFAULT}")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")

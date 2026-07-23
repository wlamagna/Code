#!/usr/bin/python
# rr_logger.py
import logging
import logging.handlers
import sys
import os

# --- Configuration ---
LOG_FILENAME = 'round_robin.log'
MAX_BYTES = 1024 * 10  # 10 KB (adjust this to your desired size, e.g., 1024 * 1024 for 1MB)
BACKUP_COUNT = 5       # Keep a maximum of 5 backup log files (round_robin.log.1, round_robin.log.2, etc.)

def configure_logger():
    """Configures the logger with a RotatingFileHandler."""

    # 1. Create a logger instance
    logger = logging.getLogger('RoundRobinLogger')
    logger.setLevel(logging.INFO)

    # 2. Define the log message format
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )

    # 3. Create a RotatingFileHandler
    # This is the core of the round robin/log rotation implementation.
    # It ensures the log file rotates after reaching MAX_BYTES,
    # keeping up to BACKUP_COUNT previous files.
    handler = logging.handlers.RotatingFileHandler(
        filename=LOG_FILENAME,
        maxBytes=MAX_BYTES,
        backupCount=BACKUP_COUNT,
        encoding='utf-8'
    )

    # 4. Set the formatter and add the handler to the logger
    handler.setFormatter(formatter)

    # Optionally, add a StreamHandler to print to the console as well
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    if not logger.handlers: # Prevent adding handlers multiple times
        logger.addHandler(handler)
        logger.addHandler(stream_handler)

    return logger

def log_input_message(message):
    """Logs the given message using the configured rotating logger."""

    logger = configure_logger()

    # Log the message as an INFO level message
    logger.info(message)

    print(f"\nSuccessfully logged: '{message}'")
    print(f"Check the log file: {os.path.abspath(LOG_FILENAME)}")

# --- Main execution block ---
if __name__ == '__main__':
    # Check if an argument (the message) was provided
    if len(sys.argv) < 2:
        print("Usage: python rr_logger.py \"Your log message here\"")
        sys.exit(1)

    # The message is the first argument after the script name (sys.argv[0])
    input_message = sys.argv[1]

    # Execute the logging function
    log_input_message(input_message)


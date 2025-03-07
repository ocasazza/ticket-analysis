"""
Logger module for Ticket Analytics.

This module provides logging configuration for the Ticket Analytics library.
"""
import logging
import sys


def setup_logger(log_file="freshservice_scraper.log"):
    """
    Set up and configure the logger.

    Args:
        log_file: Path to the log file

    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger("freshservice_scraper")
    logger.setLevel(logging.DEBUG)

    # Remove existing handlers if any
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Set up logging to file
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Also log to console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger


# Default logger instance
logger = setup_logger()

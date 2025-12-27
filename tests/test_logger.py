"""Tests for logger module."""

import logging

from csv2iif.logger import setup_logger


def test_setup_logger_default_level():
    """Test logger setup with default INFO level."""
    logger = setup_logger("test_default")
    assert logger.level == logging.INFO


def test_setup_logger_custom_level():
    """Test logger setup with custom level."""
    logger = setup_logger("test_custom", level="DEBUG")
    assert logger.level == logging.DEBUG


def test_setup_logger_env_level(monkeypatch):
    """Test logger setup with LOG_LEVEL environment variable."""
    monkeypatch.setenv("LOG_LEVEL", "WARNING")
    logger = setup_logger("test_env")
    assert logger.level == logging.WARNING


def test_setup_logger_invalid_level():
    """Test logger setup with invalid level defaults to INFO."""
    logger = setup_logger("test_invalid", level="INVALID")
    assert logger.level == logging.INFO


def test_setup_logger_has_handler():
    """Test logger has a handler configured."""
    logger = setup_logger("test_handler")
    assert len(logger.handlers) > 0

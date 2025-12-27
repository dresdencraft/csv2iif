"""Tests for converter module."""

import tempfile
from pathlib import Path

import pytest

from csv2iif.converter import Converter


def create_temp_csv(content: str) -> Path:
    """Helper to create temporary CSV file."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as temp_file:
        temp_file.write(content)
        return Path(temp_file.name)


def test_converter_successful_conversion():
    """Test successful conversion from CSV to IIF."""
    csv_content = """date,credit-account,debit-account,number,name,amount,memo
01/15/2024,Sales Income,Checking,1001,John Doe,500.00,Payment received"""
    csv_file = create_temp_csv(csv_content)

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".iif") as temp_iif:
        iif_path = Path(temp_iif.name)

    try:
        converter = Converter(str(csv_file), str(iif_path))
        converter.convert()

        assert iif_path.exists()
        content = iif_path.read_text()
        assert "!TRNS" in content
        assert "John Doe" in content
        assert "500.00" in content
    finally:
        csv_file.unlink()
        iif_path.unlink()


def test_converter_input_file_not_found():
    """Test converter with non-existent input file."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".iif") as temp_iif:
        iif_path = Path(temp_iif.name)

    try:
        converter = Converter("/nonexistent/file.csv", str(iif_path))
        with pytest.raises(FileNotFoundError):
            converter.convert()
    finally:
        iif_path.unlink()


def test_converter_invalid_csv_data():
    """Test converter with invalid CSV data."""
    csv_content = """date,credit-account,debit-account,number,name,amount,memo
13/45/2024,Sales Income,Checking,1001,John Doe,500.00,Payment received"""
    csv_file = create_temp_csv(csv_content)

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".iif") as temp_iif:
        iif_path = Path(temp_iif.name)

    try:
        converter = Converter(str(csv_file), str(iif_path))
        with pytest.raises(ValueError):
            converter.convert()
    finally:
        csv_file.unlink()
        iif_path.unlink()


def test_converter_multiple_transactions():
    """Test converter with multiple transactions."""
    csv_content = """date,credit-account,debit-account,number,name,amount,memo
01/15/2024,Sales Income,Checking,1001,John Doe,500.00,Payment received
01/16/2024,Checking,Office Supplies,1002,Office Depot,75.50,Printer paper"""
    csv_file = create_temp_csv(csv_content)

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".iif") as temp_iif:
        iif_path = Path(temp_iif.name)

    try:
        converter = Converter(str(csv_file), str(iif_path))
        converter.convert()

        content = iif_path.read_text()
        lines = [line for line in content.split("\n") if line.startswith("ENDTRNS")]
        assert len(lines) == 2
    finally:
        csv_file.unlink()
        iif_path.unlink()

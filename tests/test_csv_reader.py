"""Tests for csv_reader module."""

import tempfile
from pathlib import Path

import pytest

from csv2iif.csv_reader import CSVReader


def create_temp_csv(content: str) -> Path:
    """Helper to create temporary CSV file."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as temp_file:
        temp_file.write(content)
        return Path(temp_file.name)


def test_csv_reader_valid_file():
    """Test reading a valid CSV file."""
    content = """date,credit-account,debit-account,number,name,amount,memo
01/15/2024,Sales Income,Checking,1001,John Doe,500.00,Payment received"""
    csv_file = create_temp_csv(content)

    try:
        reader = CSVReader(str(csv_file))
        transactions = reader.read()
        assert len(transactions) == 1
        assert transactions[0].name == "John Doe"
        assert transactions[0].amount == "500.00"
    finally:
        csv_file.unlink()


def test_csv_reader_multiple_transactions():
    """Test reading multiple transactions."""
    content = """date,credit-account,debit-account,number,name,amount,memo
01/15/2024,Sales Income,Checking,1001,John Doe,500.00,Payment received
01/16/2024,Checking,Office Supplies,1002,Office Depot,75.50,Printer paper"""
    csv_file = create_temp_csv(content)

    try:
        reader = CSVReader(str(csv_file))
        transactions = reader.read()
        assert len(transactions) == 2
    finally:
        csv_file.unlink()


def test_csv_reader_flexible_column_order():
    """Test CSV with different column order."""
    content = """amount,date,name,memo,number,debit-account,credit-account
500.00,01/15/2024,John Doe,Payment received,1001,Checking,Sales Income"""
    csv_file = create_temp_csv(content)

    try:
        reader = CSVReader(str(csv_file))
        transactions = reader.read()
        assert len(transactions) == 1
        assert transactions[0].name == "John Doe"
    finally:
        csv_file.unlink()


def test_csv_reader_case_insensitive_headers():
    """Test CSV with mixed case headers."""
    content = """Date,Credit-Account,DEBIT-ACCOUNT,Number,Name,Amount,Memo
01/15/2024,Sales Income,Checking,1001,John Doe,500.00,Payment received"""
    csv_file = create_temp_csv(content)

    try:
        reader = CSVReader(str(csv_file))
        transactions = reader.read()
        assert len(transactions) == 1
    finally:
        csv_file.unlink()


def test_csv_reader_missing_column():
    """Test CSV with missing required column."""
    content = """date,credit-account,debit-account,number,name,amount
01/15/2024,Sales Income,Checking,1001,John Doe,500.00"""
    csv_file = create_temp_csv(content)

    try:
        reader = CSVReader(str(csv_file))
        with pytest.raises(ValueError, match="Missing required columns: memo"):
            reader.read()
    finally:
        csv_file.unlink()


def test_csv_reader_file_not_found():
    """Test reading non-existent file."""
    reader = CSVReader("/nonexistent/file.csv")
    with pytest.raises(FileNotFoundError):
        reader.read()


def test_csv_reader_empty_file():
    """Test reading empty CSV file."""
    csv_file = create_temp_csv("")

    try:
        reader = CSVReader(str(csv_file))
        with pytest.raises(ValueError, match="CSV file is empty"):
            reader.read()
    finally:
        csv_file.unlink()


def test_csv_reader_headers_only():
    """Test CSV with headers but no data."""
    content = """date,credit-account,debit-account,number,name,amount,memo"""
    csv_file = create_temp_csv(content)

    try:
        reader = CSVReader(str(csv_file))
        transactions = reader.read()
        assert len(transactions) == 0
    finally:
        csv_file.unlink()


def test_csv_reader_invalid_row_data():
    """Test CSV with invalid data in row."""
    content = """date,credit-account,debit-account,number,name,amount,memo
13/45/2024,Sales Income,Checking,1001,John Doe,500.00,Payment received"""
    csv_file = create_temp_csv(content)

    try:
        reader = CSVReader(str(csv_file))
        with pytest.raises(ValueError, match="Error in row 2"):
            reader.read()
    finally:
        csv_file.unlink()


def test_csv_reader_empty_value_in_row():
    """Test CSV with empty required value in row."""
    content = """date,credit-account,debit-account,number,name,amount,memo
01/15/2024,,Checking,1001,John Doe,500.00,Payment received"""
    csv_file = create_temp_csv(content)

    try:
        reader = CSVReader(str(csv_file))
        with pytest.raises(ValueError, match="Error in row 2"):
            reader.read()
    finally:
        csv_file.unlink()


def test_csv_reader_empty_number_allowed():
    """Test CSV with empty number is allowed."""
    content = """date,credit-account,debit-account,number,name,amount,memo
01/15/2024,Sales Income,Checking,,John Doe,500.00,Payment received"""
    csv_file = create_temp_csv(content)

    try:
        reader = CSVReader(str(csv_file))
        transactions = reader.read()
        assert len(transactions) == 1
        assert transactions[0].number == ""
    finally:
        csv_file.unlink()


def test_csv_reader_empty_name_allowed():
    """Test CSV with empty name is allowed."""
    content = """date,credit-account,debit-account,number,name,amount,memo
01/15/2024,Sales Income,Checking,1001,,500.00,Payment received"""
    csv_file = create_temp_csv(content)

    try:
        reader = CSVReader(str(csv_file))
        transactions = reader.read()
        assert len(transactions) == 1
        assert transactions[0].name == ""
    finally:
        csv_file.unlink()


def test_csv_reader_skip_empty_rows():
    """Test CSV skips empty rows."""
    content = """date,credit-account,debit-account,number,name,amount,memo
01/15/2024,Sales Income,Checking,1001,John Doe,500.00,Payment received

01/16/2024,Checking,Office Supplies,1002,Office Depot,75.50,Printer paper"""
    csv_file = create_temp_csv(content)

    try:
        reader = CSVReader(str(csv_file))
        transactions = reader.read()
        assert len(transactions) == 2
    finally:
        csv_file.unlink()

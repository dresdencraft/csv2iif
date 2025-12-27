"""Tests for models module."""

import pytest

from csv2iif.models import Transaction


def test_transaction_valid():
    """Test creating a valid transaction."""
    transaction = Transaction(
        date="01/15/2024",
        credit_account="Sales Income",
        debit_account="Checking",
        number="1001",
        name="John Doe",
        amount="500.00",
        memo="Payment received",
    )
    assert transaction.date == "01/15/2024"
    assert transaction.amount == "500.00"


def test_transaction_amount_formatting():
    """Test amount is formatted to 2 decimal places."""
    transaction = Transaction(
        date="01/15/2024",
        credit_account="Sales Income",
        debit_account="Checking",
        number="1001",
        name="John Doe",
        amount="500",
        memo="Payment",
    )
    assert transaction.amount == "500.00"


def test_transaction_invalid_date():
    """Test transaction with invalid date raises ValueError."""
    with pytest.raises(ValueError, match="Invalid date format"):
        Transaction(
            date="13/45/2024",
            credit_account="Sales Income",
            debit_account="Checking",
            number="1001",
            name="John Doe",
            amount="500.00",
            memo="Payment",
        )


def test_transaction_invalid_date_format():
    """Test transaction with wrong date format raises ValueError."""
    with pytest.raises(ValueError, match="Invalid date format"):
        Transaction(
            date="2024-01-15",
            credit_account="Sales Income",
            debit_account="Checking",
            number="1001",
            name="John Doe",
            amount="500.00",
            memo="Payment",
        )


def test_transaction_negative_amount():
    """Test transaction with negative amount raises ValueError."""
    with pytest.raises(ValueError, match="Amount must be positive"):
        Transaction(
            date="01/15/2024",
            credit_account="Sales Income",
            debit_account="Checking",
            number="1001",
            name="John Doe",
            amount="-100.00",
            memo="Payment",
        )


def test_transaction_zero_amount():
    """Test transaction with zero amount raises ValueError."""
    with pytest.raises(ValueError, match="Amount must be positive"):
        Transaction(
            date="01/15/2024",
            credit_account="Sales Income",
            debit_account="Checking",
            number="1001",
            name="John Doe",
            amount="0",
            memo="Payment",
        )


def test_transaction_invalid_amount():
    """Test transaction with invalid amount raises ValueError."""
    with pytest.raises(ValueError, match="Invalid amount"):
        Transaction(
            date="01/15/2024",
            credit_account="Sales Income",
            debit_account="Checking",
            number="1001",
            name="John Doe",
            amount="abc",
            memo="Payment",
        )


def test_transaction_empty_field():
    """Test transaction with empty required field raises ValueError."""
    with pytest.raises(ValueError, match="Required fields cannot be empty"):
        Transaction(
            date="01/15/2024",
            credit_account="",
            debit_account="Checking",
            number="1001",
            name="John Doe",
            amount="500.00",
            memo="Payment",
        )


def test_transaction_whitespace_field():
    """Test transaction with whitespace-only required field raises ValueError."""
    with pytest.raises(ValueError, match="Required fields cannot be empty"):
        Transaction(
            date="01/15/2024",
            credit_account="Sales Income",
            debit_account="   ",
            number="1001",
            name="John Doe",
            amount="500.00",
            memo="Payment",
        )


def test_transaction_empty_number_allowed():
    """Test transaction with empty number is allowed."""
    transaction = Transaction(
        date="01/15/2024",
        credit_account="Sales Income",
        debit_account="Checking",
        number="",
        name="John Doe",
        amount="500.00",
        memo="Payment",
    )
    assert transaction.number == ""


def test_transaction_empty_name_allowed():
    """Test transaction with empty name is allowed."""
    transaction = Transaction(
        date="01/15/2024",
        credit_account="Sales Income",
        debit_account="Checking",
        number="1001",
        name="",
        amount="500.00",
        memo="Payment",
    )
    assert transaction.name == ""

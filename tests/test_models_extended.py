"""Additional tests for models module."""


from csv2iif.models import Transaction


def test_transaction_amount_with_dollar_sign():
    """Test transaction with dollar sign in amount."""
    transaction = Transaction(
        date="01/15/2024",
        credit_account="Sales Income",
        debit_account="Checking",
        number="1001",
        name="John Doe",
        amount="$500.00",
        memo="Payment",
    )
    assert transaction.amount == "500.00"


def test_transaction_amount_with_comma():
    """Test transaction with comma in amount."""
    transaction = Transaction(
        date="01/15/2024",
        credit_account="Sales Income",
        debit_account="Checking",
        number="1001",
        name="John Doe",
        amount="$1,275.00",
        memo="Payment",
    )
    assert transaction.amount == "1275.00"


def test_transaction_amount_with_multiple_commas():
    """Test transaction with multiple commas in amount."""
    transaction = Transaction(
        date="01/15/2024",
        credit_account="Sales Income",
        debit_account="Checking",
        number="1001",
        name="John Doe",
        amount="$10,000,000.00",
        memo="Payment",
    )
    assert transaction.amount == "10000000.00"

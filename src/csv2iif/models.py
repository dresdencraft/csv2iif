"""Data models for csv2iif."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation


@dataclass
class Transaction:
    """Represents a single transaction with validation."""

    date: str
    credit_account: str
    debit_account: str
    number: str
    name: str
    amount: str
    memo: str

    def __post_init__(self) -> None:
        """Validate transaction data after initialization."""
        self._validate_date()
        self._validate_amount()
        self._validate_required_fields()

    def _validate_date(self) -> None:
        """Validate date format is MM/DD/YYYY and represents a valid date."""
        try:
            datetime.strptime(self.date, "%m/%d/%Y")
        except ValueError as e:
            raise ValueError(f"Invalid date format '{self.date}': {e}") from e

    def _validate_amount(self) -> None:
        """Validate amount is positive and format to 2 decimal places."""
        amount_str = self.amount.strip()
        amount_str = amount_str.lstrip("$").replace(",", "")

        try:
            amount_decimal = Decimal(amount_str)
        except (InvalidOperation, ValueError) as e:
            raise ValueError(f"Invalid amount '{self.amount}': {e}") from e

        if amount_decimal <= 0:
            raise ValueError(f"Amount must be positive, got: {self.amount}")

        self.amount = f"{amount_decimal:.2f}"

    def _validate_required_fields(self) -> None:
        """Validate all required fields are non-empty."""
        fields = {
            "date": self.date,
            "credit_account": self.credit_account,
            "debit_account": self.debit_account,
            "amount": self.amount,
            "memo": self.memo,
        }

        empty_fields = [name for name, value in fields.items() if not value or not value.strip()]

        if empty_fields:
            raise ValueError(f"Required fields cannot be empty: {', '.join(empty_fields)}")

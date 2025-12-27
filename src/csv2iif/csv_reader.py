"""CSV reader for csv2iif."""

import csv
from pathlib import Path

from csv2iif.logger import setup_logger
from csv2iif.models import Transaction

logger = setup_logger(__name__)


class CSVReader:
    """Reads and validates CSV files with flexible column ordering."""

    REQUIRED_COLUMNS = {
        "date",
        "credit-account",
        "debit-account",
        "number",
        "name",
        "amount",
        "memo",
    }

    def __init__(self, file_path: str) -> None:
        """
        Initialize CSV reader.

        Args:
            file_path: Path to CSV file
        """
        self.file_path = Path(file_path)
        self.column_mapping: dict[str, int] = {}

    def read(self) -> list[Transaction]:
        """
        Read CSV file and return list of Transaction objects.

        Returns:
            List of validated Transaction objects

        Raises:
            FileNotFoundError: If CSV file doesn't exist
            ValueError: If required columns are missing or data is invalid
        """
        if not self.file_path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.file_path}")

        logger.info(f"Reading CSV file: {self.file_path}")

        with open(self.file_path, encoding="utf-8") as f:
            reader = csv.reader(f)
            headers = next(reader, None)

            if headers is None:
                raise ValueError("CSV file is empty")

            self._validate_headers(headers)
            transactions = self._parse_rows(reader)

        logger.info(f"Successfully read {len(transactions)} transactions")
        return transactions

    def _validate_headers(self, headers: list[str]) -> None:
        """
        Validate CSV headers contain all required columns.

        Args:
            headers: List of column names from CSV

        Raises:
            ValueError: If required columns are missing
        """
        normalized_headers = {}
        for i, h in enumerate(headers):
            normalized = h.strip().lower()
            if normalized and normalized not in normalized_headers:
                normalized_headers[normalized] = i

        missing_columns = self.REQUIRED_COLUMNS - normalized_headers.keys()

        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(sorted(missing_columns))}")

        self.column_mapping = {col: normalized_headers[col] for col in self.REQUIRED_COLUMNS}
        logger.debug(f"Column mapping: {self.column_mapping}")

    def _parse_rows(self, reader: csv.reader) -> list[Transaction]:
        """
        Parse CSV rows into Transaction objects.

        Args:
            reader: CSV reader object

        Returns:
            List of Transaction objects

        Raises:
            ValueError: If row data is invalid
        """
        transactions = []

        for row_num, row in enumerate(reader, start=2):
            if not row or all(not cell.strip() for cell in row):
                continue

            try:
                transaction = self._create_transaction(row)
                transactions.append(transaction)
            except (ValueError, IndexError) as e:
                raise ValueError(f"Error in row {row_num}: {e}") from e

        return transactions

    def _create_transaction(self, row: list[str]) -> Transaction:
        """
        Create Transaction object from CSV row.

        Args:
            row: List of values from CSV row

        Returns:
            Transaction object
        """
        return Transaction(
            date=row[self.column_mapping["date"]].strip(),
            credit_account=row[self.column_mapping["credit-account"]].strip(),
            debit_account=row[self.column_mapping["debit-account"]].strip(),
            number=row[self.column_mapping["number"]].strip(),
            name=row[self.column_mapping["name"]].strip(),
            amount=row[self.column_mapping["amount"]].strip(),
            memo=row[self.column_mapping["memo"]].strip(),
        )

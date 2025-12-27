"""IIF writer for csv2iif."""

from pathlib import Path

from csv2iif.logger import setup_logger
from csv2iif.models import Transaction

logger = setup_logger(__name__)


class IIFWriter:
    """Writes transactions to IIF format file."""

    def __init__(self, file_path: str) -> None:
        """
        Initialize IIF writer.

        Args:
            file_path: Path to output IIF file
        """
        self.file_path = Path(file_path)

    def write(self, transactions: list[Transaction]) -> None:
        """
        Write transactions to IIF file.

        Args:
            transactions: List of Transaction objects to write

        Raises:
            IOError: If file cannot be written
        """
        logger.info(f"Writing {len(transactions)} transactions to IIF file: {self.file_path}")

        with open(self.file_path, "w", encoding="utf-8") as f:
            self._write_headers(f)
            self._write_transactions(f, transactions)

        logger.info("Successfully wrote IIF file")

    def _write_headers(self, f) -> None:
        """
        Write IIF headers to file.

        Args:
            f: File object
        """
        f.write("!TRNS\tTRNSID\tTRNSTYPE\tDATE\tACCNT\tNAME\tAMOUNT\tDOCNUM\tMEMO\n")
        f.write("!SPL\tSPLID\tTRNSTYPE\tDATE\tACCNT\tNAME\tAMOUNT\tDOCNUM\tMEMO\n")
        f.write("!ENDTRNS\n")

    def _write_transactions(self, f, transactions: list[Transaction]) -> None:
        """
        Write transaction entries to file.

        Args:
            f: File object
            transactions: List of Transaction objects
        """
        for transaction in transactions:
            self._write_transaction_block(f, transaction)

    def _write_transaction_block(self, f, transaction: Transaction) -> None:
        """
        Write a single transaction block (TRNS/SPL/ENDTRNS).

        Args:
            f: File object
            transaction: Transaction object
        """
        trns_line = self._format_trns_line(transaction)
        spl_line = self._format_spl_line(transaction)

        f.write(f"{trns_line}\n")
        f.write(f"{spl_line}\n")
        f.write("ENDTRNS\n")

    def _format_trns_line(self, transaction: Transaction) -> str:
        """
        Format TRNS line for transaction.

        Args:
            transaction: Transaction object

        Returns:
            Formatted TRNS line
        """
        return (
            f"TRNS\t\tGENERAL JOURNAL\t{transaction.date}\t"
            f"{transaction.debit_account}\t{transaction.name}\t"
            f"{transaction.amount}\t{transaction.number}\t{transaction.memo}"
        )

    def _format_spl_line(self, transaction: Transaction) -> str:
        """
        Format SPL line for transaction.

        Args:
            transaction: Transaction object

        Returns:
            Formatted SPL line
        """
        negative_amount = f"-{transaction.amount}"
        return (
            f"SPL\t\tGENERAL JOURNAL\t{transaction.date}\t"
            f"{transaction.credit_account}\t{transaction.name}\t"
            f"{negative_amount}\t{transaction.number}\t{transaction.memo}"
        )

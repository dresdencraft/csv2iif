"""Tests for iif_writer module."""

import tempfile
from pathlib import Path

from csv2iif.iif_writer import IIFWriter
from csv2iif.models import Transaction


def test_iif_writer_single_transaction():
    """Test writing a single transaction to IIF file."""
    transaction = Transaction(
        date="01/15/2024",
        credit_account="Sales Income",
        debit_account="Checking",
        number="1001",
        name="John Doe",
        amount="500.00",
        memo="Payment received",
    )

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".iif") as temp_file:
        temp_path = Path(temp_file.name)

    try:
        writer = IIFWriter(str(temp_path))
        writer.write([transaction])

        content = temp_path.read_text()
        lines = content.strip().split("\n")

        assert lines[0] == "!TRNS\tTRNSID\tTRNSTYPE\tDATE\tACCNT\tNAME\tAMOUNT\tDOCNUM\tMEMO"
        assert lines[1] == "!SPL\tSPLID\tTRNSTYPE\tDATE\tACCNT\tNAME\tAMOUNT\tDOCNUM\tMEMO"
        assert lines[2] == "!ENDTRNS"
        expected_trns = (
            "TRNS\t\tGENERAL JOURNAL\t01/15/2024\tChecking\t"
            "John Doe\t500.00\t1001\tPayment received"
        )
        expected_spl = (
            "SPL\t\tGENERAL JOURNAL\t01/15/2024\tSales Income\t"
            "John Doe\t-500.00\t1001\tPayment received"
        )
        assert expected_trns in lines[3]
        assert expected_spl in lines[4]
        assert lines[5] == "ENDTRNS"
    finally:
        temp_path.unlink()


def test_iif_writer_multiple_transactions():
    """Test writing multiple transactions to IIF file."""
    transactions = [
        Transaction(
            date="01/15/2024",
            credit_account="Sales Income",
            debit_account="Checking",
            number="1001",
            name="John Doe",
            amount="500.00",
            memo="Payment received",
        ),
        Transaction(
            date="01/16/2024",
            credit_account="Checking",
            debit_account="Office Supplies",
            number="1002",
            name="Office Depot",
            amount="75.50",
            memo="Printer paper",
        ),
    ]

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".iif") as temp_file:
        temp_path = Path(temp_file.name)

    try:
        writer = IIFWriter(str(temp_path))
        writer.write(transactions)

        content = temp_path.read_text()
        lines = content.strip().split("\n")

        assert len(lines) == 9
        assert lines[0].startswith("!TRNS")
        assert lines[3].startswith("TRNS")
        assert lines[4].startswith("SPL")
        assert lines[5] == "ENDTRNS"
        assert lines[6].startswith("TRNS")
        assert lines[7].startswith("SPL")
        assert lines[8] == "ENDTRNS"
    finally:
        temp_path.unlink()


def test_iif_writer_empty_transactions():
    """Test writing empty transaction list."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".iif") as temp_file:
        temp_path = Path(temp_file.name)

    try:
        writer = IIFWriter(str(temp_path))
        writer.write([])

        content = temp_path.read_text()
        lines = content.strip().split("\n")

        assert len(lines) == 3
        assert lines[0].startswith("!TRNS")
        assert lines[1].startswith("!SPL")
        assert lines[2] == "!ENDTRNS"
    finally:
        temp_path.unlink()


def test_iif_writer_negative_amount_in_spl():
    """Test that SPL line has negative amount."""
    transaction = Transaction(
        date="01/15/2024",
        credit_account="Sales Income",
        debit_account="Checking",
        number="1001",
        name="John Doe",
        amount="500.00",
        memo="Payment",
    )

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".iif") as temp_file:
        temp_path = Path(temp_file.name)

    try:
        writer = IIFWriter(str(temp_path))
        writer.write([transaction])

        content = temp_path.read_text()
        assert "\t-500.00\t" in content
    finally:
        temp_path.unlink()


def test_iif_writer_tab_delimited():
    """Test that output is tab-delimited."""
    transaction = Transaction(
        date="01/15/2024",
        credit_account="Sales Income",
        debit_account="Checking",
        number="1001",
        name="John Doe",
        amount="500.00",
        memo="Payment",
    )

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".iif") as temp_file:
        temp_path = Path(temp_file.name)

    try:
        writer = IIFWriter(str(temp_path))
        writer.write([transaction])

        content = temp_path.read_text()
        lines = content.strip().split("\n")

        trns_line = [line for line in lines if line.startswith("TRNS\t")][0]
        assert "\t\t" in trns_line
        assert trns_line.count("\t") >= 7
    finally:
        temp_path.unlink()

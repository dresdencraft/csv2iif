"""Tests for cli module."""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from csv2iif.cli import main, parse_args


def create_temp_csv(content: str) -> Path:
    """Helper to create temporary CSV file."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as temp_file:
        temp_file.write(content)
        return Path(temp_file.name)


def test_parse_args_basic():
    """Test parsing basic arguments."""
    with patch("sys.argv", ["csv2iif", "input.csv", "output.iif"]):
        args = parse_args()
        assert args.input == "input.csv"
        assert args.output == "output.iif"
        assert args.verbose is False


def test_parse_args_verbose():
    """Test parsing with verbose flag."""
    with patch("sys.argv", ["csv2iif", "input.csv", "output.iif", "--verbose"]):
        args = parse_args()
        assert args.verbose is True


def test_parse_args_verbose_short():
    """Test parsing with verbose short flag."""
    with patch("sys.argv", ["csv2iif", "input.csv", "output.iif", "-v"]):
        args = parse_args()
        assert args.verbose is True


def test_main_successful_conversion():
    """Test main function with successful conversion."""
    csv_content = """date,credit-account,debit-account,number,name,amount,memo
01/15/2024,Sales Income,Checking,1001,John Doe,500.00,Payment received"""
    csv_file = create_temp_csv(csv_content)

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".iif") as temp_iif:
        iif_path = Path(temp_iif.name)

    try:
        with patch("sys.argv", ["csv2iif", str(csv_file), str(iif_path)]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0
    finally:
        csv_file.unlink()
        iif_path.unlink()


def test_main_file_not_found():
    """Test main function with non-existent file exits with code 2."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".iif") as temp_iif:
        iif_path = Path(temp_iif.name)

    try:
        with patch("sys.argv", ["csv2iif", "/nonexistent/file.csv", str(iif_path)]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 2
    finally:
        iif_path.unlink()


def test_main_validation_error():
    """Test main function with validation error exits with code 1."""
    csv_content = """date,credit-account,debit-account,number,name,amount,memo
13/45/2024,Sales Income,Checking,1001,John Doe,500.00,Payment received"""
    csv_file = create_temp_csv(csv_content)

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".iif") as temp_iif:
        iif_path = Path(temp_iif.name)

    try:
        with patch("sys.argv", ["csv2iif", str(csv_file), str(iif_path)]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
    finally:
        csv_file.unlink()
        iif_path.unlink()


def test_main_missing_columns():
    """Test main function with missing columns exits with code 1."""
    csv_content = """date,credit-account,debit-account,number,name,amount
01/15/2024,Sales Income,Checking,1001,John Doe,500.00"""
    csv_file = create_temp_csv(csv_content)

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".iif") as temp_iif:
        iif_path = Path(temp_iif.name)

    try:
        with patch("sys.argv", ["csv2iif", str(csv_file), str(iif_path)]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
    finally:
        csv_file.unlink()
        iif_path.unlink()


def test_validate_command():
    """Test validate command."""
    csv_content = """date,credit-account,debit-account,number,name,amount,memo
01/15/2024,Sales Income,Checking,1001,John Doe,500.00,Payment"""
    csv_file = create_temp_csv(csv_content)

    try:
        with patch("sys.argv", ["csv2iif", "validate", str(csv_file)]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0
    finally:
        csv_file.unlink()


def test_validate_command_invalid():
    """Test validate command with invalid CSV."""
    csv_content = """date,credit-account,debit-account,number,name,amount,memo
13/45/2024,Sales Income,Checking,1001,John Doe,500.00,Payment"""
    csv_file = create_temp_csv(csv_content)

    try:
        with patch("sys.argv", ["csv2iif", "validate", str(csv_file)]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
    finally:
        csv_file.unlink()


def test_clean_command():
    """Test clean command."""
    csv_content = """date,number,name,debit-account,credit-account,amount,memo,memo
01/15/2024,,,Checking,Sales Income,$500.00,Payment,"""
    csv_file = create_temp_csv(csv_content)

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as temp_out:
        output_path = Path(temp_out.name)

    try:
        with patch("sys.argv", ["csv2iif", "clean", str(csv_file), str(output_path)]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0

        content = output_path.read_text()
        assert "memo,memo" not in content
        assert content.count("memo") == 1
    finally:
        csv_file.unlink()
        output_path.unlink()


def test_clean_command_in_place():
    """Test clean command with in-place flag."""
    csv_content = """date,number,name,debit-account,credit-account,amount,memo,memo
01/15/2024,,,Checking,Sales Income,$500.00,Payment,"""
    csv_file = create_temp_csv(csv_content)

    try:
        with patch("sys.argv", ["csv2iif", "clean", str(csv_file), "-i"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0

        content = csv_file.read_text()
        assert "memo,memo" not in content
    finally:
        csv_file.unlink()


def test_clean_command_no_output():
    """Test clean command without output or in-place flag."""
    csv_content = """date,number,name,debit-account,credit-account,amount,memo
01/15/2024,,,Checking,Sales Income,$500.00,Payment"""
    csv_file = create_temp_csv(csv_content)

    try:
        with patch("sys.argv", ["csv2iif", "clean", str(csv_file)]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
    finally:
        csv_file.unlink()


def test_clean_command_empty_file():
    """Test clean command with empty file."""
    csv_file = create_temp_csv("")

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as temp_out:
        output_path = Path(temp_out.name)

    try:
        with patch("sys.argv", ["csv2iif", "clean", str(csv_file), str(output_path)]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
    finally:
        csv_file.unlink()
        output_path.unlink()


def test_convert_subcommand():
    """Test explicit convert subcommand."""
    csv_content = """date,credit-account,debit-account,number,name,amount,memo
01/15/2024,Sales Income,Checking,1001,John Doe,500.00,Payment"""
    csv_file = create_temp_csv(csv_content)

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".iif") as temp_iif:
        iif_path = Path(temp_iif.name)

    try:
        with patch("sys.argv", ["csv2iif", "convert", str(csv_file), str(iif_path)]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0
    finally:
        csv_file.unlink()
        iif_path.unlink()


def test_main_unexpected_error():
    """Test main function with unexpected error exits with code 3."""
    csv_content = """date,credit-account,debit-account,number,name,amount,memo
01/15/2024,Sales Income,Checking,1001,John Doe,500.00,Payment"""
    csv_file = create_temp_csv(csv_content)

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".iif") as temp_iif:
        iif_path = Path(temp_iif.name)

    try:
        with (
            patch("sys.argv", ["csv2iif", str(csv_file), str(iif_path)]),
            patch("csv2iif.cli.Converter") as mock_converter,
        ):
            mock_converter.return_value.convert.side_effect = RuntimeError("Unexpected")
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 3
    finally:
        csv_file.unlink()
        iif_path.unlink()


def test_validate_file_not_found():
    """Test validate command with non-existent file."""
    with patch("sys.argv", ["csv2iif", "validate", "/nonexistent/file.csv"]):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 2


def test_clean_file_not_found():
    """Test clean command with non-existent file."""
    with patch("sys.argv", ["csv2iif", "clean", "/nonexistent/file.csv", "/tmp/out.csv"]):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 2


def test_clean_io_error():
    """Test clean command with IO error."""
    csv_content = """date,number,name,debit-account,credit-account,amount,memo
01/15/2024,,,Checking,Sales Income,$500.00,Payment"""
    csv_file = create_temp_csv(csv_content)

    try:
        with patch("sys.argv", ["csv2iif", "clean", str(csv_file), "/invalid/path/out.csv"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 2
    finally:
        csv_file.unlink()


def test_clean_with_all_empty_rows():
    """Test clean command with rows that have only whitespace."""
    csv_content = """date,number,name,debit-account,credit-account,amount,memo
   ,  ,  ,  ,  ,  ,
01/15/2024,,,Checking,Sales Income,$500.00,Payment"""
    csv_file = create_temp_csv(csv_content)

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as temp_out:
        output_path = Path(temp_out.name)

    try:
        with patch("sys.argv", ["csv2iif", "clean", str(csv_file), str(output_path)]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0

        lines = output_path.read_text().strip().split("\n")
        assert len(lines) == 2
    finally:
        csv_file.unlink()
        output_path.unlink()

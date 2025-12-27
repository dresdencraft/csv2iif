"""Tests for __main__ module."""

import subprocess
import sys


def test_main_module_execution():
    """Test that python -m csv2iif works."""
    result = subprocess.run(
        [sys.executable, "-m", "csv2iif", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Convert CSV files to IIF format" in result.stdout

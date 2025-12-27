# CSV to IIF Converter

A Python CLI tool that converts CSV files to IIF (Intuit Interchange Format) for QuickBooks 2010 import.

## Features

- ✅ Convert CSV to IIF format for QuickBooks 2010
- ✅ Validate CSV files before conversion
- ✅ Clean CSV files (remove duplicate headers, trim whitespace)
- ✅ Flexible column ordering (case-insensitive)
- ✅ Support for dollar signs and commas in amounts ($1,275.00)
- ✅ Optional number and name fields
- ✅ Hierarchical account names (e.g., `Expenses:Tools:Owner Contributed`)
- ✅ 98% test coverage

## Installation

### Preferred Method: pipx from GitHub

```bash
pipx install git+https://github.com/dresdencraft/csv2iif.git
```

### Alternative: pip from GitHub

```bash
pip install git+https://github.com/dresdencraft/csv2iif.git
```

### From Source

```bash
git clone https://github.com/dresdencraft/csv2iif.git
cd csv2iif
pipx install .
```

## Requirements

- Python 3.12 or greater

## Usage

### Convert CSV to IIF

```bash
csv2iif input.csv output.iif
# or
csv2iif convert input.csv output.iif
```

### Validate CSV

```bash
csv2iif validate input.csv
```

### Clean CSV

Remove duplicate headers, trim whitespace, remove empty rows:

```bash
csv2iif clean input.csv output.csv
# or in-place
csv2iif clean input.csv -i
```

### Verbose Logging

```bash
csv2iif input.csv output.iif --verbose
```

### Set Log Level via Environment

```bash
LOG_LEVEL=DEBUG csv2iif input.csv output.iif
```

## CSV Format

The input CSV must contain a header row with the following columns (case-insensitive, any order):

- `date` - Transaction date (MM/DD/YYYY format) **[Required]**
- `credit-account` - Account to credit **[Required]**
- `debit-account` - Account to debit **[Required]**
- `number` - Transaction/check number **[Optional]**
- `name` - Payee/customer name **[Optional]**
- `amount` - Transaction amount (positive, supports $1,275.00 format) **[Required]**
- `memo` - Transaction memo/description **[Required]**

### Example CSV

```csv
date,credit-account,debit-account,number,name,amount,memo
01/15/2024,Sales Income,Checking,1001,John Doe,$500.00,Payment received
01/16/2024,Checking,Office Supplies,1002,Office Depot,$75.50,Printer paper
01/17/2024,Equity:Member's Equity,Expenses:Tools:Owner Contributed,,,"$1,275.00",Drill set
```

## IIF Output

The tool generates a tab-delimited IIF file with TRNS/SPL entries for double-entry bookkeeping:

```
!TRNS	TRNSID	TRNSTYPE	DATE	ACCNT	NAME	AMOUNT	DOCNUM	MEMO
!SPL	SPLID	TRNSTYPE	DATE	ACCNT	NAME	AMOUNT	DOCNUM	MEMO
!ENDTRNS
TRNS		GENERAL JOURNAL	01/15/2024	Checking	John Doe	500.00	1001	Payment received
SPL		GENERAL JOURNAL	01/15/2024	Sales Income	John Doe	-500.00	1001	Payment received
ENDTRNS
```

## Configuration

Create a `.env` file in your working directory:

```bash
LOG_LEVEL=INFO
```

CLI arguments override environment variables.

## Exit Codes

- `0` - Success
- `1` - Validation error (invalid data, missing columns, etc.)
- `2` - File error (file not found, permission denied, etc.)
- `3` - Conversion error (unexpected error during conversion)

## Development

### Install Development Dependencies

```bash
make install-dev
```

### Run Tests

```bash
make test
```

### Lint Code

```bash
make lint
```

### Format Code

```bash
make format
```

### Run in Development Mode

```bash
make run INPUT=input.csv OUTPUT=output.iif
```

### Clean Build Artifacts

```bash
make clean
```

## Validation Rules

- **Date Format**: MM/DD/YYYY only, must be valid calendar date
- **Amount**: Positive numbers only, supports dollar signs and commas ($1,275.00)
- **Required Fields**: date, credit-account, debit-account, amount, memo
- **Optional Fields**: number, name (can be empty)
- **Column Names**: Case-insensitive matching
- **Duplicate Headers**: First occurrence used, duplicates ignored

## Project Structure

```
csv2iif/
├── src/
│   └── csv2iif/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── converter.py
│       ├── csv_reader.py
│       ├── iif_writer.py
│       ├── logger.py
│       └── models.py
├── tests/
│   ├── test_cli.py
│   ├── test_converter.py
│   ├── test_csv_reader.py
│   ├── test_iif_writer.py
│   ├── test_logger.py
│   ├── test_main.py
│   ├── test_models.py
│   └── test_models_extended.py
├── Makefile
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## License

Apache License 2.0
# Test PR Pipeline

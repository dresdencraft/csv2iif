"""Command-line interface for csv2iif."""

import argparse
import sys

from dotenv import load_dotenv

from csv2iif.converter import Converter
from csv2iif.logger import setup_logger

load_dotenv()


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments
    """
    if len(sys.argv) >= 3 and sys.argv[1] not in ["convert", "validate", "clean", "-h", "--help"]:
        args = argparse.Namespace()
        args.command = "convert"
        args.input = sys.argv[1]
        args.output = sys.argv[2]
        args.verbose = len(sys.argv) == 4 and sys.argv[3] in ["-v", "--verbose"]
        return args

    parser = argparse.ArgumentParser(
        description="Convert CSV files to IIF format for QuickBooks 2010",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    convert_parser = subparsers.add_parser("convert", help="Convert CSV to IIF")
    convert_parser.add_argument("input", type=str, help="Input CSV file path")
    convert_parser.add_argument("output", type=str, help="Output IIF file path")
    convert_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging (DEBUG level)",
    )

    validate_parser = subparsers.add_parser("validate", help="Validate CSV file")
    validate_parser.add_argument("input", type=str, help="Input CSV file path")
    validate_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging (DEBUG level)",
    )

    clean_parser = subparsers.add_parser("clean", help="Clean and trim CSV file")
    clean_parser.add_argument("input", type=str, help="Input CSV file path")
    clean_parser.add_argument("output", type=str, nargs="?", help="Output cleaned CSV file path")
    clean_parser.add_argument(
        "-i",
        "--in-place",
        action="store_true",
        help="Edit file in place",
    )
    clean_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging (DEBUG level)",
    )

    return parser.parse_args()


def main() -> None:
    """Main entry point for CLI."""
    args = parse_args()

    log_level = "DEBUG" if args.verbose else None
    logger = setup_logger(__name__, level=log_level)

    try:
        if args.command == "convert":
            converter = Converter(args.input, args.output)
            converter.convert()
            sys.exit(0)

        elif args.command == "validate":
            from csv2iif.csv_reader import CSVReader

            reader = CSVReader(args.input)
            transactions = reader.read()
            logger.info(f"Validation successful: {len(transactions)} transactions found")
            print(f"✓ CSV is valid: {len(transactions)} transactions")
            sys.exit(0)

        elif args.command == "clean":
            import csv
            import tempfile
            from pathlib import Path

            input_path = Path(args.input)

            if args.in_place:
                output_path = Path(tempfile.mktemp(suffix=".csv"))
            elif args.output:
                output_path = Path(args.output)
            else:
                raise ValueError("Either --in-place or output path must be specified")

            with open(input_path, encoding="utf-8") as infile:
                reader = csv.reader(infile)
                rows = list(reader)

            if not rows:
                raise ValueError("CSV file is empty")

            headers = [h.strip() for h in rows[0]]
            seen = set()
            unique_headers = []
            for h in headers:
                if h and h.lower() not in seen:
                    unique_headers.append(h)
                    seen.add(h.lower())

            cleaned_rows = [unique_headers]
            for row in rows[1:]:
                if not row or all(not cell.strip() for cell in row):
                    continue
                cleaned_row = [cell.strip() for cell in row[: len(unique_headers)]]
                cleaned_rows.append(cleaned_row)

            with open(output_path, "w", encoding="utf-8", newline="") as outfile:
                writer = csv.writer(outfile)
                writer.writerows(cleaned_rows)

            if args.in_place:
                import shutil

                shutil.move(str(output_path), str(input_path))
                logger.info(f"Cleaned CSV in place: {input_path}")
                print(f"✓ Cleaned CSV in place: {input_path}")
            else:
                logger.info(f"Cleaned CSV written to {output_path}")
                print(f"✓ Cleaned CSV written to {output_path}")
            sys.exit(0)

    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        sys.exit(2)

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        sys.exit(1)

    except OSError as e:
        logger.error(f"File I/O error: {e}")
        sys.exit(2)

    except Exception as e:
        logger.error(f"Conversion error: {e}")
        sys.exit(3)


if __name__ == "__main__":
    main()

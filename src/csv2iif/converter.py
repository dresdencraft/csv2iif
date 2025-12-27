"""Converter orchestration for csv2iif."""

from csv2iif.csv_reader import CSVReader
from csv2iif.iif_writer import IIFWriter
from csv2iif.logger import setup_logger

logger = setup_logger(__name__)


class Converter:
    """Orchestrates CSV to IIF conversion."""

    def __init__(self, input_path: str, output_path: str) -> None:
        """
        Initialize converter.

        Args:
            input_path: Path to input CSV file
            output_path: Path to output IIF file
        """
        self.input_path = input_path
        self.output_path = output_path
        self.reader = CSVReader(input_path)
        self.writer = IIFWriter(output_path)

    def convert(self) -> None:
        """
        Convert CSV file to IIF format.

        Raises:
            FileNotFoundError: If input file doesn't exist
            ValueError: If CSV data is invalid
            IOError: If output file cannot be written
        """
        logger.info(f"Starting conversion: {self.input_path} -> {self.output_path}")

        transactions = self.reader.read()
        self.writer.write(transactions)

        logger.info("Conversion completed successfully")

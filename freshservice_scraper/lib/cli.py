"""
Command-line interface module for Ticket Analytics.

This module provides the command-line interface for the Ticket Analytics library.
"""
import argparse
import os
import sys
import re
from datetime import datetime
import pendulum
from dateutil import parser

from .api import FreshserviceClient
from .data_handler import TicketDataHandler, TicketProcessor
from .logger import logger


class TicketAnalyticsCLI:
    """Class for handling command-line interface for Ticket Analytics."""

    def __init__(self):
        """Initialize the CLI handler."""
        self.args = None
        self.client = None
        self.data_handler = None
        self.processor = None

    def parse_arguments(self):
        """
        Parse command line arguments.
        
        Returns:
            Parsed arguments
        """
        parser = argparse.ArgumentParser(
            description="Fetch tickets from Freshservice for a range of dates"
        )

        # Date range parameters
        parser.add_argument(
            "--start-date",
            type=str,
            help="Start date in format YYYY-MM-DD, MM/DD/YYYY, DD-MM-YYYY, or Month DD, YYYY",
        )
        parser.add_argument(
            "--end-date",
            type=str,
            help="End date in format YYYY-MM-DD, MM/DD/YYYY, DD-MM-YYYY, or Month DD, YYYY",
        )

        # Interval parameters (alternative to date range)
        parser.add_argument(
            "--interval-size",
            type=str,
            choices=["day", "week", "month", "year"],
            help="Size of each interval (day, week, month, year)",
        )
        parser.add_argument("--interval-n", type=int,
                            help="Number of intervals to process")

        # Output format parameters
        parser.add_argument(
            "--output-format",
            type=str,
            choices=["csv", "json", "excel", "parquet"],
            default="csv",
            help="Output format for the data files (default: csv)",
        )

        # Other parameters
        parser.add_argument(
            "--domain",
            type=str,
            default="schrodinger",
            help="Freshservice domain (without .freshservice.com)",
        )
        parser.add_argument("--api-key", type=str, help="Freshservice API key")
        parser.add_argument(
            "--output-dir",
            type=str,
            default="./data",
            help="Output directory for data files",
        )

        self.args = parser.parse_args()
        return self.args

    def parse_date(self, date_str):
        """
        Parse a date string in multiple formats.
        
        Args:
            date_str: Date string to parse
            
        Returns:
            pendulum.DateTime object
            
        Raises:
            ValueError: If the date string cannot be parsed
        """
        try:
            # First try pendulum's parser
            return pendulum.parse(date_str)
        except ValueError:
            try:
                # Fall back to dateutil's parser which handles more formats
                dt = parser.parse(date_str)
                # Convert to pendulum DateTime
                return pendulum.instance(dt)
            except ValueError:
                raise ValueError(f"Could not parse date: {date_str}")
    
    def validate_arguments(self):
        """
        Validate command line arguments.
        
        Returns:
            True if arguments are valid, False otherwise
        """
        # Get API key from arguments or environment variable
        api_key = self.args.api_key or os.environ.get("freshservice_scraper_KEY")

        if not api_key:
            logger.error(
                "Error: API key is required. Provide it with --api-key or set freshservice_scraper_KEY environment variable."
            )
            return False

        # Determine date ranges to process
        if self.args.start_date and self.args.end_date:
            # Use explicit date range
            try:
                start_date = self.parse_date(self.args.start_date)
                end_date = self.parse_date(self.args.end_date)

                if start_date > end_date:
                    logger.error(
                        "Error: Start date must be before or equal to end date.")
                    return False
            except ValueError as e:
                logger.error(str(e))
                return False
        elif self.args.interval_size and self.args.interval_n:
            # Use interval-based date ranges
            if not self.args.start_date:
                logger.error(
                    "Error: start-date is required when using interval parameters."
                )
                return False

            try:
                self.parse_date(self.args.start_date)
            except ValueError as e:
                logger.error(str(e))
                return False
        else:
            logger.error(
                "Error: Either (start_date AND end_date) OR (interval_size AND interval_n) must be provided."
            )
            return False

        return True

    def initialize_components(self):
        """
        Initialize components needed for processing.
        
        Returns:
            True if initialization is successful, False otherwise
        """
        # Get API key from arguments or environment variable
        api_key = self.args.api_key or os.environ.get("freshservice_scraper_KEY")
        
        # Initialize client
        self.client = FreshserviceClient(self.args.domain, api_key)
        if not self.client.connect():
            return False
            
        # Initialize data handler
        self.data_handler = TicketDataHandler(self.args.output_dir)
        
        # Initialize processor
        self.processor = TicketProcessor(self.client, self.data_handler)
        
        return True

    def get_date_range_for_interval(self, start_date, interval_size, interval_n):
        """
        Generate date ranges for a specific interval.

        Args:
            start_date: Starting date (datetime or pendulum.DateTime)
            interval_size: Size of each interval ('day', 'week', 'month', 'year')
            interval_n: Number of intervals to generate

        Returns:
            List of (start_date, end_date) tuples

        Raises:
            ValueError: If the interval size is invalid
        """
        # Convert to pendulum if it's a standard datetime
        if not isinstance(start_date, pendulum.DateTime):
            start_date = pendulum.instance(start_date)
        
        date_ranges = []
        
        # Handle standard interval sizes
        if interval_size == "day":
            for i in range(interval_n):
                interval_start = start_date.add(days=i)
                interval_end = interval_start.end_of('day')
                date_ranges.append((interval_start, interval_end))
        elif interval_size == "week":
            for i in range(interval_n):
                interval_start = start_date.add(weeks=i)
                interval_end = interval_start.add(days=6).end_of('day')
                date_ranges.append((interval_start, interval_end))
        elif interval_size == "month":
            for i in range(interval_n):
                if i == 0:
                    interval_start = start_date.start_of('month')
                else:
                    interval_start = start_date.add(months=i).start_of('month')
                interval_end = interval_start.end_of('month')
                date_ranges.append((interval_start, interval_end))
        elif interval_size == "year":
            for i in range(interval_n):
                interval_start = start_date.add(years=i)
                interval_end = interval_start.add(years=1).subtract(days=1).end_of('day')
                date_ranges.append((interval_start, interval_end))
        else:
            raise ValueError(f"Invalid interval size: {interval_size}")
        
        return date_ranges

    def determine_date_ranges(self):
        """
        Determine date ranges to process based on arguments.
        
        Returns:
            List of (start_date, end_date) tuples
        """
        date_ranges = []

        if self.args.start_date and self.args.end_date:
            # Use explicit date range
            start_date = self.parse_date(self.args.start_date)
            end_date = self.parse_date(self.args.end_date)
            date_ranges.append((start_date, end_date))
        elif self.args.interval_size and self.args.interval_n:
            # Use interval-based date ranges
            start_date = self.parse_date(self.args.start_date)
            date_ranges = self.get_date_range_for_interval(
                start_date, self.args.interval_size, self.args.interval_n
            )

        return date_ranges

    def run(self):
        """
        Run the CLI application.
        
        Returns:
            0 for success, 1 for failure
        """
        logger.info("Starting Freshservice ticket retrieval using freshpy")

        # Parse arguments
        self.parse_arguments()
        logger.info("Command line arguments: %s", self.args)

        # Validate arguments
        if not self.validate_arguments():
            return 1

        # Initialize components
        if not self.initialize_components():
            return 1

        # Determine date ranges to process
        date_ranges = self.determine_date_ranges()

        # Process each date range
        total_tickets = 0

        for start_date, end_date in date_ranges:
            tickets_count = self.processor.process_date_range(
                start_date,
                end_date,
                self.args.output_format,
            )
            total_tickets += tickets_count

        logger.info(
            "Completed processing %s tickets across all date ranges.", total_tickets
        )
        print(
            f"Completed processing {total_tickets} tickets across all date ranges.")

        return 0


def main():
    """Main entry point for the CLI application."""
    cli = TicketAnalyticsCLI()
    sys.exit(cli.run())


if __name__ == "__main__":
    main()

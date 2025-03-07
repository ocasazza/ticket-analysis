"""
Tests for the cli module.
"""
import unittest
from unittest.mock import patch, MagicMock
import argparse
from datetime import datetime
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.cli import TicketAnalyticsCLI


class TestTicketAnalyticsCLI(unittest.TestCase):
    """Tests for the TicketAnalyticsCLI class."""

    def setUp(self):
        """Set up test fixtures."""
        self.cli = TicketAnalyticsCLI()

    @patch("argparse.ArgumentParser.parse_args")
    def test_parse_arguments(self, mock_parse_args):
        """Test parsing command line arguments."""
        # Configure the mock
        mock_args = MagicMock()
        mock_args.start_date = "2023-01-15"
        mock_args.end_date = "2023-01-31"
        mock_args.output_format = "csv"
        mock_args.domain = "testdomain"
        mock_args.api_key = "testapikey"
        mock_args.output_dir = "./data"
        mock_parse_args.return_value = mock_args

        # Call the method
        args = self.cli.parse_arguments()

        # Assertions
        self.assertEqual(args.start_date, "2023-01-15")
        self.assertEqual(args.end_date, "2023-01-31")
        self.assertEqual(args.output_format, "csv")
        self.assertEqual(args.domain, "testdomain")
        self.assertEqual(args.api_key, "testapikey")
        self.assertEqual(args.output_dir, "./data")

    @patch.dict("os.environ", {"freshservice_scraper_KEY": "env_api_key"})
    def test_validate_arguments_with_env_api_key(self):
        """Test validating arguments with API key from environment variable."""
        # Set up
        self.cli.args = MagicMock()
        self.cli.args.api_key = None
        self.cli.args.start_date = "2023-01-15"
        self.cli.args.end_date = "2023-01-31"
        self.cli.args.interval_size = None
        self.cli.args.interval_n = None

        # Call the method
        result = self.cli.validate_arguments()

        # Assertions
        self.assertTrue(result)

    def test_validate_arguments_no_api_key(self):
        """Test validating arguments with no API key."""
        # Set up
        self.cli.args = MagicMock()
        self.cli.args.api_key = None
        self.cli.args.start_date = "2023-01-15"
        self.cli.args.end_date = "2023-01-31"
        self.cli.args.interval_size = None
        self.cli.args.interval_n = None

        # Call the method with a patch to ensure no environment variable
        with patch.dict("os.environ", {}, clear=True):
            result = self.cli.validate_arguments()

            # Assertions
            self.assertFalse(result)

    @patch("lib.cli.DateParser.parse_date")
    def test_validate_arguments_with_date_range(self, mock_parse_date):
        """Test validating arguments with date range."""
        # Set up
        self.cli.args = MagicMock()
        self.cli.args.api_key = "testapikey"
        self.cli.args.start_date = "2023-01-15"
        self.cli.args.end_date = "2023-01-31"
        self.cli.args.interval_size = None
        self.cli.args.interval_n = None

        # Configure the mock
        mock_parse_date.side_effect = [
            datetime(2023, 1, 15),
            datetime(2023, 1, 31)
        ]

        # Call the method
        result = self.cli.validate_arguments()

        # Assertions
        self.assertTrue(result)
        self.assertEqual(mock_parse_date.call_count, 2)

    @patch("lib.cli.DateParser.parse_date")
    def test_validate_arguments_with_invalid_date_range(self, mock_parse_date):
        """Test validating arguments with invalid date range."""
        # Set up
        self.cli.args = MagicMock()
        self.cli.args.api_key = "testapikey"
        self.cli.args.start_date = "2023-01-31"
        self.cli.args.end_date = "2023-01-15"
        self.cli.args.interval_size = None
        self.cli.args.interval_n = None

        # Configure the mock
        mock_parse_date.side_effect = [
            datetime(2023, 1, 31),
            datetime(2023, 1, 15)
        ]

        # Call the method
        result = self.cli.validate_arguments()

        # Assertions
        self.assertFalse(result)
        self.assertEqual(mock_parse_date.call_count, 2)

    @patch("lib.cli.DateParser.parse_date")
    def test_validate_arguments_with_interval(self, mock_parse_date):
        """Test validating arguments with interval."""
        # Set up
        self.cli.args = MagicMock()
        self.cli.args.api_key = "testapikey"
        self.cli.args.start_date = "2023-01-15"
        self.cli.args.end_date = None
        self.cli.args.interval_size = "month"
        self.cli.args.interval_n = 3

        # Configure the mock
        mock_parse_date.return_value = datetime(2023, 1, 15)

        # Call the method
        result = self.cli.validate_arguments()

        # Assertions
        self.assertTrue(result)
        mock_parse_date.assert_called_once_with("2023-01-15")

    def test_validate_arguments_with_invalid_interval(self):
        """Test validating arguments with invalid interval."""
        # Set up
        self.cli.args = MagicMock()
        self.cli.args.api_key = "testapikey"
        self.cli.args.start_date = None
        self.cli.args.end_date = None
        self.cli.args.interval_size = "month"
        self.cli.args.interval_n = 3

        # Call the method
        result = self.cli.validate_arguments()

        # Assertions
        self.assertFalse(result)

    def test_validate_arguments_with_no_date_range_or_interval(self):
        """Test validating arguments with no date range or interval."""
        # Set up
        self.cli.args = MagicMock()
        self.cli.args.api_key = "testapikey"
        self.cli.args.start_date = None
        self.cli.args.end_date = None
        self.cli.args.interval_size = None
        self.cli.args.interval_n = None

        # Call the method
        result = self.cli.validate_arguments()

        # Assertions
        self.assertFalse(result)

    @patch("lib.cli.FreshserviceClient")
    @patch("lib.cli.TicketDataHandler")
    @patch("lib.cli.TicketProcessor")
    def test_initialize_components_success(self, mock_processor, mock_data_handler, mock_client):
        """Test successful initialization of components."""
        # Set up
        self.cli.args = MagicMock()
        self.cli.args.api_key = "testapikey"
        self.cli.args.domain = "testdomain"
        self.cli.args.output_dir = "./data"

        # Configure the mocks
        mock_client_instance = MagicMock()
        mock_client_instance.connect.return_value = True
        mock_client.return_value = mock_client_instance

        mock_data_handler_instance = MagicMock()
        mock_data_handler.return_value = mock_data_handler_instance

        mock_processor_instance = MagicMock()
        mock_processor.return_value = mock_processor_instance

        # Call the method
        result = self.cli.initialize_components()

        # Assertions
        self.assertTrue(result)
        mock_client.assert_called_once_with("testdomain", "testapikey")
        mock_client_instance.connect.assert_called_once()
        mock_data_handler.assert_called_once_with("./data")
        mock_processor.assert_called_once_with(mock_client_instance, mock_data_handler_instance)

    @patch("lib.cli.FreshserviceClient")
    def test_initialize_components_failure(self, mock_client):
        """Test failed initialization of components."""
        # Set up
        self.cli.args = MagicMock()
        self.cli.args.api_key = "testapikey"
        self.cli.args.domain = "testdomain"
        self.cli.args.output_dir = "./data"

        # Configure the mock
        mock_client_instance = MagicMock()
        mock_client_instance.connect.return_value = False
        mock_client.return_value = mock_client_instance

        # Call the method
        result = self.cli.initialize_components()

        # Assertions
        self.assertFalse(result)
        mock_client.assert_called_once_with("testdomain", "testapikey")
        mock_client_instance.connect.assert_called_once()

    @patch("lib.cli.DateParser.parse_date")
    def test_determine_date_ranges_with_date_range(self, mock_parse_date):
        """Test determining date ranges with explicit date range."""
        # Set up
        self.cli.args = MagicMock()
        self.cli.args.start_date = "2023-01-15"
        self.cli.args.end_date = "2023-01-31"
        self.cli.args.interval_size = None
        self.cli.args.interval_n = None

        # Configure the mock
        start_date = datetime(2023, 1, 15)
        end_date = datetime(2023, 1, 31)
        mock_parse_date.side_effect = [start_date, end_date]

        # Call the method
        date_ranges = self.cli.determine_date_ranges()

        # Assertions
        self.assertEqual(len(date_ranges), 1)
        self.assertEqual(date_ranges[0], (start_date, end_date))
        self.assertEqual(mock_parse_date.call_count, 2)

    @patch("lib.cli.DateParser.parse_date")
    @patch("lib.cli.DateRangeGenerator.get_date_range_for_interval")
    def test_determine_date_ranges_with_interval(self, mock_get_range, mock_parse_date):
        """Test determining date ranges with interval."""
        # Set up
        self.cli.args = MagicMock()
        self.cli.args.start_date = "2023-01-15"
        self.cli.args.end_date = None
        self.cli.args.interval_size = "month"
        self.cli.args.interval_n = 3

        # Configure the mocks
        start_date = datetime(2023, 1, 15)
        mock_parse_date.return_value = start_date
        
        expected_ranges = [
            (datetime(2023, 1, 1), datetime(2023, 1, 31, 23, 59, 59)),
            (datetime(2023, 2, 1), datetime(2023, 2, 28, 23, 59, 59)),
            (datetime(2023, 3, 1), datetime(2023, 3, 31, 23, 59, 59))
        ]
        mock_get_range.return_value = expected_ranges

        # Call the method
        date_ranges = self.cli.determine_date_ranges()

        # Assertions
        self.assertEqual(date_ranges, expected_ranges)
        mock_parse_date.assert_called_once_with("2023-01-15")
        mock_get_range.assert_called_once_with(start_date, "month", 3)

    @patch.object(TicketAnalyticsCLI, "parse_arguments")
    @patch.object(TicketAnalyticsCLI, "validate_arguments")
    @patch.object(TicketAnalyticsCLI, "initialize_components")
    @patch.object(TicketAnalyticsCLI, "determine_date_ranges")
    def test_run_success(self, mock_determine_ranges, mock_initialize, mock_validate, mock_parse):
        """Test successful run of the CLI application."""
        # Set up
        mock_parse.return_value = MagicMock()
        mock_validate.return_value = True
        mock_initialize.return_value = True
        
        date_ranges = [
            (datetime(2023, 1, 1), datetime(2023, 1, 31)),
            (datetime(2023, 2, 1), datetime(2023, 2, 28))
        ]
        mock_determine_ranges.return_value = date_ranges
        
        self.cli.processor = MagicMock()
        self.cli.processor.process_date_range.side_effect = [10, 15]
        
        self.cli.args = MagicMock()
        self.cli.args.output_format = "csv"

        # Call the method
        result = self.cli.run()

        # Assertions
        self.assertEqual(result, 0)  # Success
        mock_parse.assert_called_once()
        mock_validate.assert_called_once()
        mock_initialize.assert_called_once()
        mock_determine_ranges.assert_called_once()
        self.assertEqual(self.cli.processor.process_date_range.call_count, 2)

    @patch.object(TicketAnalyticsCLI, "parse_arguments")
    @patch.object(TicketAnalyticsCLI, "validate_arguments")
    def test_run_validation_failure(self, mock_validate, mock_parse):
        """Test run with validation failure."""
        # Set up
        mock_parse.return_value = MagicMock()
        mock_validate.return_value = False

        # Call the method
        result = self.cli.run()

        # Assertions
        self.assertEqual(result, 1)  # Failure
        mock_parse.assert_called_once()
        mock_validate.assert_called_once()

    @patch.object(TicketAnalyticsCLI, "parse_arguments")
    @patch.object(TicketAnalyticsCLI, "validate_arguments")
    @patch.object(TicketAnalyticsCLI, "initialize_components")
    def test_run_initialization_failure(self, mock_initialize, mock_validate, mock_parse):
        """Test run with initialization failure."""
        # Set up
        mock_parse.return_value = MagicMock()
        mock_validate.return_value = True
        mock_initialize.return_value = False

        # Call the method
        result = self.cli.run()

        # Assertions
        self.assertEqual(result, 1)  # Failure
        mock_parse.assert_called_once()
        mock_validate.assert_called_once()
        mock_initialize.assert_called_once()


if __name__ == "__main__":
    unittest.main()

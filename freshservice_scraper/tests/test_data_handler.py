"""
Tests for the data_handler module.
"""
import os
import sys
import unittest
import tempfile
import shutil
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime
import pandas as pd

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.data_handler import (
    TicketDataHandler, TicketProcessor
)


class TestTicketDataHandler(unittest.TestCase):
    """Tests for the TicketDataHandler class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.data_handler = TicketDataHandler(self.test_dir)
        
        # Sample tickets data
        self.tickets = [
            {"id": 1, "subject": "Test Ticket 1", "status": "Open"},
            {"id": 2, "subject": "Test Ticket 2", "status": "Closed"}
        ]

    def tearDown(self):
        """Tear down test fixtures."""
        # Remove the temporary directory
        shutil.rmtree(self.test_dir)

    @patch("pandas.DataFrame.to_csv")
    def test_save_data_csv(self, mock_to_csv):
        """Test saving data in CSV format."""
        output_file = os.path.join(self.test_dir, "test.csv")
        
        # Call the method
        result = self.data_handler.save_data(self.tickets, output_file, "csv")
        
        # Assertions
        self.assertTrue(result)
        mock_to_csv.assert_called_once_with(output_file, index=False)

    @patch("pandas.DataFrame.to_json")
    def test_save_data_json(self, mock_to_json):
        """Test saving data in JSON format."""
        output_file = os.path.join(self.test_dir, "test.json")
        
        # Call the method
        result = self.data_handler.save_data(self.tickets, output_file, "json")
        
        # Assertions
        self.assertTrue(result)
        mock_to_json.assert_called_once_with(output_file, orient="records", indent=2)

    @patch("pandas.DataFrame.to_excel")
    def test_save_data_excel(self, mock_to_excel):
        """Test saving data in Excel format."""
        output_file = os.path.join(self.test_dir, "test.xlsx")
        
        # Call the method
        result = self.data_handler.save_data(self.tickets, output_file, "excel")
        
        # Assertions
        self.assertTrue(result)
        mock_to_excel.assert_called_once_with(output_file, index=False)

    @patch("pandas.DataFrame.to_parquet")
    def test_save_data_parquet(self, mock_to_parquet):
        """Test saving data in Parquet format."""
        output_file = os.path.join(self.test_dir, "test.parquet")
        
        # Call the method
        result = self.data_handler.save_data(self.tickets, output_file, "parquet")
        
        # Assertions
        self.assertTrue(result)
        mock_to_parquet.assert_called_once_with(output_file, index=False)

    def test_save_data_unsupported_format(self):
        """Test saving data in an unsupported format."""
        output_file = os.path.join(self.test_dir, "test.txt")
        
        # Call the method with a patch to avoid actual file operations
        with patch("pandas.DataFrame.to_csv") as mock_to_csv:
            result = self.data_handler.save_data(self.tickets, output_file, "txt")
            
            # Assertions
            self.assertTrue(result)
            mock_to_csv.assert_called_once_with(output_file, index=False)

    def test_save_data_empty_tickets(self):
        """Test saving empty tickets data."""
        output_file = os.path.join(self.test_dir, "test.csv")
        
        # Call the method
        result = self.data_handler.save_data([], output_file, "csv")
        
        # Assertions
        self.assertFalse(result)

    @patch("pandas.DataFrame.to_csv")
    def test_save_data_error(self, mock_to_csv):
        """Test error handling when saving data."""
        output_file = os.path.join(self.test_dir, "test.csv")
        
        # Configure the mock to raise an exception
        mock_to_csv.side_effect = Exception("Save error")
        
        # Call the method
        result = self.data_handler.save_data(self.tickets, output_file, "csv")
        
        # Assertions
        self.assertFalse(result)

    def test_generate_output_filename_csv(self):
        """Test generating output filename for CSV format."""
        start_date = datetime(2023, 1, 15)
        end_date = datetime(2023, 1, 31)
        
        # Call the method
        filename = self.data_handler.generate_output_filename(start_date, end_date, "csv")
        
        # Assertions
        expected = os.path.join(self.test_dir, "2023-01-15_to_2023-01-31.csv")
        self.assertEqual(filename, expected)

    def test_generate_output_filename_json(self):
        """Test generating output filename for JSON format."""
        start_date = datetime(2023, 1, 15)
        end_date = datetime(2023, 1, 31)
        
        # Call the method
        filename = self.data_handler.generate_output_filename(start_date, end_date, "json")
        
        # Assertions
        expected = os.path.join(self.test_dir, "2023-01-15_to_2023-01-31.json")
        self.assertEqual(filename, expected)

    def test_generate_output_filename_excel(self):
        """Test generating output filename for Excel format."""
        start_date = datetime(2023, 1, 15)
        end_date = datetime(2023, 1, 31)
        
        # Call the method
        filename = self.data_handler.generate_output_filename(start_date, end_date, "excel")
        
        # Assertions
        expected = os.path.join(self.test_dir, "2023-01-15_to_2023-01-31.xlsx")
        self.assertEqual(filename, expected)

    def test_generate_output_filename_parquet(self):
        """Test generating output filename for Parquet format."""
        start_date = datetime(2023, 1, 15)
        end_date = datetime(2023, 1, 31)
        
        # Call the method
        filename = self.data_handler.generate_output_filename(start_date, end_date, "parquet")
        
        # Assertions
        expected = os.path.join(self.test_dir, "2023-01-15_to_2023-01-31.parquet")
        self.assertEqual(filename, expected)

    def test_generate_output_filename_unsupported_format(self):
        """Test generating output filename for an unsupported format."""
        start_date = datetime(2023, 1, 15)
        end_date = datetime(2023, 1, 31)
        
        # Call the method
        filename = self.data_handler.generate_output_filename(start_date, end_date, "txt")
        
        # Assertions
        expected = os.path.join(self.test_dir, "2023-01-15_to_2023-01-31.csv")
        self.assertEqual(filename, expected)


class TestTicketProcessor(unittest.TestCase):
    """Tests for the TicketProcessor class."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = MagicMock()
        self.data_handler = MagicMock()
        self.processor = TicketProcessor(self.client, self.data_handler)
        
        # Sample tickets data
        self.tickets = [
            {"id": 1, "subject": "Test Ticket 1", "status": "Open"},
            {"id": 2, "subject": "Test Ticket 2", "status": "Closed"}
        ]

    def test_process_date_range(self):
        """Test processing a date range."""
        start_date = datetime(2023, 1, 15)
        end_date = datetime(2023, 1, 31)
        output_format = "csv"
        
        # Configure mocks
        self.client.fetch_tickets.return_value = self.tickets
        self.data_handler.generate_output_filename.return_value = "test.csv"
        self.data_handler.save_data.return_value = True
        
        # Call the method
        result = self.processor.process_date_range(start_date, end_date, output_format)
        
        # Assertions
        self.assertEqual(result, 2)  # Number of tickets
        self.client.fetch_tickets.assert_called_once()
        self.data_handler.generate_output_filename.assert_called_once_with(
            start_date, end_date, output_format
        )
        self.data_handler.save_data.assert_called_once_with(
            self.tickets, "test.csv", output_format
        )


if __name__ == "__main__":
    unittest.main()

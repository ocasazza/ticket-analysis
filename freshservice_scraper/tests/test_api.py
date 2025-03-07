"""
Tests for the api module.
"""
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.api import FreshserviceClient


class TestFreshserviceClient(unittest.TestCase):
    """Tests for the FreshserviceClient class."""

    def setUp(self):
        """Set up test fixtures."""
        self.domain = "testdomain"
        self.api_key = "testapikey"
        self.client = FreshserviceClient(self.domain, self.api_key)

    @patch("lib.api.FreshPy")
    def test_connect_success(self, mock_freshpy):
        """Test successful connection to Freshservice API."""
        # Configure the mock
        mock_freshpy.return_value = MagicMock()

        # Call the method
        result = self.client.connect()

        # Assertions
        self.assertTrue(result)
        mock_freshpy.assert_called_once_with(
            domain="testdomain.freshservice.com", api_key=self.api_key
        )
        self.assertIsNotNone(self.client.client)

    @patch("lib.api.FreshPy")
    def test_connect_with_full_domain(self, mock_freshpy):
        """Test connection with full domain name."""
        # Set up
        self.client.domain = "testdomain.freshservice.com"

        # Configure the mock
        mock_freshpy.return_value = MagicMock()

        # Call the method
        result = self.client.connect()

        # Assertions
        self.assertTrue(result)
        mock_freshpy.assert_called_once_with(
            domain="testdomain.freshservice.com", api_key=self.api_key
        )

    @patch("lib.api.FreshPy")
    def test_connect_failure(self, mock_freshpy):
        """Test connection failure to Freshservice API."""
        # Configure the mock to raise an exception
        mock_freshpy.side_effect = Exception("Connection failed")

        # Call the method
        result = self.client.connect()

        # Assertions
        self.assertFalse(result)

    @patch("lib.api.FreshPy")
    def test_fetch_tickets_success_dict_response(self, mock_freshpy):
        """Test successful ticket fetching with dict response."""
        # Set up mock client
        mock_client = MagicMock()
        mock_tickets = MagicMock()
        mock_tickets.get_tickets.return_value = {
            "tickets": [{"id": 1}, {"id": 2}]
        }
        mock_client.tickets = mock_tickets
        mock_freshpy.return_value = mock_client

        # Connect first
        self.client.connect()

        # Call the method
        tickets = self.client.fetch_tickets("2023-01-01T00:00:00Z")

        # Assertions
        self.assertEqual(len(tickets), 2)
        self.assertEqual(tickets[0]["id"], 1)
        self.assertEqual(tickets[1]["id"], 2)
        mock_tickets.get_tickets.assert_called_once_with(
            updated_since="2023-01-01T00:00:00Z"
        )

    @patch("lib.api.FreshPy")
    def test_fetch_tickets_success_single_ticket(self, mock_freshpy):
        """Test successful ticket fetching with single ticket response."""
        # Set up mock client
        mock_client = MagicMock()
        mock_tickets = MagicMock()
        mock_tickets.get_tickets.return_value = {"ticket": {"id": 1}}
        mock_client.tickets = mock_tickets
        mock_freshpy.return_value = mock_client

        # Connect first
        self.client.connect()

        # Call the method
        tickets = self.client.fetch_tickets("2023-01-01T00:00:00Z")

        # Assertions
        self.assertEqual(len(tickets), 1)
        self.assertEqual(tickets[0]["id"], 1)

    @patch("lib.api.FreshPy")
    def test_fetch_tickets_success_list_response(self, mock_freshpy):
        """Test successful ticket fetching with list response."""
        # Set up mock client
        mock_client = MagicMock()
        mock_tickets = MagicMock()
        mock_tickets.get_tickets.return_value = [{"id": 1}, {"id": 2}]
        mock_client.tickets = mock_tickets
        mock_freshpy.return_value = mock_client

        # Connect first
        self.client.connect()

        # Call the method
        tickets = self.client.fetch_tickets("2023-01-01T00:00:00Z")

        # Assertions
        self.assertEqual(len(tickets), 2)
        self.assertEqual(tickets[0]["id"], 1)
        self.assertEqual(tickets[1]["id"], 2)

    @patch("lib.api.FreshPy")
    def test_fetch_tickets_empty_response(self, mock_freshpy):
        """Test ticket fetching with empty response."""
        # Set up mock client
        mock_client = MagicMock()
        mock_tickets = MagicMock()
        mock_tickets.get_tickets.return_value = {}
        mock_client.tickets = mock_tickets
        mock_freshpy.return_value = mock_client

        # Connect first
        self.client.connect()

        # Call the method
        tickets = self.client.fetch_tickets("2023-01-01T00:00:00Z")

        # Assertions
        self.assertEqual(len(tickets), 0)

    @patch("lib.api.FreshPy")
    def test_fetch_tickets_error(self, mock_freshpy):
        """Test ticket fetching with error."""
        # Set up mock client
        mock_client = MagicMock()
        mock_tickets = MagicMock()
        mock_tickets.get_tickets.side_effect = ValueError("API error")
        mock_client.tickets = mock_tickets
        mock_freshpy.return_value = mock_client

        # Connect first
        self.client.connect()

        # Call the method
        tickets = self.client.fetch_tickets("2023-01-01T00:00:00Z")

        # Assertions
        self.assertEqual(len(tickets), 0)

    def test_fetch_tickets_no_connection(self):
        """Test ticket fetching without connection."""
        # Don't connect first
        self.client.client = None

        # Mock the connect method to return False
        self.client.connect = MagicMock(return_value=False)

        # Call the method
        tickets = self.client.fetch_tickets("2023-01-01T00:00:00Z")

        # Assertions
        self.assertEqual(len(tickets), 0)
        self.client.connect.assert_called_once()


if __name__ == "__main__":
    unittest.main()

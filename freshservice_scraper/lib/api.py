"""
API module for Ticket Analytics.

This module provides API interaction functionality for the Ticket Analytics library.
"""
from freshpy import FreshPy
from .logger import logger


class FreshserviceClient:
    """Class for interacting with the Freshservice API."""

    def __init__(self, domain, api_key):
        """
        Initialize the Freshservice client.

        Args:
            domain: Freshservice domain
            api_key: Freshservice API key
        """
        self.domain = domain
        self.api_key = api_key
        self.client = None

    def connect(self):
        """
        Connect to the Freshservice API.

        Returns:
            True if connection is successful, False otherwise
        """
        logger.info("Connecting to Freshservice domain: %s", self.domain)

        try:
            # Make sure domain includes the full freshservice.com part
            if not self.domain.endswith(".freshservice.com"):
                self.domain = f"{self.domain}.freshservice.com"

            # Initialize the FreshPy client
            self.client = FreshPy(domain=self.domain, api_key=self.api_key)
            logger.info("Successfully initialized FreshPy client")
            return True
        except Exception as e:
            logger.error("Error connecting to Freshservice: %s", str(e))
            return False

    def fetch_tickets(self, updated_since):
        """
        Fetch tickets from Freshservice API.

        Args:
            updated_since: Start date for ticket retrieval in API format

        Returns:
            List of ticket dictionaries or empty list if an error occurs
        """
        if not self.client:
            if not self.connect():
                return []

        try:
            logger.info("Using updated_since: %s", updated_since)
            logger.info("Fetching tickets...")

            # Get tickets updated since the start date
            all_tickets_data = self.client.tickets.get_tickets(
                updated_since=updated_since
            )

            logger.info("API response received, type: %s", type(all_tickets_data))

            # Extract the tickets from the response
            all_tickets = []
            if isinstance(all_tickets_data, dict):
                if "tickets" in all_tickets_data:
                    all_tickets = all_tickets_data["tickets"]
                    logger.info("Found %s tickets in response", len(all_tickets))
                elif "ticket" in all_tickets_data:
                    all_tickets = [all_tickets_data["ticket"]]
                    logger.info("Found 1 ticket in response")
                else:
                    logger.warning(
                        "No tickets found in response. Keys: %s",
                        list(all_tickets_data.keys()),
                    )
            elif isinstance(all_tickets_data, list):
                all_tickets = all_tickets_data
                logger.info("Found %s tickets in list response", len(all_tickets))
            else:
                logger.warning("Unexpected response type: %s", type(all_tickets_data))

            logger.info("Total tickets retrieved: %s", len(all_tickets))
            return all_tickets
        except (ValueError, TypeError, KeyError) as e:
            logger.error("Error fetching tickets: %s", str(e))
            return []
        except Exception as e:
            logger.error("Unexpected error fetching tickets: %s", str(e))
            return []

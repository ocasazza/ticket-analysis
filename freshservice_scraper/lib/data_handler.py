"""
Data handler module for Ticket Analytics.

This module provides data handling functionality for the Ticket Analytics library.
"""
import os
import pandas as pd
import pendulum
from .logger import logger


class TicketDataHandler:
    """Class for handling ticket data processing and saving."""

    def __init__(self, output_dir="./data"):
        """
        Initialize the ticket data handler.

        Args:
            output_dir: Directory to save output files
        """
        self.output_dir = output_dir
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)

    def save_data(self, tickets, output_file, output_format="csv"):
        """
        Save tickets to a file in the specified format.

        Args:
            tickets: List of ticket dictionaries
            output_file: Path to the output file
            output_format: Format to save the data in (csv, json, excel, parquet)
            
        Returns:
            True if successful, False otherwise
        """
        if not tickets:
            logger.warning("No tickets to save.")
            print("No tickets to save.")
            return False

        logger.info(
            "Saving %s tickets to %s in %s format", len(
                tickets), output_file, output_format
        )

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        try:
            # Convert tickets to a pandas DataFrame
            df = pd.DataFrame(tickets)

            # Save the data in the specified format
            if output_format == "csv":
                df.to_csv(output_file, index=False)
            elif output_format == "json":
                # Make sure the file has a .json extension
                if not output_file.endswith(".json"):
                    output_file = os.path.splitext(output_file)[0] + ".json"
                df.to_json(output_file, orient="records", indent=2)
            elif output_format == "excel":
                # Make sure the file has a .xlsx extension
                if not output_file.endswith(".xlsx"):
                    output_file = os.path.splitext(output_file)[0] + ".xlsx"
                df.to_excel(output_file, index=False)
            elif output_format == "parquet":
                # Make sure the file has a .parquet extension
                if not output_file.endswith(".parquet"):
                    output_file = os.path.splitext(output_file)[0] + ".parquet"
                df.to_parquet(output_file, index=False)
            else:
                logger.warning(
                    "Unsupported output format: %s. Defaulting to CSV.", output_format
                )
                df.to_csv(output_file, index=False)

            logger.info("Successfully saved tickets to %s", output_file)
            print(f"Saved {len(tickets)} tickets to {output_file}")
            return True
        except Exception as e:
            logger.error("Error saving tickets: %s", str(e))
            return False

    def format_for_filename(self, dt):
        """
        Format a datetime object for use in filenames.
        
        Args:
            dt: datetime or pendulum.DateTime object
            
        Returns:
            Formatted date string (YYYY-MM-DD)
        """
        # Convert to pendulum if it's a standard datetime
        if not isinstance(dt, pendulum.DateTime):
            dt = pendulum.instance(dt)
        return dt.format("YYYY-MM-DD")

    def generate_output_filename(self, start_date, end_date, output_format="csv"):
        """
        Generate an output filename based on date range and format.
        
        Args:
            start_date: Start date for the date range
            end_date: End date for the date range
            output_format: Output format (csv, json, excel, parquet)
            
        Returns:
            Full path to the output file
        """
        # Format dates for filename
        start_str = self.format_for_filename(start_date)
        end_str = self.format_for_filename(end_date)
        
        # Base filename without extension
        base_filename = f"{start_str}_to_{end_str}"

        # Add appropriate extension based on output format
        if output_format == "csv":
            filename = f"{base_filename}.csv"
        elif output_format == "json":
            filename = f"{base_filename}.json"
        elif output_format == "excel":
            filename = f"{base_filename}.xlsx"
        elif output_format == "parquet":
            filename = f"{base_filename}.parquet"
        else:
            filename = f"{base_filename}.csv"

        return os.path.join(self.output_dir, filename)


class TicketProcessor:
    """Class for processing tickets for specific date ranges."""
    
    def __init__(self, client, data_handler):
        """
        Initialize the ticket processor.
        
        Args:
            client: FreshserviceClient instance
            data_handler: TicketDataHandler instance
        """
        self.client = client
        self.data_handler = data_handler
        
    def format_for_api(self, dt):
        """
        Format a datetime object for API requests.
        
        Args:
            dt: datetime or pendulum.DateTime object
            
        Returns:
            Formatted date string (YYYY-MM-DDThh:mm:ssZ)
        """
        # Convert to pendulum if it's a standard datetime
        if not isinstance(dt, pendulum.DateTime):
            dt = pendulum.instance(dt)
        return dt.to_iso8601_string()

    def process_date_range(self, start_date, end_date, output_format="csv"):
        """
        Process tickets for a specific date range.

        Args:
            start_date: Start date for ticket retrieval
            end_date: End date for ticket retrieval
            output_format: Format to save data (csv, json, excel, parquet)

        Returns:
            Number of tickets processed
        """
        # Format start date for API
        start_str = self.format_for_api(start_date)

        logger.info(
            "Processing tickets from %s to %s",
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d"),
        )

        # Fetch tickets
        tickets = self.client.fetch_tickets(start_str)

        # Generate output filename
        output_file = self.data_handler.generate_output_filename(
            start_date, end_date, output_format
        )

        # Save data in the specified format
        self.data_handler.save_data(tickets, output_file, output_format)

        return len(tickets)

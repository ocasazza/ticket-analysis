#!/usr/bin/env python3
"""
Freshservice Ticket Retrieval Script

This script is an entry point for the freshservice_scraper library.
It fetches tickets from Freshservice API for a specified date range or interval.
"""
import os
import sys

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Import the CLI class
from freshservice_scraper.lib.cli import TicketAnalyticsCLI

if __name__ == "__main__":
    cli = TicketAnalyticsCLI()
    sys.exit(cli.run())

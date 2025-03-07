# Freshservice API

A Python library for retrieving and analyzing Freshservice tickets.

## Installation

```bash
# Clone the repository
git clone https://github.com/ocasazza/freshservice-api.git
cd freshservice-api

# Install the package
pip install -e .

# Install development dependencies (including pytest and pytest-cov)
pip install -e ".[dev]"

# Alternatively, you can install from requirements.txt
pip install -r requirements.txt
```

## Usage

### Command Line Interface

The library provides a command-line interface for retrieving tickets:

```bash
# Using explicit date range
python get_tickets.py --start-date "2023-01-01" --end-date "2023-01-31" --domain "schrodinger" --api-key "your-api-key" --output-format json

# Using interval-based date range
python get_tickets.py --start-date "2023-01-01" --interval-size month --interval-n 3 --domain "schrodinger" --api-key "your-api-key" --output-format csv
```

### API Usage

You can also use the library programmatically:

```python
from freshservice_scraper.lib.api import FreshserviceClient
from freshservice_scraper.lib.data_handler import TicketDataHandler, TicketProcessor
from freshservice_scraper.lib.date_utils import DateParser, DateFormatter

# Initialize client
client = FreshserviceClient("schrodinger", "your-api-key")
client.connect()

# Initialize data handler
data_handler = TicketDataHandler("./data")

# Initialize processor
processor = TicketProcessor(client, data_handler)

# Parse dates
start_date = DateParser.parse_date("2023-01-01")
end_date = DateParser.parse_date("2023-01-31")

# Process date range
tickets_count = processor.process_date_range(start_date, end_date, "json")
print(f"Processed {tickets_count} tickets")
```

## Command Line Options

- `--start-date`: Start date in format YYYY-MM-DD, MM/DD/YYYY, DD-MM-YYYY, or Month DD, YYYY
- `--end-date`: End date in format YYYY-MM-DD, MM/DD/YYYY, DD-MM-YYYY, or Month DD, YYYY
- `--interval-size`: Size of each interval (day, week, month, year)
- `--interval-n`: Number of intervals to process
- `--output-format`: Output format for the data files (csv, json, excel, parquet)
- `--domain`: Freshservice domain (without .freshservice.com)
- `--api-key`: Freshservice API key
- `--output-dir`: Output directory for data files

## Environment Variables

- `freshservice_scraper_KEY`: Freshservice API key (alternative to --api-key)

## Testing

The library includes a comprehensive test suite using pytest. To run the tests:

```bash
# Install development dependencies if you haven't already
pip install -e ".[dev]"

# Alternatively, install from requirements.txt
pip install -r requirements.txt

# Run tests with coverage report using the test runner script
./run_tests.py

# Or use pytest directly
pytest

# Run tests for a specific module
./run_tests.py tests/test_date_utils.py
# or
pytest tests/test_date_utils.py

# Run a specific test
./run_tests.py tests/test_date_utils.py::TestDateParser::test_parse_date_iso_format
# or
pytest tests/test_date_utils.py::TestDateParser::test_parse_date_iso_format
```

The test suite includes:

- Unit tests for all modules
- Mocked API interactions
- Test coverage reporting

## Library Structure

```
freshservice_scraper/
├── lib/                     # Main package
│   ├── __init__.py          # Package initialization
│   ├── api.py               # API interaction
│   ├── cli.py               # Command-line interface
│   ├── data_handler.py      # Data handling and saving
│   ├── date_utils.py        # Date utilities
│   └── logger.py            # Logging configuration
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── test_api.py          # Tests for API module
│   ├── test_cli.py          # Tests for CLI module
│   ├── test_data_handler.py # Tests for data handler module
│   └── test_date_utils.py   # Tests for date utilities module
├── get_tickets.py           # Entry point script
├── pytest.ini               # Pytest configuration
├── README.md                # Documentation
├── requirements.txt         # Dependencies
├── run_tests.py             # Test runner script
└── setup.py                 # Package setup file
```

## Classes

- `FreshserviceClient`: Handles API interactions with Freshservice
- `DateParser`: Parses date strings in various formats
- `DateFormatter`: Formats dates for various purposes
- `DateRangeGenerator`: Generates date ranges based on various parameters
- `TicketDataHandler`: Handles saving and processing ticket data
- `TicketProcessor`: Processes tickets for specific date ranges
- `TicketAnalyticsCLI`: Handles command-line interface

## Todo(s) 

- [ ] remove `freshpy` python dependency.

## License

MIT

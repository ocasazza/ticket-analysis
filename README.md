# Ticket Analytics

This project provides tools for analyzing ticket data through both Splunk and JupyterLite. The setup includes proper time-based indexing using the "Created Time" field and automatic field name formatting.

## Prerequisites

- Docker and Docker Compose installed
- Running on a system that can use amd64 platform images (the setup uses platform emulation if needed)
- The ticket CSV data files in the `data/fresh_service_tickets/` directory

## Configuration

The setup includes:

1. A Splunk instance configured to monitor and index the CSV files
2. A custom `ticket_data` index for storing the ticket information
3. Appropriate sourcetype configuration for CSV data

## Usage

1. Set the Splunk password as an environment variable (optional, defaults to 'adminadmin'):
   ```
   export SPLUNK_PASSWORD=your_secure_password
   ```

2. Start the Splunk instance:
   ```
   docker-compose up -d
   ```

3. Access the Splunk web interface:
   - URL: http://localhost:8000
   - Username: admin
   - Password: (the password you set in the environment variable)

4. The ticket data will be automatically imported into the `ticket_data` index
   - You can search the data using queries like: `index=ticket_data`

## Customization

- Edit `docker-compose.yml` to change Splunk settings
- Modify the Splunk configuration files in the `splunk-config/` directory:
  - `inputs.conf`: Controls data input settings
  - `props.conf`: Configures data processing
  - `indexes.conf`: Defines index properties

## JupyterLite for Data Analysis

This project also includes a JupyterLite deployment that lets you analyze ticket data directly in your browser without requiring a Python backend server.

### Features

- Runs entirely in the browser using WebAssembly
- Pre-loaded with common data science libraries (pandas, numpy, matplotlib, seaborn, scikit-learn)
- Sample notebooks for ticket data analysis
- Access to ticket data from the repository

### How to Use JupyterLite

The JupyterLite instance is automatically deployed to GitHub Pages when changes are pushed to the main branch.

1. Visit the GitHub Pages URL for this repository (typically `https://[username].github.io/[repository-name]/`)
2. The JupyterLite interface will load in your browser
3. Open the sample `ticket_analysis.ipynb` notebook to start analyzing ticket data
4. Create new notebooks for your custom analysis

### Local Development

To build and test the JupyterLite deployment locally:

1. Install the required packages:
   ```
   pip install -r jupyter-lite/requirements.txt
   pip install jupyter-lite-lab
   ```

2. Build the JupyterLite site:
   ```
   cd jupyter-lite
   jupyter lite build
   ```

3. Serve the site locally:
   ```
   jupyter lite serve
   ```

4. Open your browser to `http://localhost:8888/` to access the local JupyterLite instance

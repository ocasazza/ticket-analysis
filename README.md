# Ticket Analytics Splunk Setup

This project automatically imports ticket data from CSV files into a Splunk instance for analysis. The setup includes:
- Automatic field name formatting to snake_case (converting "Field Name" to "field_name")
- Configuration to use "created_time" as the timestamp field for events
- A pre-configured dashboard for visualizing ticket data

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

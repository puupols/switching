# Project Name: Switching

## Description:
This project is designed to manage different real-life switches based on the future electricity price and weather forecast. It automates the operation of switches by analyzing cost-effective electricity usage times and weather conditions, aiming to optimize energy consumption and reduce costs.
Adding new switches is straightforward: simply create a new file in the switch_service/switch_statuses directory with the switch's name. This file should define the logic that will be executed when the REST API /status endpoint is called. These files are designed to have access to both electricity price and weather data, enabling dynamic response based on current conditions.


## Structure:
- `src/`: Main source code including application logic and services.
  - `app.py`: Entry point of the application.
  - `switching.conf`: Configuration settings for the application.
  - `electricity_price_service/`: Services for fetching and processing electricity prices.
  - `weather_service/`: Services for fetching and processing weather forecast.
  - `repository_service/`: Services for storing the data.
  - `switch_service/`: Services for getting the switch status by switch name
  - `location_service/`: Services for getting the current location for the weather forecast
  - `job_service/`: Services for planning the background jobs to fetch weather and electricity price data
  - `rest_api/`: REST API service to interface with external systems or switches.
- `tests/`: Contains unit tests for the application modules.

## Installation:
1. Ensure Python 3.8 or newer is installed.
2. Install dependencies: `pip install -r requirements.txt`
3. No specific environment variables are used.

## Usage:
Run the application by running the following script:
python src/app.py


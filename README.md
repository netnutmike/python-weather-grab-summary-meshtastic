# Weather Formatter

A Python command-line application that retrieves weather data from OpenWeatherMap API 3.0 and outputs it in a highly configurable, condensed format. Perfect for integrating weather information into status bars, messaging systems like Meshtastic, or any application requiring compact weather data.

> **Note**: This application uses OpenWeather One Call API 3.0, which requires a subscription. A free tier is available with 1,000 calls/day. See [Getting an OpenWeatherMap API Key](#getting-an-openweathermap-api-key) for setup instructions.

## Features

- **Flexible Output Format**: Customize separators, fields, and output structure
- **YAML Configuration**: Store your preferences in a config file
- **CLI Overrides**: Override any config setting via command-line arguments
- **Custom Icon Mapping**: Map weather conditions to your own icon codes
- **Current Weather & Forecasts**: Get current temperature and hourly forecasts
- **Today or Tomorrow**: Retrieve forecasts for today or tomorrow
- **Extensible Fields**: Access any field from the OpenWeatherMap API response

## Installation

### Prerequisites

- Python 3.8 or higher
- OpenWeatherMap API key (free tier available at https://openweathermap.org/api)

### Install from Source

1. Clone the repository:
```bash
git clone <repository-url>
cd weather-formatter
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install the package:
```bash
pip install -e .
```

### Dependencies

The application requires the following Python packages:
- `requests>=2.31.0` - HTTP client for API calls
- `PyYAML>=6.0.1` - YAML configuration parsing
- `python-dateutil>=2.8.2` - Date/time handling

## Quick Start

1. **Get an API Key**: Sign up for a free API key at https://openweathermap.org/api

2. **Run the application** (this will create a default config file):
```bash
weather-formatter
```

3. **Edit the config file** (`weather_config.yaml`) and add your API key and zipcode:
```yaml
api_key: "your_api_key_here"
zipcode: "10001"
```

4. **Run again** to get weather data:
```bash
weather-formatter
```

### Example Output

With default settings, the output looks like:
```
#76#1pm,9,75,0.0#2pm,9,76,0.0#3pm,9,76,0.0#4pm,9,75,0.0#5pm,9,74,0.0#
```

Format: `#[current_temp]#[hour],[icon],[temp],[precip]#...#`

## Usage

### Command-Line Arguments

```bash
weather-formatter [OPTIONS]
```

#### Location and API Options

**Location** (choose one):
- `-z, --zipcode ZIPCODE` - US ZIP code for weather lookup (5 digits)
- `--latitude LATITUDE` - Latitude in decimal format (-90 to 90)
- `--longitude LONGITUDE` - Longitude in decimal format (-180 to 180)

**API Key:**
- `-k, --api-key API_KEY` - OpenWeatherMap API key

**Note**: Provide either a ZIP code OR both latitude and longitude coordinates, not both.

#### Forecast Options

- `--hours HOURS` - Number of forecast hours to retrieve (default: 5)
- `-d, --day {today,tomorrow}` - Forecast day (default: today)

#### Output Format Options

- `-e, --entry-sep SEPARATOR` - Entry separator character(s) (default: #)
- `-f, --field-sep SEPARATOR` - Field separator character(s) (default: ,)
- `--fields FIELDS` - Comma-separated list of fields to output
- `-p, --preamble TEXT` - Preamble string to prefix output

#### Configuration Options

- `-c, --config PATH` - Path to configuration file (default: weather_config.yaml)
- `-v, --verbose` - Enable verbose logging

#### Help

- `--help` - Display help information

### Examples

#### Basic Usage with CLI Arguments

```bash
# Get weather for a specific ZIP code
weather-formatter -z 10001 -k YOUR_API_KEY

# Get weather using GPS coordinates
weather-formatter --latitude 40.7128 --longitude -74.0060 -k YOUR_API_KEY

# Get 8-hour forecast for tomorrow
weather-formatter --hours 8 --day tomorrow

# Custom separators
weather-formatter --entry-sep "|" --field-sep ":"
```

#### Custom Output Fields

```bash
# Show only hour, icon, and temperature
weather-formatter --fields hour,icon,temp

# Include humidity and wind speed
weather-formatter --fields hour,icon,temp,humidity,wind_speed
```

#### Using a Preamble

```bash
# Add a prefix to the output (replaces the leading #)
weather-formatter --preamble "WEATHER:"
# Output: WEATHER:76#1pm,9,75,0.0#...#

# Or include the # in the preamble if desired
weather-formatter --preamble "WEATHER:#"
# Output: WEATHER:#76#1pm,9,75,0.0#...#
```

#### Using a Custom Config File

```bash
# Use a different config file
weather-formatter --config ~/my_weather_config.yaml
```

## Configuration File

The application uses a YAML configuration file (default: `weather_config.yaml`) to store settings. On first run, a default config file is created with example settings.

### Configuration Structure

```yaml
# Weather API Configuration
api_key: "YOUR_API_KEY_HERE"

# Location (use either zipcode OR coordinates)
zipcode: "10001"
# OR
# latitude: 40.7128
# longitude: -74.0060

# Forecast Settings
forecast_hours: 5
forecast_day: "today"  # today or tomorrow

# Output Format
entry_separator: "#"
field_separator: ","
preamble: ""

# Output Fields (in order)
output_fields:
  - hour
  - icon
  - temp
  - precip

# Weather Condition Icon Mappings
icon_mappings:
  "clear sky": "9"
  "few clouds": "4"
  "scattered clouds": "4"
  "broken clouds": "0"
  "overcast clouds": "0"
  "light rain": "2"
  "moderate rain": "7"
  "heavy intensity rain": "6"
  "thunderstorm": "5"
  "snow": "8"
  "mist": "1"
  "fog": "1"
  "windy": ";"
  "default": "?"
```

### Location Options

The application supports two methods for specifying location:

#### Option 1: US ZIP Code
```yaml
zipcode: "10001"
```
- Simple 5-digit US ZIP code
- Automatically geocoded to coordinates (cached for efficiency)
- Limited to US locations only

#### Option 2: GPS Coordinates (Decimal Format)
```yaml
latitude: 40.7128   # Range: -90 to 90
longitude: -74.0060  # Range: -180 to 180
```
- Works for any location worldwide
- More precise location specification
- Saves one geocoding API call per session
- No ZIP code lookup required

**Important**: Use either ZIP code OR coordinates, not both. The configuration will be rejected if both are provided.

### Available Output Fields

The following fields are available for the `output_fields` configuration:

**Standard Fields:**
- `hour` - Hour in 12-hour format (e.g., "1pm", "2pm")
- `icon` - Weather condition icon code (mapped via icon_mappings)
- `temp` - Temperature (integer)
- `feels_like` - Feels-like temperature (integer)
- `precip` - Precipitation probability (0-100) or amount
- `humidity` - Humidity percentage
- `wind_speed` - Wind speed
- `wind_direction` - Wind direction in degrees
- `pressure` - Atmospheric pressure
- `uv_index` - UV index (if available)
- `visibility` - Visibility distance (if available)
- `dew_point` - Dew point temperature (if available)

**Custom Fields:**
You can also specify any field from the OpenWeatherMap API response using dot notation. For example:
- `clouds.all` - Cloud coverage percentage
- `weather.0.main` - Main weather category

### Icon Mappings

The `icon_mappings` section maps OpenWeatherMap weather condition descriptions to custom icon codes. The default mappings use numeric codes:

- `0` - Cloudy/overcast
- `1` - Foggy/misty
- `2` - Light rain
- `3` - Partially sunny with rain
- `4` - Partly cloudy
- `5` - Thunderstorms
- `6` - Heavy rain
- `7` - Moderate rain
- `8` - Snow
- `9` - Sunny/clear
- `;` - Windy
- `?` - Unknown/default

You can customize these mappings to use any characters or codes you prefer. The matching is case-insensitive and whitespace is stripped.

### CLI Overrides

Command-line arguments always override configuration file settings. This allows you to test different configurations without modifying the config file:

```bash
# Override zipcode from config file
weather-formatter --zipcode 90210

# Override multiple settings
weather-formatter --hours 10 --day tomorrow --entry-sep "|"
```

## Getting an OpenWeatherMap API Key

**IMPORTANT: This application uses OpenWeather One Call API 3.0**

1. Go to https://openweathermap.org/api
2. Sign up for a free account
3. Subscribe to One Call API 3.0 at https://home.openweathermap.org/subscriptions
4. Select the "One Call by Call" subscription (includes a free tier)
5. Navigate to your API keys section
6. Copy your API key
7. Add it to your `weather_config.yaml` file or use the `-k` flag

The free tier includes:
- 1,000 API calls per day
- Current weather data
- Hourly forecasts for up to 48 hours
- Daily forecasts for up to 8 days
- UV index, dew point, and other detailed metrics
- Weather alerts (excluded by default in this app)

### Migration from API 2.5

If you were previously using OpenWeather API 2.5, note the following changes:

- **Subscription Required**: API 3.0 requires a subscription (free tier available)
- **Better Hourly Data**: Hourly forecasts instead of 3-hour intervals
- **More Details**: Additional fields like UV index and dew point are now available
- **Geocoding**: ZIP codes are automatically converted to coordinates (cached for efficiency)
- **No Code Changes**: The application interface remains the same - just update your API key

## Output Format

The output follows this structure:

```
[preamble or entry_sep][current_temp][entry_sep][forecast_1][entry_sep][forecast_2]...[entry_sep]
```

**Note**: The preamble replaces the leading entry separator. If no preamble is configured, output starts with the entry separator.

Each forecast entry contains the configured fields separated by the field separator:

```
[field_1][field_sep][field_2][field_sep]...[field_n]
```

### Example Outputs

**Default Configuration:**
```
#76#1pm,9,75,0.0#2pm,9,76,0.0#3pm,9,76,0.0#4pm,9,75,0.0#5pm,9,74,0.0#
```

**With Preamble "WEATHER:":**
```
WEATHER:76#1pm,9,75,0.0#2pm,9,76,0.0#3pm,9,76,0.0#
```

**With Preamble "WEATHER:#":**
```
WEATHER:#76#1pm,9,75,0.0#2pm,9,76,0.0#3pm,9,76,0.0#
```

**Custom Separators (| and :):**
```
|76|1pm:9:75:0.0|2pm:9:76:0.0|3pm:9:76:0.0|
```

**Custom Fields (hour, icon, temp, humidity, wind_speed):**
```
#76#1pm,9,75,65,5.2#2pm,9,76,63,6.1#3pm,9,76,62,7.3#
```

## Troubleshooting

### "api_key is required" Error

**Problem:** The application cannot find your API key.

**Solution:** 
- Ensure your `weather_config.yaml` file contains a valid `api_key` value
- Or provide the API key via command line: `weather-formatter -k YOUR_API_KEY`

### "Invalid API key" Error

**Problem:** The API key is not recognized by OpenWeatherMap.

**Solution:**
- Verify your API key is correct (copy it from your OpenWeatherMap account)
- New API keys can take a few hours to activate
- Ensure there are no extra spaces or quotes around the key in the config file

### "Invalid zipcode" Error

**Problem:** The zipcode format is incorrect or not found.

**Solution:**
- Ensure the zipcode is a 5-digit US ZIP code
- Verify the zipcode exists and is valid
- Check for typos in the config file or command line

### "Request timed out" Error

**Problem:** Network connection issue or API is slow to respond.

**Solution:**
- Check your internet connection
- Try again in a few moments
- If the problem persists, check OpenWeatherMap's status page

### "API rate limit exceeded" Error

**Problem:** You've exceeded the free tier limit (1,000 calls per day).

**Solution:**
- Wait until the next day for the limit to reset
- Consider upgrading to a paid plan if you need more API calls
- Reduce the frequency of your requests

### Config File Not Found

**Problem:** The application cannot find `weather_config.yaml`.

**Solution:**
- Run the application once to create a default config file
- Ensure you're running the command from the correct directory
- Use the `-c` flag to specify a different config file path

### Empty or Incorrect Output

**Problem:** The output doesn't match expectations.

**Solution:**
- Use the `-v` flag to enable verbose logging and see what's happening
- Check that your `output_fields` configuration includes valid field names
- Verify your icon mappings are correct
- Ensure the API is returning data (check with verbose mode)

## Development

### Running from Source

```bash
# Run the module directly
python -m weather_formatter.cli

# Or use the installed command
weather-formatter
```

### Project Structure

```
weather-formatter/
├── weather_formatter/
│   ├── __init__.py
│   ├── cli.py              # Command-line interface
│   ├── config.py           # Configuration management
│   ├── weather_client.py   # Weather API client
│   ├── formatter.py        # Output formatting logic
│   └── icon_mapper.py      # Weather condition to icon mapping
├── weather_config.yaml     # Configuration file (created on first run)
├── requirements.txt        # Python dependencies
├── setup.py               # Package setup
└── README.md              # This file
```

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]

## Support

For issues, questions, or contributions, please [add contact/repository information here].

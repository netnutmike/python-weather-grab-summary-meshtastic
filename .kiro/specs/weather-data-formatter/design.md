# Design Document

## Overview

The Weather Data Formatter is a Python command-line application that retrieves weather data from a weather service API and outputs it in a highly configurable, condensed format. The application is designed with modularity, configurability, and extensibility as core principles.

### Key Design Goals

- Clean separation between API interaction, configuration management, data formatting, and CLI interface
- Flexible output format supporting any fields available from the weather API
- YAML-based configuration with command-line overrides
- Extensible weather condition icon mapping system
- Minimal dependencies and straightforward installation

### Weather API Selection

The application will use the **OpenWeatherMap API** (https://openweathermap.org/api) for the following reasons:

- Free tier available with sufficient API calls for personal use
- Comprehensive weather data including current conditions and hourly forecasts
- Well-documented API with consistent JSON responses
- Supports location lookup by ZIP code
- Provides detailed weather condition codes that can be mapped to custom icons

API Endpoints to use:
- Current Weather: `https://api.openweathermap.org/data/2.5/weather`
- Hourly Forecast: `https://api.openweathermap.org/data/2.5/forecast` (provides 5-day forecast in 3-hour intervals)

Note: For true hourly forecasts, the One Call API 3.0 endpoint could be used, but it requires a paid subscription. The design will accommodate either endpoint.

## Architecture

### High-Level Architecture

```
┌─────────────────┐
│   CLI Interface │
│   (argparse)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Config Manager  │
│ (YAML + CLI)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Weather Client  │
│ (API calls)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Data Formatter  │
│ (output gen)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Output String  │
└─────────────────┘
```

### Module Structure

```
weather-formatter/
├── weather_formatter/
│   ├── __init__.py
│   ├── cli.py              # Command-line interface
│   ├── config.py           # Configuration management
│   ├── weather_client.py   # Weather API client
│   ├── formatter.py        # Output formatting logic
│   └── icon_mapper.py      # Weather condition to icon mapping
├── weather_config.yaml     # Default configuration file
├── requirements.txt        # Python dependencies
├── setup.py               # Package setup
├── README.md              # Documentation
├── .gitignore            # Git ignore rules
└── examples/             # Example configurations and outputs
    └── example_config.yaml
```

## Components and Interfaces

### 1. CLI Interface (`cli.py`)

**Responsibility:** Parse command-line arguments and orchestrate the application flow

**Key Functions:**
- `main()` - Entry point for the application
- `parse_arguments()` - Parse and validate command-line arguments
- `display_help()` - Show usage information

**Command-line Arguments:**
```
--zipcode, -z          : ZIP code for weather lookup
--config, -c           : Path to config file (default: ./weather_config.yaml)
--hours, -h            : Number of forecast hours (default: 5)
--day, -d              : Forecast day (today/tomorrow, default: today)
--entry-sep, -e        : Entry separator (default: #)
--field-sep, -f        : Field separator (default: ,)
--fields               : Comma-separated list of fields to output
--preamble, -p         : Preamble string to prefix output
--api-key, -k          : Weather API key
--help                 : Display help information
```

**Interface:**
```python
def main() -> int:
    """Main entry point. Returns exit code."""
    
def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
```

### 2. Configuration Manager (`config.py`)

**Responsibility:** Load, validate, and merge configuration from YAML file and CLI arguments

**Key Classes:**
```python
@dataclass
class WeatherConfig:
    """Configuration data structure"""
    zipcode: Optional[str]
    api_key: Optional[str]
    forecast_hours: int = 5
    forecast_day: str = "today"
    entry_separator: str = "#"
    field_separator: str = ","
    output_fields: List[str] = field(default_factory=lambda: ["hour", "icon", "temp", "precip"])
    icon_mappings: Dict[str, str] = field(default_factory=dict)
    preamble: str = ""
    
    def validate(self) -> List[str]:
        """Validate configuration and return list of errors"""
```

**Key Functions:**
```python
def load_config(config_path: str) -> WeatherConfig:
    """Load configuration from YAML file"""
    
def create_default_config(config_path: str) -> None:
    """Create default configuration file"""
    
def merge_config(file_config: WeatherConfig, cli_args: argparse.Namespace) -> WeatherConfig:
    """Merge file config with CLI arguments, CLI takes precedence"""
```

**Default YAML Structure:**
```yaml
# Weather API Configuration
api_key: "YOUR_API_KEY_HERE"
zipcode: "10001"

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
# Maps OpenWeatherMap condition descriptions to custom icons
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
  "partly cloudy": "4"
  "windy": ";"
  "default": "?"
```

### 3. Weather API Client (`weather_client.py`)

**Responsibility:** Interact with OpenWeatherMap API to retrieve weather data

**Key Classes:**
```python
@dataclass
class WeatherData:
    """Structured weather data"""
    timestamp: datetime
    hour: str
    temp: float
    feels_like: float
    condition: str
    condition_code: int
    precip: float
    humidity: int
    wind_speed: float
    wind_direction: int
    pressure: int
    uv_index: Optional[float]
    visibility: Optional[int]
    dew_point: Optional[float]
    raw_data: Dict[str, Any]  # Full API response for extensibility
    
class WeatherClient:
    """Client for OpenWeatherMap API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
        
    def get_current_weather(self, zipcode: str) -> WeatherData:
        """Get current weather for zipcode"""
        
    def get_hourly_forecast(self, zipcode: str, hours: int, day: str) -> List[WeatherData]:
        """Get hourly forecast for specified number of hours and day"""
        
    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make HTTP request to API with error handling"""
```

**Error Handling:**
- Network errors (timeout, connection refused)
- API errors (invalid key, rate limit, invalid zipcode)
- Invalid response format
- All errors should raise custom exceptions with user-friendly messages

### 4. Icon Mapper (`icon_mapper.py`)

**Responsibility:** Map weather conditions from API to custom icon codes

**Key Classes:**
```python
class IconMapper:
    """Maps weather conditions to icon codes"""
    
    def __init__(self, mappings: Dict[str, str]):
        self.mappings = self._normalize_mappings(mappings)
        self.default_icon = mappings.get("default", "?")
        
    def map_condition(self, condition: str) -> str:
        """Map weather condition to icon code"""
        
    def _normalize_mappings(self, mappings: Dict[str, str]) -> Dict[str, str]:
        """Normalize condition strings (lowercase, strip) for matching"""
        
    @staticmethod
    def get_default_mappings() -> Dict[str, str]:
        """Return default icon mappings"""
```

### 5. Data Formatter (`formatter.py`)

**Responsibility:** Format weather data into the configured output string

**Key Classes:**
```python
class WeatherFormatter:
    """Formats weather data into output string"""
    
    def __init__(self, config: WeatherConfig, icon_mapper: IconMapper):
        self.config = config
        self.icon_mapper = icon_mapper
        
    def format_output(self, current_temp: float, forecast: List[WeatherData]) -> str:
        """Format complete output string"""
        
    def _format_entry(self, weather: WeatherData) -> str:
        """Format single forecast entry"""
        
    def _get_field_value(self, weather: WeatherData, field: str) -> str:
        """Extract field value from weather data"""
        
    def _apply_preamble(self, output: str) -> str:
        """Apply preamble to output"""
```

**Field Mapping:**
The formatter will support the following field names:
- `hour` - Hour in 12-hour format (e.g., "1pm", "2pm")
- `icon` - Weather condition icon code
- `temp` - Temperature
- `feels_like` - Feels-like temperature
- `precip` - Precipitation amount
- `humidity` - Humidity percentage
- `wind_speed` - Wind speed
- `wind_direction` - Wind direction in degrees
- `pressure` - Atmospheric pressure
- `uv_index` - UV index
- `visibility` - Visibility distance
- `dew_point` - Dew point temperature
- Any other field name will attempt to extract from `raw_data` using dot notation

## Data Models

### Configuration Data Flow

```
YAML File → WeatherConfig (defaults applied)
                ↓
CLI Arguments → WeatherConfig (overrides applied)
                ↓
        Validated Config
```

### Weather Data Flow

```
API Request → JSON Response → WeatherData objects
                                      ↓
                              Icon Mapping Applied
                                      ↓
                              Field Extraction
                                      ↓
                              Formatted String
```

### Output Format Structure

```
[preamble][entry_sep][current_temp][entry_sep][forecast_1][entry_sep][forecast_2]...[entry_sep]

Where each forecast entry is:
[field_1][field_sep][field_2][field_sep]...[field_n]
```

Example with defaults:
```
#76#1pm,9,75,0.0#2pm,9,76,0.0#3pm,9,76,0.0#4pm,9,75,0.0#5pm,9,74,0.0#
```

## Error Handling

### Error Categories and Handling Strategy

1. **Configuration Errors**
   - Missing required fields (zipcode, API key)
   - Invalid YAML syntax
   - Invalid field names or values
   - Action: Display clear error message, show example config, exit with code 1

2. **API Errors**
   - Invalid API key
   - Invalid zipcode
   - Rate limit exceeded
   - Network timeout
   - Action: Display error message with suggestion, exit with code 2

3. **Data Processing Errors**
   - Unexpected API response format
   - Missing expected fields
   - Action: Log warning, use fallback values where possible, or exit with code 3

4. **File System Errors**
   - Cannot create config file
   - Cannot read config file
   - Action: Display error with permissions info, exit with code 4

### Logging Strategy

- Use Python's `logging` module
- Default log level: WARNING
- Optional `--verbose` flag for DEBUG level
- Log to stderr to keep stdout clean for output
- Log format: `[LEVEL] message`

## Testing Strategy

### Unit Tests

**Config Module Tests:**
- Test YAML parsing with valid and invalid files
- Test default config creation
- Test config merging with CLI overrides
- Test validation logic

**Weather Client Tests:**
- Mock API responses for different scenarios
- Test error handling for various API errors
- Test data parsing and WeatherData creation
- Test timezone handling for tomorrow's forecast

**Icon Mapper Tests:**
- Test condition matching (exact, case-insensitive)
- Test default icon fallback
- Test custom mappings

**Formatter Tests:**
- Test output format with various field combinations
- Test separator customization
- Test preamble application
- Test field extraction including custom fields

### Integration Tests

- End-to-end test with mocked API
- Test complete flow from CLI to output
- Test config file + CLI override scenarios

### Manual Testing Checklist

- Test with real OpenWeatherMap API
- Verify output format matches specification
- Test all CLI arguments
- Test config file modifications
- Test error scenarios (invalid zipcode, no API key, etc.)
- Test tomorrow forecast functionality

## Dependencies

### Required Python Packages

```
requests>=2.31.0      # HTTP client for API calls
PyYAML>=6.0.1         # YAML configuration parsing
python-dateutil>=2.8.2 # Date/time handling
```

### Python Version

- Minimum: Python 3.8
- Recommended: Python 3.10+
- Rationale: Use of dataclasses, type hints, and modern standard library features

## Installation and Setup

### Package Structure

The application will be installable via pip using a `setup.py` file:

```python
from setuptools import setup, find_packages

setup(
    name="weather-formatter",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "PyYAML>=6.0.1",
        "python-dateutil>=2.8.2",
    ],
    entry_points={
        "console_scripts": [
            "weather-formatter=weather_formatter.cli:main",
        ],
    },
    python_requires=">=3.8",
)
```

### Installation Methods

1. **Development Installation:**
   ```bash
   pip install -e .
   ```

2. **Standard Installation:**
   ```bash
   pip install .
   ```

3. **Direct Execution:**
   ```bash
   python -m weather_formatter.cli
   ```

## Security Considerations

1. **API Key Storage:**
   - Config file should not be committed to version control
   - Add `weather_config.yaml` to `.gitignore`
   - Provide `weather_config.yaml.example` as template
   - Support environment variable `OPENWEATHER_API_KEY` as alternative

2. **Input Validation:**
   - Validate zipcode format (5 digits for US)
   - Sanitize all user inputs before API calls
   - Validate separator characters to prevent injection

3. **API Communication:**
   - Use HTTPS for all API calls
   - Implement request timeout (10 seconds)
   - Validate SSL certificates

## Performance Considerations

1. **API Call Optimization:**
   - Single API call for current weather
   - Single API call for forecast data
   - Cache responses for repeated calls within short time window (optional future enhancement)

2. **Response Time:**
   - Target: < 2 seconds for complete execution
   - Most time spent on API calls (network latency)
   - Minimal processing overhead

3. **Resource Usage:**
   - Minimal memory footprint (< 50MB)
   - No persistent storage required
   - Stateless execution

## Future Enhancements

Potential features for future versions:

1. Support for multiple weather APIs (Weather.gov, WeatherAPI, etc.)
2. Caching layer to reduce API calls
3. Support for multiple locations in single call
4. JSON output format option
5. Extended forecast periods (7-day, 14-day)
6. Weather alerts and warnings
7. Historical weather data
8. Configuration profiles for different use cases
9. Plugin system for custom formatters
10. GUI or web interface option

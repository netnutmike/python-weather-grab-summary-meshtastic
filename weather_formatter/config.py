"""Configuration management for Weather Formatter."""

from dataclasses import dataclass, field
from typing import Optional, List, Dict
import yaml
import os


@dataclass
class WeatherConfig:
    """Configuration data structure for Weather Formatter.
    
    Attributes:
        latitude: Latitude coordinate for weather lookup
        longitude: Longitude coordinate for weather lookup
        zipcode: ZIP code for weather lookup (will be converted to lat/lon)
        api_key: OpenWeatherMap API key
        forecast_hours: Number of forecast hours to retrieve (default: 5)
        forecast_day: Day for forecast - 'today' or 'tomorrow' (default: 'today')
        entry_separator: Separator between forecast entries (default: '#')
        field_separator: Separator between fields within an entry (default: ',')
        output_fields: List of fields to include in output
        icon_mappings: Dictionary mapping weather conditions to icon codes
        preamble: Optional prefix string for output (default: '')
    """
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    zipcode: Optional[str] = None
    api_key: Optional[str] = None
    forecast_hours: int = 5
    forecast_day: str = "today"
    entry_separator: str = "#"
    field_separator: str = ","
    output_fields: List[str] = field(default_factory=lambda: ["hour", "icon", "temp", "precip"])
    icon_mappings: Dict[str, str] = field(default_factory=dict)
    preamble: str = ""
    
    def validate(self) -> List[str]:
        """Validate configuration and return list of error messages.
        
        Returns:
            List of error messages. Empty list if configuration is valid.
        """
        errors = []
        
        # Check that either lat/lon or zipcode is provided
        has_coords = self.latitude is not None and self.longitude is not None
        has_zipcode = self.zipcode is not None
        
        if not has_coords and not has_zipcode:
            errors.append("either latitude/longitude or zipcode is required")
        
        # Validate latitude if provided
        if self.latitude is not None:
            if not isinstance(self.latitude, (int, float)) or not (-90 <= self.latitude <= 90):
                errors.append("latitude must be a number between -90 and 90")
        
        # Validate longitude if provided
        if self.longitude is not None:
            if not isinstance(self.longitude, (int, float)) or not (-180 <= self.longitude <= 180):
                errors.append("longitude must be a number between -180 and 180")
        
        # Validate zipcode format if provided
        if self.zipcode is not None:
            if not self.zipcode.isdigit() or len(self.zipcode) != 5:
                errors.append("zipcode must be a 5-digit US ZIP code")
            
        if not self.api_key:
            errors.append("api_key is required")
        
        # Validate forecast_hours
        if not isinstance(self.forecast_hours, int) or self.forecast_hours <= 0:
            errors.append("forecast_hours must be a positive integer")
        
        # Validate forecast_day
        if self.forecast_day not in ["today", "tomorrow"]:
            errors.append("forecast_day must be 'today' or 'tomorrow'")
        
        # Validate output_fields is not empty
        if not self.output_fields or len(self.output_fields) == 0:
            errors.append("output_fields must contain at least one field")
        
        return errors



def load_config(config_path: str = "weather_config.yaml") -> Optional[WeatherConfig]:
    """Load configuration from YAML file.
    
    Reads a YAML configuration file and parses it into a WeatherConfig object.
    If the file doesn't exist, returns None. Applies default values for any
    missing optional fields.
    
    Args:
        config_path: Path to the YAML configuration file (default: 'weather_config.yaml')
    
    Returns:
        WeatherConfig object if file exists and is valid, None if file doesn't exist
        
    Raises:
        yaml.YAMLError: If the YAML file is malformed
        ValueError: If the configuration contains invalid values
        
    Example:
        >>> config = load_config('weather_config.yaml')
        >>> if config:
        ...     print(f"Loaded config for zipcode: {config.zipcode}")
        ... else:
        ...     print("Config file not found")
    """
    # Check if file exists
    if not os.path.exists(config_path):
        return None
    
    try:
        with open(config_path, 'r') as f:
            data = yaml.safe_load(f)
        
        # Handle empty file
        if data is None:
            data = {}
        
        # Extract fields with defaults
        config = WeatherConfig(
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            zipcode=data.get('zipcode'),
            api_key=data.get('api_key'),
            forecast_hours=data.get('forecast_hours', 5),
            forecast_day=data.get('forecast_day', 'today'),
            entry_separator=data.get('entry_separator', '#'),
            field_separator=data.get('field_separator', ','),
            output_fields=data.get('output_fields', ["hour", "icon", "temp", "precip"]),
            icon_mappings=data.get('icon_mappings', {}),
            preamble=data.get('preamble', '')
        )
        
        return config
        
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML configuration file: {e}")
    except Exception as e:
        raise ValueError(f"Error loading configuration: {e}")



def create_default_config(config_path: str = "weather_config.yaml") -> None:
    """Create a default configuration file with example settings.
    
    Generates a comprehensive example configuration file with comments explaining
    all available options. The file includes default icon mappings and example
    values for all configuration fields.
    
    Args:
        config_path: Path where the config file should be created (default: 'weather_config.yaml')
        
    Raises:
        IOError: If the file cannot be created
        
    Example:
        >>> create_default_config('my_weather_config.yaml')
        >>> # Edit the file to add your API key and zipcode
        >>> config = load_config('my_weather_config.yaml')
    """
    default_config = """# Weather Formatter Configuration File
# This file contains all configuration options for the Weather Formatter application

# Weather API Configuration
# Get your API key from: https://openweathermap.org/api
# NOTE: This application uses OpenWeather One Call API 3.0
# The One Call API 3.0 requires a subscription (there is a free tier with 1,000 calls/day)
# Sign up at: https://home.openweathermap.org/subscriptions
api_key: "YOUR_API_KEY_HERE"

# Location Settings
# Provide EITHER zipcode OR latitude/longitude coordinates (not both)

# Option 1: US ZIP code (5 digits)
zipcode: "10001"

# Option 2: GPS Coordinates in decimal format
# Uncomment and use these instead of zipcode if you prefer coordinates
# latitude: 40.7128   # Decimal degrees, range: -90 to 90
# longitude: -74.0060  # Decimal degrees, range: -180 to 180

# Forecast Settings
# Number of hours to forecast (positive integer)
forecast_hours: 5

# Forecast day: "today" or "tomorrow"
forecast_day: "today"

# Output Format Settings
# Character(s) used to separate forecast entries
entry_separator: "#"

# Character(s) used to separate fields within an entry
field_separator: ","

# Optional prefix string added to the beginning of output
preamble: ""

# Output Fields Configuration
# List of fields to include in each forecast entry (in order)
# Available fields: hour, icon, temp, feels_like, precip, humidity, wind_speed,
#                   wind_direction, pressure, uv_index, visibility, dew_point
# You can also specify custom fields from the API response using dot notation
output_fields:
  - hour
  - icon
  - temp
  - precip

# Weather Condition Icon Mappings
# Maps OpenWeatherMap condition descriptions to custom icon codes
# These are case-insensitive and whitespace is stripped
icon_mappings:
  # Clear conditions
  "clear sky": "9"
  
  # Cloudy conditions
  "few clouds": "4"
  "scattered clouds": "4"
  "broken clouds": "0"
  "overcast clouds": "0"
  "partly cloudy": "4"
  
  # Rain conditions
  "light rain": "7"
  "moderate rain": "7"
  "heavy intensity rain": "6"
  "very heavy rain": "6"
  "extreme rain": "6"
  "light intensity drizzle": "7"
  "drizzle": "7"
  "rain": "7"
  
  # Thunderstorm conditions
  "thunderstorm": "5"
  "thunderstorm with light rain": "5"
  "thunderstorm with rain": "5"
  "thunderstorm with heavy rain": "5"
  
  # Snow conditions
  "snow": "8"
  "light snow": "8"
  "heavy snow": "8"
  "sleet": "3"
  
  # Atmospheric conditions
  "mist": "1"
  "fog": "1"
  "haze": "1"
  "smoke": "1"
  
  # Wind conditions
  "windy": ";"
  
  # Default for unknown conditions
  "default": "?"
"""
    
    try:
        with open(config_path, 'w') as f:
            f.write(default_config)
    except IOError as e:
        raise IOError(f"Cannot create configuration file at {config_path}: {e}")




def merge_config(file_config: Optional[WeatherConfig], cli_args) -> WeatherConfig:
    """Merge file configuration with CLI arguments.
    
    Combines configuration from a YAML file with command-line arguments.
    CLI arguments take precedence over file configuration values.
    None values from CLI arguments do not override file config values,
    allowing selective overrides.
    
    Args:
        file_config: Configuration loaded from file (can be None)
        cli_args: Parsed command-line arguments (argparse.Namespace or dict-like object)
    
    Returns:
        Merged WeatherConfig object with CLI overrides applied
        
    Example:
        >>> file_config = load_config('weather_config.yaml')
        >>> args = parse_arguments()  # From cli module
        >>> final_config = merge_config(file_config, args)
        >>> # final_config now has CLI values overriding file values
    """
    # Start with file config or create default
    if file_config is None:
        config = WeatherConfig()
    else:
        # Create a copy to avoid modifying the original
        config = WeatherConfig(
            latitude=file_config.latitude,
            longitude=file_config.longitude,
            zipcode=file_config.zipcode,
            api_key=file_config.api_key,
            forecast_hours=file_config.forecast_hours,
            forecast_day=file_config.forecast_day,
            entry_separator=file_config.entry_separator,
            field_separator=file_config.field_separator,
            output_fields=file_config.output_fields.copy(),
            icon_mappings=file_config.icon_mappings.copy(),
            preamble=file_config.preamble
        )
    
    # Override with CLI arguments if they are not None
    # Handle both argparse.Namespace and dict-like objects
    def get_arg(name, default=None):
        if hasattr(cli_args, name):
            return getattr(cli_args, name, default)
        elif isinstance(cli_args, dict):
            return cli_args.get(name, default)
        return default
    
    latitude = get_arg('latitude')
    if latitude is not None:
        config.latitude = latitude
    
    longitude = get_arg('longitude')
    if longitude is not None:
        config.longitude = longitude
    
    zipcode = get_arg('zipcode')
    if zipcode is not None:
        config.zipcode = zipcode
    
    api_key = get_arg('api_key')
    if api_key is not None:
        config.api_key = api_key
    
    hours = get_arg('hours')
    if hours is not None:
        config.forecast_hours = hours
    
    day = get_arg('day')
    if day is not None:
        config.forecast_day = day
    
    entry_sep = get_arg('entry_sep')
    if entry_sep is not None:
        config.entry_separator = entry_sep
    
    field_sep = get_arg('field_sep')
    if field_sep is not None:
        config.field_separator = field_sep
    
    fields = get_arg('fields')
    if fields is not None:
        # Handle comma-separated string or list
        if isinstance(fields, str):
            config.output_fields = [f.strip() for f in fields.split(',')]
        elif isinstance(fields, list):
            config.output_fields = fields
    
    preamble = get_arg('preamble')
    if preamble is not None:
        config.preamble = preamble
    
    return config

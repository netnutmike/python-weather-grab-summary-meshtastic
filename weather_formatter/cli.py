"""Command-line interface for Weather Formatter.

This module provides the CLI interface and main application flow
for the Weather Formatter application.
"""

import argparse
import sys
import logging
from typing import Optional

from weather_formatter.config import (
    WeatherConfig,
    load_config,
    create_default_config,
    merge_config
)
from weather_formatter.weather_client import WeatherClient, WeatherAPIError
from weather_formatter.icon_mapper import IconMapper
from weather_formatter.formatter import WeatherFormatter


# Configure logging
logging.basicConfig(
    level=logging.WARNING,
    format='[%(levelname)s] %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)


def parse_arguments() -> argparse.Namespace:
    """Parse and return command-line arguments.
    
    Defines all command-line arguments with appropriate defaults,
    help text, and short flags for common options.
    
    Returns:
        argparse.Namespace containing parsed arguments
    """
    parser = argparse.ArgumentParser(
        prog='weather-formatter',
        description='Retrieve and format weather data in a configurable, condensed format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  weather-formatter --lat 40.7128 --lon -74.0060 -k YOUR_API_KEY
  weather-formatter -z 10001 -k YOUR_API_KEY
  weather-formatter --config my_config.yaml --hours 8 --day tomorrow
  weather-formatter -z 90210 --fields hour,icon,temp,humidity
  weather-formatter --preamble "WEATHER:" --entry-sep "|"

Configuration:
  Settings can be specified in a YAML config file (default: weather_config.yaml)
  or via command-line arguments. CLI arguments override config file settings.
  
  Location can be specified using either latitude/longitude or US ZIP code.
  If a ZIP code is provided, it will be automatically converted to coordinates.
  
  If no config file exists, a default one will be created on first run.
        """
    )
    
    # Location and API settings
    parser.add_argument(
        '--lat', '--latitude',
        type=float,
        dest='latitude',
        help='Latitude coordinate for weather lookup'
    )
    
    parser.add_argument(
        '--lon', '--longitude',
        type=float,
        dest='longitude',
        help='Longitude coordinate for weather lookup'
    )
    
    parser.add_argument(
        '-z', '--zipcode',
        type=str,
        help='US ZIP code for weather lookup (5 digits, will be converted to lat/lon)'
    )
    
    parser.add_argument(
        '-k', '--api-key',
        type=str,
        dest='api_key',
        help='OpenWeatherMap API key'
    )
    
    # Configuration file
    parser.add_argument(
        '-c', '--config',
        type=str,
        default='weather_config.yaml',
        help='Path to configuration file (default: weather_config.yaml)'
    )
    
    # Forecast settings
    parser.add_argument(
        '--hours',
        type=int,
        help='Number of forecast hours to retrieve (default: 5)'
    )
    
    parser.add_argument(
        '-d', '--day',
        type=str,
        choices=['today', 'tomorrow'],
        help='Forecast day: today or tomorrow (default: today)'
    )
    
    # Output format settings
    parser.add_argument(
        '-e', '--entry-sep',
        type=str,
        dest='entry_sep',
        help='Entry separator character(s) (default: #)'
    )
    
    parser.add_argument(
        '-f', '--field-sep',
        type=str,
        dest='field_sep',
        help='Field separator character(s) (default: ,)'
    )
    
    parser.add_argument(
        '--fields',
        type=str,
        help='Comma-separated list of fields to output (e.g., hour,icon,temp,precip)'
    )
    
    parser.add_argument(
        '-p', '--preamble',
        type=str,
        help='Preamble string to prefix output'
    )
    
    # Verbose logging
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    return parser.parse_args()



def validate_cli_arguments(args: argparse.Namespace) -> list[str]:
    """Validate command-line arguments and return list of errors.
    
    Performs validation on CLI arguments that can be checked before
    merging with config file. This includes format validation for
    zipcode, latitude, longitude, forecast_day, and forecast_hours.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        List of error messages. Empty list if all arguments are valid.
    """
    errors = []
    
    # Validate latitude if provided
    if args.latitude is not None:
        if not (-90 <= args.latitude <= 90):
            errors.append("latitude must be between -90 and 90")
    
    # Validate longitude if provided
    if args.longitude is not None:
        if not (-180 <= args.longitude <= 180):
            errors.append("longitude must be between -180 and 180")
    
    # Validate zipcode format if provided
    if args.zipcode is not None:
        if not args.zipcode.isdigit() or len(args.zipcode) != 5:
            errors.append("zipcode must be a 5-digit US ZIP code")
    
    # Validate forecast_hours if provided
    if args.hours is not None:
        if args.hours <= 0:
            errors.append("forecast hours must be a positive integer")
    
    # Validate forecast_day if provided (already constrained by choices in argparse)
    # This is redundant but kept for completeness
    if args.day is not None:
        if args.day not in ['today', 'tomorrow']:
            errors.append("forecast day must be 'today' or 'tomorrow'")
    
    return errors



def main() -> int:
    """Main entry point for the Weather Formatter application.
    
    Orchestrates the complete application flow:
    1. Parse command-line arguments
    2. Validate CLI arguments
    3. Load configuration from file
    4. Merge configurations (CLI overrides file)
    5. Validate final configuration
    6. Create default config if none exists
    7. Initialize components (WeatherClient, IconMapper, WeatherFormatter)
    8. Fetch weather data
    9. Format output
    10. Print to stdout
    
    Returns:
        Exit code: 0 for success, non-zero for errors
        - 1: Configuration error
        - 2: API error
        - 3: Data processing error
        - 4: File system error
    """
    # Parse command-line arguments
    args = parse_arguments()
    
    # Set logging level
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled")
    
    # Validate CLI arguments
    cli_errors = validate_cli_arguments(args)
    if cli_errors:
        for error in cli_errors:
            print(f"Error: {error}", file=sys.stderr)
        return 1
    
    # Load configuration from file
    try:
        file_config = load_config(args.config)
        
        # If no config file exists, create a default one
        if file_config is None:
            logger.info(f"No configuration file found at {args.config}")
            try:
                create_default_config(args.config)
                logger.info(f"Created default configuration file: {args.config}")
                print(f"Created default configuration file: {args.config}", file=sys.stderr)
                print(f"Please edit the file to add your API key and zipcode, then run again.", file=sys.stderr)
                return 0
            except IOError as e:
                print(f"Error: Cannot create configuration file: {e}", file=sys.stderr)
                return 4
        
        logger.debug(f"Loaded configuration from {args.config}")
        
    except Exception as e:
        print(f"Error loading configuration: {e}", file=sys.stderr)
        return 1
    
    # Merge file config with CLI arguments
    try:
        config = merge_config(file_config, args)
        logger.debug("Merged configuration with CLI arguments")
    except Exception as e:
        print(f"Error merging configuration: {e}", file=sys.stderr)
        return 1
    
    # Validate final configuration
    validation_errors = config.validate()
    if validation_errors:
        print("Configuration errors:", file=sys.stderr)
        for error in validation_errors:
            print(f"  - {error}", file=sys.stderr)
        print(f"\nPlease check your configuration file ({args.config}) or command-line arguments.", file=sys.stderr)
        return 1
    
    logger.debug(f"Configuration validated successfully")
    
    # Initialize components
    try:
        # Create WeatherClient
        weather_client = WeatherClient(config.api_key)
        logger.debug("Initialized WeatherClient")
        
        # Determine coordinates (either from config or by geocoding zipcode)
        if config.latitude is not None and config.longitude is not None:
            lat, lon = config.latitude, config.longitude
            logger.debug(f"Using coordinates: lat={lat}, lon={lon}")
        elif config.zipcode is not None:
            logger.debug(f"Geocoding zipcode: {config.zipcode}")
            lat, lon = weather_client.geocode_zipcode(config.zipcode)
            logger.debug(f"Geocoded to: lat={lat}, lon={lon}")
        else:
            # This should not happen due to validation, but handle it anyway
            print("Error: No location specified (latitude/longitude or zipcode required)", file=sys.stderr)
            return 1
        
        # Create IconMapper with configured or default mappings
        if config.icon_mappings:
            icon_mapper = IconMapper(config.icon_mappings)
            logger.debug("Initialized IconMapper with custom mappings")
        else:
            icon_mapper = IconMapper(IconMapper.get_default_mappings())
            logger.debug("Initialized IconMapper with default mappings")
        
        # Create WeatherFormatter
        formatter = WeatherFormatter(config, icon_mapper)
        logger.debug("Initialized WeatherFormatter")
        
    except WeatherAPIError as e:
        print(f"Weather API error: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Error initializing components: {e}", file=sys.stderr)
        return 3
    
    # Fetch weather data
    try:
        logger.debug(f"Fetching current weather for lat={lat}, lon={lon}")
        current_weather = weather_client.get_current_weather(lat, lon)
        current_temp = current_weather.temp
        logger.debug(f"Current temperature: {current_temp}°F")
        
        logger.debug(f"Fetching {config.forecast_hours}-hour forecast for {config.forecast_day}")
        forecast = weather_client.get_hourly_forecast(
            lat,
            lon,
            config.forecast_hours,
            config.forecast_day
        )
        logger.debug(f"Retrieved {len(forecast)} forecast entries")
        
    except WeatherAPIError as e:
        print(f"Weather API error: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Error fetching weather data: {e}", file=sys.stderr)
        return 2
    
    # Format output
    try:
        output = formatter.format_output(current_temp, forecast)
        logger.debug(f"Formatted output: {output}")
    except Exception as e:
        print(f"Error formatting output: {e}", file=sys.stderr)
        return 3
    
    # Print output to stdout
    print(output)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

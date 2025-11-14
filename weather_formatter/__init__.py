"""Weather Data Formatter - A configurable weather data retrieval and formatting tool.

This package provides a command-line application for retrieving weather data from
OpenWeatherMap and formatting it into a highly configurable, condensed output format.

The package is organized into the following modules:

- cli: Command-line interface and main application flow
- config: Configuration management (YAML file and CLI argument handling)
- weather_client: Weather API client for OpenWeatherMap
- formatter: Output formatting logic with customizable separators and fields
- icon_mapper: Weather condition to icon code mapping

Basic Usage:
    >>> from weather_formatter.cli import main
    >>> import sys
    >>> sys.exit(main())

Or from the command line:
    $ weather-formatter -z 10001 -k YOUR_API_KEY

For more information, see the README.md file or run:
    $ weather-formatter --help

Attributes:
    __version__ (str): Package version number
    __author__ (str): Package author information
"""

__version__ = "1.0.0"
__author__ = "Weather Formatter Team"

# Public API exports
from weather_formatter.config import WeatherConfig, load_config, create_default_config, merge_config
from weather_formatter.weather_client import WeatherClient, WeatherData, WeatherAPIError
from weather_formatter.icon_mapper import IconMapper
from weather_formatter.formatter import WeatherFormatter

__all__ = [
    'WeatherConfig',
    'load_config',
    'create_default_config',
    'merge_config',
    'WeatherClient',
    'WeatherData',
    'WeatherAPIError',
    'IconMapper',
    'WeatherFormatter',
]

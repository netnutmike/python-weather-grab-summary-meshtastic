#!/usr/bin/env python3
"""Debug script to test formatter output."""

from datetime import datetime
from weather_formatter.formatter import WeatherFormatter
from weather_formatter.config import WeatherConfig
from weather_formatter.icon_mapper import IconMapper
from weather_formatter.weather_client import WeatherData

# Create config with preamble
config = WeatherConfig(
    entry_separator="#",
    field_separator=",",
    output_fields=["hour", "icon", "temp", "precip"],
    preamble="pre"
)

# Create icon mapper
icon_mapper = IconMapper({"clear sky": "9", "default": "?"})

# Create formatter
formatter = WeatherFormatter(config, icon_mapper)

# Create sample weather data
weather1 = WeatherData(
    timestamp=datetime.now(),
    hour="1pm",
    temp=75.0,
    feels_like=73.0,
    condition="clear sky",
    condition_code=800,
    precip=0.0,
    humidity=60,
    wind_speed=5.5,
    wind_direction=180,
    pressure=1013,
    raw_data={}
)

weather2 = WeatherData(
    timestamp=datetime.now(),
    hour="2pm",
    temp=76.0,
    feels_like=74.0,
    condition="clear sky",
    condition_code=800,
    precip=0.0,
    humidity=60,
    wind_speed=5.5,
    wind_direction=180,
    pressure=1013,
    raw_data={}
)

forecast = [weather1, weather2]

# Format output
output = formatter.format_output(74.0, forecast)

print("Output:", repr(output))
print("Visual:", output)
print()
print("Expected: 'pre#74#1pm,9,75,0.0#2pm,9,76,0.0#'")
print("Match:", output == "pre#74#1pm,9,75,0.0#2pm,9,76,0.0#")

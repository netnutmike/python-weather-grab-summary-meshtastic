"""Data formatting module for weather output.

This module provides functionality to format weather data into
configurable output strings with custom separators and field selection.
"""

from typing import List
from weather_formatter.config import WeatherConfig
from weather_formatter.icon_mapper import IconMapper
from weather_formatter.weather_client import WeatherData


class WeatherFormatter:
    """Formats weather data into output string.
    
    The WeatherFormatter takes weather data and configuration to produce
    a formatted output string with configurable separators, fields, and preamble.
    
    Attributes:
        config: WeatherConfig object containing formatting settings
        icon_mapper: IconMapper for converting conditions to icon codes
        
    Example:
        >>> from weather_formatter.config import WeatherConfig
        >>> from weather_formatter.icon_mapper import IconMapper
        >>> 
        >>> config = WeatherConfig(
        ...     entry_separator="#",
        ...     field_separator=",",
        ...     output_fields=["hour", "icon", "temp", "precip"]
        ... )
        >>> icon_mapper = IconMapper(IconMapper.get_default_mappings())
        >>> formatter = WeatherFormatter(config, icon_mapper)
        >>> 
        >>> # Format weather data
        >>> output = formatter.format_output(76, forecast_list)
        >>> print(output)  # #76#1pm,9,75,0.0#2pm,9,76,0.0#...
    """
    
    def __init__(self, config: WeatherConfig, icon_mapper: IconMapper):
        """Initialize WeatherFormatter with configuration and icon mapper.
        
        Args:
            config: WeatherConfig object with separators and output fields
            icon_mapper: IconMapper for weather condition to icon code mapping
        """
        self.config = config
        self.icon_mapper = icon_mapper
    
    def format_output(self, current_temp: float, forecast: List[WeatherData]) -> str:
        """Format complete output string with current temp and forecast.
        
        Creates the full output string following the pattern:
        [preamble][entry_sep][current_temp][entry_sep][forecast_1][entry_sep]...[entry_sep]
        
        Args:
            current_temp: Current temperature value
            forecast: List of WeatherData objects for forecast entries
            
        Returns:
            Formatted output string
            
        Example:
            With defaults (entry_sep="#", field_sep=",", fields=["hour","icon","temp","precip"]):
            "#76#1pm,9,75,0.0#2pm,9,76,0.0#3pm,9,76,0.0#"
        """
        # Start with entry separator
        output_parts = [self.config.entry_separator]
        
        # Add current temperature
        output_parts.append(str(int(current_temp)))
        output_parts.append(self.config.entry_separator)
        
        # Add each forecast entry
        for weather in forecast:
            entry = self._format_entry(weather)
            output_parts.append(entry)
            output_parts.append(self.config.entry_separator)
        
        output = "".join(output_parts)
        
        # Apply preamble if configured
        if self.config.preamble:
            output = self._apply_preamble(output)
        
        return output
    
    def _format_entry(self, weather: WeatherData) -> str:
        """Format single forecast entry with configured fields.
        
        Extracts the configured fields from the WeatherData object and
        joins them with the field separator.
        
        Args:
            weather: WeatherData object to format
            
        Returns:
            Formatted entry string with fields separated by field_separator
            
        Example:
            With field_sep="," and fields=["hour","icon","temp","precip"]:
            "1pm,9,75,0.0"
        """
        field_values = []
        
        for field in self.config.output_fields:
            value = self._get_field_value(weather, field)
            if value is not None:
                field_values.append(value)
        
        return self.config.field_separator.join(field_values)
    
    def _get_field_value(self, weather: WeatherData, field: str) -> str:
        """Extract field value from WeatherData object.
        
        Supports standard field names and custom fields from raw_data.
        Applies special formatting for certain fields:
        - hour: Already in 12-hour format from WeatherData
        - icon: Maps condition through IconMapper
        - temp, feels_like: Rounded to integer
        - precip: Formatted as float with one decimal
        
        Args:
            weather: WeatherData object containing weather information
            field: Field name to extract
            
        Returns:
            String representation of the field value, or None if field not found
        """
        # Standard field mappings
        if field == "hour":
            return weather.hour
        elif field == "icon":
            return self.icon_mapper.map_condition(weather.condition)
        elif field == "temp":
            return str(int(weather.temp))
        elif field == "feels_like":
            return str(int(weather.feels_like))
        elif field == "precip":
            return f"{weather.precip:.1f}"
        elif field == "humidity":
            return str(weather.humidity)
        elif field == "wind_speed":
            return f"{weather.wind_speed:.1f}"
        elif field == "wind_direction":
            return str(weather.wind_direction)
        elif field == "pressure":
            return str(weather.pressure)
        elif field == "uv_index":
            if weather.uv_index is not None:
                return f"{weather.uv_index:.1f}"
            return "N/A"
        elif field == "visibility":
            if weather.visibility is not None:
                return str(weather.visibility)
            return "N/A"
        elif field == "dew_point":
            if weather.dew_point is not None:
                return str(int(weather.dew_point))
            return "N/A"
        else:
            # Try to extract from raw_data for custom fields
            # Support dot notation for nested fields
            try:
                value = weather.raw_data
                for key in field.split('.'):
                    value = value[key]
                return str(value)
            except (KeyError, TypeError):
                # Field not found, skip it
                return None
    
    def _apply_preamble(self, output: str) -> str:
        """Apply preamble prefix to output string.
        
        Adds the configured preamble string to the beginning of the output.
        Handles empty preambles (returns output unchanged) and supports
        multi-character and special character preambles.
        
        Args:
            output: Output string to prefix
            
        Returns:
            Output string with preamble prefix, or unchanged if preamble is empty
            
        Example:
            >>> formatter._apply_preamble("#76#1pm,9,75#")
            "WEATHER:#76#1pm,9,75#"  # if preamble is "WEATHER:"
        """
        if not self.config.preamble:
            return output
        
        return self.config.preamble + output

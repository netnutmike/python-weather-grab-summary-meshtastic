"""Unit tests for formatter module."""

import pytest
from datetime import datetime
from weather_formatter.formatter import WeatherFormatter
from weather_formatter.config import WeatherConfig
from weather_formatter.icon_mapper import IconMapper
from weather_formatter.weather_client import WeatherData


class TestWeatherFormatter:
    """Tests for WeatherFormatter class."""
    
    def create_sample_weather_data(self, hour="1pm", temp=75.0, condition="clear sky", precip=0.0):
        """Helper to create sample WeatherData for testing."""
        return WeatherData(
            timestamp=datetime.now(),
            hour=hour,
            temp=temp,
            feels_like=temp - 2,
            condition=condition,
            condition_code=800,
            precip=precip,
            humidity=60,
            wind_speed=5.5,
            wind_direction=180,
            pressure=1013,
            uv_index=3.5,
            visibility=10000,
            dew_point=55.0,
            raw_data={"test": "data"}
        )
    
    def test_initialization(self):
        """Test WeatherFormatter initializes correctly."""
        config = WeatherConfig()
        icon_mapper = IconMapper(IconMapper.get_default_mappings())
        formatter = WeatherFormatter(config, icon_mapper)
        
        assert formatter.config == config
        assert formatter.icon_mapper == icon_mapper
    
    def test_format_output_basic(self):
        """Test basic output formatting with defaults."""
        config = WeatherConfig(
            entry_separator="#",
            field_separator=",",
            output_fields=["hour", "icon", "temp", "precip"]
        )
        icon_mapper = IconMapper({"clear sky": "9", "default": "?"})
        formatter = WeatherFormatter(config, icon_mapper)
        
        forecast = [
            self.create_sample_weather_data("1pm", 75.0, "clear sky", 0.0),
            self.create_sample_weather_data("2pm", 76.0, "clear sky", 0.0),
            self.create_sample_weather_data("3pm", 77.0, "clear sky", 5.0)
        ]
        
        output = formatter.format_output(74.0, forecast)
        
        # Should be: #74#1pm,9,75,0.0#2pm,9,76,0.0#3pm,9,77,5.0#
        assert output.startswith("#")
        assert output.endswith("#")
        assert "#74#" in output
        assert "1pm,9,75,0.0" in output
        assert "2pm,9,76,0.0" in output
        assert "3pm,9,77,5.0" in output
    
    def test_format_output_custom_separators(self):
        """Test output formatting with custom separators."""
        config = WeatherConfig(
            entry_separator="|",
            field_separator=";",
            output_fields=["hour", "temp"]
        )
        icon_mapper = IconMapper({"default": "?"})
        formatter = WeatherFormatter(config, icon_mapper)
        
        forecast = [
            self.create_sample_weather_data("1pm", 75.0),
            self.create_sample_weather_data("2pm", 76.0)
        ]
        
        output = formatter.format_output(74.0, forecast)
        
        # Should be: |74|1pm;75|2pm;76|
        assert output == "|74|1pm;75|2pm;76|"
    
    def test_format_output_with_preamble(self):
        """Test output formatting with preamble."""
        config = WeatherConfig(
            entry_separator="#",
            field_separator=",",
            output_fields=["hour", "temp"],
            preamble="WEATHER:"
        )
        icon_mapper = IconMapper({"default": "?"})
        formatter = WeatherFormatter(config, icon_mapper)
        
        forecast = [self.create_sample_weather_data("1pm", 75.0)]
        
        output = formatter.format_output(74.0, forecast)
        
        assert output.startswith("WEATHER:")
        assert "#74#" in output
    
    def test_format_output_empty_forecast(self):
        """Test output formatting with empty forecast list."""
        config = WeatherConfig()
        icon_mapper = IconMapper({"default": "?"})
        formatter = WeatherFormatter(config, icon_mapper)
        
        output = formatter.format_output(74.0, [])
        
        # Should be: #74#
        assert output == "#74#"
    
    def test_format_entry_standard_fields(self):
        """Test formatting single entry with standard fields."""
        config = WeatherConfig(
            field_separator=",",
            output_fields=["hour", "icon", "temp", "precip", "humidity"]
        )
        icon_mapper = IconMapper({"clear sky": "9", "default": "?"})
        formatter = WeatherFormatter(config, icon_mapper)
        
        weather = self.create_sample_weather_data("1pm", 75.0, "clear sky", 10.5)
        entry = formatter._format_entry(weather)
        
        assert entry == "1pm,9,75,10.5,60"
    
    def test_get_field_value_hour(self):
        """Test extracting hour field."""
        config = WeatherConfig()
        icon_mapper = IconMapper({"default": "?"})
        formatter = WeatherFormatter(config, icon_mapper)
        
        weather = self.create_sample_weather_data("3pm", 75.0)
        assert formatter._get_field_value(weather, "hour") == "3pm"
    
    def test_get_field_value_icon(self):
        """Test extracting and mapping icon field."""
        config = WeatherConfig()
        icon_mapper = IconMapper({"clear sky": "9", "rain": "2", "default": "?"})
        formatter = WeatherFormatter(config, icon_mapper)
        
        weather = self.create_sample_weather_data(condition="clear sky")
        assert formatter._get_field_value(weather, "icon") == "9"
        
        weather = self.create_sample_weather_data(condition="rain")
        assert formatter._get_field_value(weather, "icon") == "2"
        
        weather = self.create_sample_weather_data(condition="unknown")
        assert formatter._get_field_value(weather, "icon") == "?"
    
    def test_get_field_value_temp(self):
        """Test extracting temperature field (rounded to int)."""
        config = WeatherConfig()
        icon_mapper = IconMapper({"default": "?"})
        formatter = WeatherFormatter(config, icon_mapper)
        
        weather = self.create_sample_weather_data(temp=75.7)
        assert formatter._get_field_value(weather, "temp") == "75"
        
        weather = self.create_sample_weather_data(temp=75.2)
        assert formatter._get_field_value(weather, "temp") == "75"
    
    def test_get_field_value_feels_like(self):
        """Test extracting feels_like field (rounded to int)."""
        config = WeatherConfig()
        icon_mapper = IconMapper({"default": "?"})
        formatter = WeatherFormatter(config, icon_mapper)
        
        weather = WeatherData(
            timestamp=datetime.now(),
            hour="1pm",
            temp=75.0,
            feels_like=73.8,
            condition="clear",
            condition_code=800,
            precip=0.0,
            humidity=60,
            wind_speed=5.0,
            wind_direction=180,
            pressure=1013,
            raw_data={}
        )
        assert formatter._get_field_value(weather, "feels_like") == "73"
    
    def test_get_field_value_precip(self):
        """Test extracting precipitation field (formatted with 1 decimal)."""
        config = WeatherConfig()
        icon_mapper = IconMapper({"default": "?"})
        formatter = WeatherFormatter(config, icon_mapper)
        
        weather = self.create_sample_weather_data(precip=15.67)
        assert formatter._get_field_value(weather, "precip") == "15.7"
        
        weather = self.create_sample_weather_data(precip=0.0)
        assert formatter._get_field_value(weather, "precip") == "0.0"
    
    def test_get_field_value_humidity(self):
        """Test extracting humidity field."""
        config = WeatherConfig()
        icon_mapper = IconMapper({"default": "?"})
        formatter = WeatherFormatter(config, icon_mapper)
        
        weather = self.create_sample_weather_data()
        assert formatter._get_field_value(weather, "humidity") == "60"
    
    def test_get_field_value_wind_speed(self):
        """Test extracting wind speed field (formatted with 1 decimal)."""
        config = WeatherConfig()
        icon_mapper = IconMapper({"default": "?"})
        formatter = WeatherFormatter(config, icon_mapper)
        
        weather = self.create_sample_weather_data()
        assert formatter._get_field_value(weather, "wind_speed") == "5.5"
    
    def test_get_field_value_wind_direction(self):
        """Test extracting wind direction field."""
        config = WeatherConfig()
        icon_mapper = IconMapper({"default": "?"})
        formatter = WeatherFormatter(config, icon_mapper)
        
        weather = self.create_sample_weather_data()
        assert formatter._get_field_value(weather, "wind_direction") == "180"
    
    def test_get_field_value_pressure(self):
        """Test extracting pressure field."""
        config = WeatherConfig()
        icon_mapper = IconMapper({"default": "?"})
        formatter = WeatherFormatter(config, icon_mapper)
        
        weather = self.create_sample_weather_data()
        assert formatter._get_field_value(weather, "pressure") == "1013"
    
    def test_get_field_value_optional_fields(self):
        """Test extracting optional fields (uv_index, visibility, dew_point)."""
        config = WeatherConfig()
        icon_mapper = IconMapper({"default": "?"})
        formatter = WeatherFormatter(config, icon_mapper)
        
        weather = self.create_sample_weather_data()
        assert formatter._get_field_value(weather, "uv_index") == "3.5"
        assert formatter._get_field_value(weather, "visibility") == "10000"
        assert formatter._get_field_value(weather, "dew_point") == "55"
    
    def test_get_field_value_optional_fields_none(self):
        """Test extracting optional fields when they are None."""
        config = WeatherConfig()
        icon_mapper = IconMapper({"default": "?"})
        formatter = WeatherFormatter(config, icon_mapper)
        
        weather = WeatherData(
            timestamp=datetime.now(),
            hour="1pm",
            temp=75.0,
            feels_like=73.0,
            condition="clear",
            condition_code=800,
            precip=0.0,
            humidity=60,
            wind_speed=5.0,
            wind_direction=180,
            pressure=1013,
            uv_index=None,
            visibility=None,
            dew_point=None,
            raw_data={}
        )
        
        assert formatter._get_field_value(weather, "uv_index") == "N/A"
        assert formatter._get_field_value(weather, "visibility") == "N/A"
        assert formatter._get_field_value(weather, "dew_point") == "N/A"
    
    def test_get_field_value_custom_field(self):
        """Test extracting custom field from raw_data."""
        config = WeatherConfig()
        icon_mapper = IconMapper({"default": "?"})
        formatter = WeatherFormatter(config, icon_mapper)
        
        weather = WeatherData(
            timestamp=datetime.now(),
            hour="1pm",
            temp=75.0,
            feels_like=73.0,
            condition="clear",
            condition_code=800,
            precip=0.0,
            humidity=60,
            wind_speed=5.0,
            wind_direction=180,
            pressure=1013,
            raw_data={"custom_field": "custom_value", "nested": {"field": "nested_value"}}
        )
        
        assert formatter._get_field_value(weather, "custom_field") == "custom_value"
        assert formatter._get_field_value(weather, "nested.field") == "nested_value"
    
    def test_get_field_value_nonexistent_field(self):
        """Test extracting nonexistent field returns None."""
        config = WeatherConfig()
        icon_mapper = IconMapper({"default": "?"})
        formatter = WeatherFormatter(config, icon_mapper)
        
        weather = self.create_sample_weather_data()
        assert formatter._get_field_value(weather, "nonexistent") is None
    
    def test_apply_preamble(self):
        """Test applying preamble to output."""
        config = WeatherConfig(preamble="WEATHER:")
        icon_mapper = IconMapper({"default": "?"})
        formatter = WeatherFormatter(config, icon_mapper)
        
        output = "#74#1pm,9,75#"
        result = formatter._apply_preamble(output)
        assert result == "WEATHER:#74#1pm,9,75#"
    
    def test_apply_preamble_empty(self):
        """Test applying empty preamble returns unchanged output."""
        config = WeatherConfig(preamble="")
        icon_mapper = IconMapper({"default": "?"})
        formatter = WeatherFormatter(config, icon_mapper)
        
        output = "#74#1pm,9,75#"
        result = formatter._apply_preamble(output)
        assert result == "#74#1pm,9,75#"
    
    def test_apply_preamble_special_characters(self):
        """Test applying preamble with special characters."""
        config = WeatherConfig(preamble=">>> ")
        icon_mapper = IconMapper({"default": "?"})
        formatter = WeatherFormatter(config, icon_mapper)
        
        output = "#74#"
        result = formatter._apply_preamble(output)
        assert result == ">>> #74#"
    
    def test_format_output_different_field_combinations(self):
        """Test formatting with different field combinations."""
        # Test with minimal fields
        config = WeatherConfig(
            entry_separator="#",
            field_separator=",",
            output_fields=["temp"]
        )
        icon_mapper = IconMapper({"default": "?"})
        formatter = WeatherFormatter(config, icon_mapper)
        
        forecast = [self.create_sample_weather_data("1pm", 75.0)]
        output = formatter.format_output(74.0, forecast)
        assert output == "#74#75#"
        
        # Test with many fields
        config = WeatherConfig(
            entry_separator="#",
            field_separator=",",
            output_fields=["hour", "temp", "humidity", "wind_speed", "pressure"]
        )
        formatter = WeatherFormatter(config, icon_mapper)
        
        forecast = [self.create_sample_weather_data("1pm", 75.0)]
        output = formatter.format_output(74.0, forecast)
        assert "1pm,75,60,5.5,1013" in output

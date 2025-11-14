"""Unit tests for config module."""

import pytest
import tempfile
import os
from weather_formatter.config import (
    WeatherConfig,
    load_config,
    create_default_config,
    merge_config
)


class TestWeatherConfig:
    """Tests for WeatherConfig dataclass."""
    
    def test_default_values(self):
        """Test that default values are set correctly."""
        config = WeatherConfig()
        assert config.zipcode is None
        assert config.api_key is None
        assert config.forecast_hours == 5
        assert config.forecast_day == "today"
        assert config.entry_separator == "#"
        assert config.field_separator == ","
        assert config.output_fields == ["hour", "icon", "temp", "precip"]
        assert config.icon_mappings == {}
        assert config.preamble == ""
    
    def test_validate_valid_config(self):
        """Test validation passes for valid configuration."""
        config = WeatherConfig(
            zipcode="10001",
            api_key="test_key",
            forecast_hours=5,
            forecast_day="today"
        )
        errors = config.validate()
        assert len(errors) == 0
    
    def test_validate_missing_zipcode(self):
        """Test validation fails when zipcode is missing."""
        config = WeatherConfig(api_key="test_key")
        errors = config.validate()
        assert "zipcode is required" in errors
    
    def test_validate_invalid_zipcode_format(self):
        """Test validation fails for invalid zipcode format."""
        config = WeatherConfig(zipcode="123", api_key="test_key")
        errors = config.validate()
        assert any("5-digit" in error for error in errors)
        
        config = WeatherConfig(zipcode="abcde", api_key="test_key")
        errors = config.validate()
        assert any("5-digit" in error for error in errors)
    
    def test_validate_missing_api_key(self):
        """Test validation fails when API key is missing."""
        config = WeatherConfig(zipcode="10001")
        errors = config.validate()
        assert "api_key is required" in errors
    
    def test_validate_invalid_forecast_hours(self):
        """Test validation fails for invalid forecast hours."""
        config = WeatherConfig(zipcode="10001", api_key="test_key", forecast_hours=0)
        errors = config.validate()
        assert any("positive integer" in error for error in errors)
        
        config = WeatherConfig(zipcode="10001", api_key="test_key", forecast_hours=-5)
        errors = config.validate()
        assert any("positive integer" in error for error in errors)
    
    def test_validate_invalid_forecast_day(self):
        """Test validation fails for invalid forecast day."""
        config = WeatherConfig(
            zipcode="10001",
            api_key="test_key",
            forecast_day="next_week"
        )
        errors = config.validate()
        assert any("today" in error and "tomorrow" in error for error in errors)
    
    def test_validate_empty_output_fields(self):
        """Test validation fails when output_fields is empty."""
        config = WeatherConfig(
            zipcode="10001",
            api_key="test_key",
            output_fields=[]
        )
        errors = config.validate()
        assert any("at least one field" in error for error in errors)


class TestLoadConfig:
    """Tests for load_config function."""
    
    def test_load_nonexistent_file(self):
        """Test loading config from nonexistent file returns None."""
        result = load_config("nonexistent_file.yaml")
        assert result is None
    
    def test_load_valid_config(self):
        """Test loading valid YAML configuration."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("""
zipcode: "10001"
api_key: "test_api_key"
forecast_hours: 8
forecast_day: "tomorrow"
entry_separator: "|"
field_separator: ";"
preamble: "WEATHER:"
output_fields:
  - hour
  - temp
  - icon
icon_mappings:
  "clear sky": "9"
  "rain": "2"
""")
            f.flush()
            config_path = f.name
        
        try:
            config = load_config(config_path)
            assert config is not None
            assert config.zipcode == "10001"
            assert config.api_key == "test_api_key"
            assert config.forecast_hours == 8
            assert config.forecast_day == "tomorrow"
            assert config.entry_separator == "|"
            assert config.field_separator == ";"
            assert config.preamble == "WEATHER:"
            assert config.output_fields == ["hour", "temp", "icon"]
            assert config.icon_mappings == {"clear sky": "9", "rain": "2"}
        finally:
            os.unlink(config_path)
    
    def test_load_config_with_defaults(self):
        """Test loading config applies defaults for missing fields."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("""
zipcode: "10001"
api_key: "test_key"
""")
            f.flush()
            config_path = f.name
        
        try:
            config = load_config(config_path)
            assert config.forecast_hours == 5
            assert config.forecast_day == "today"
            assert config.entry_separator == "#"
            assert config.field_separator == ","
            assert config.output_fields == ["hour", "icon", "temp", "precip"]
            assert config.icon_mappings == {}
            assert config.preamble == ""
        finally:
            os.unlink(config_path)
    
    def test_load_empty_config_file(self):
        """Test loading empty YAML file uses all defaults."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("")
            f.flush()
            config_path = f.name
        
        try:
            config = load_config(config_path)
            assert config is not None
            assert config.zipcode is None
            assert config.api_key is None
            assert config.forecast_hours == 5
        finally:
            os.unlink(config_path)
    
    def test_load_malformed_yaml(self):
        """Test loading malformed YAML raises error."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("invalid: yaml: content: [")
            f.flush()
            config_path = f.name
        
        try:
            with pytest.raises(Exception):
                load_config(config_path)
        finally:
            os.unlink(config_path)


class TestCreateDefaultConfig:
    """Tests for create_default_config function."""
    
    def test_create_default_config_file(self):
        """Test creating default configuration file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = os.path.join(tmpdir, "test_config.yaml")
            create_default_config(config_path)
            
            assert os.path.exists(config_path)
            
            # Verify file can be loaded
            config = load_config(config_path)
            assert config is not None
            assert "YOUR_API_KEY_HERE" in config.api_key
            assert config.zipcode == "10001"


class TestMergeConfig:
    """Tests for merge_config function."""
    
    def test_merge_with_none_file_config(self):
        """Test merging when file config is None."""
        cli_args = type('Args', (), {
            'zipcode': '90210',
            'api_key': 'cli_key',
            'hours': 10,
            'day': 'tomorrow',
            'entry_sep': '|',
            'field_sep': ';',
            'fields': 'hour,temp',
            'preamble': 'TEST:'
        })()
        
        config = merge_config(None, cli_args)
        assert config.zipcode == '90210'
        assert config.api_key == 'cli_key'
        assert config.forecast_hours == 10
        assert config.forecast_day == 'tomorrow'
        assert config.entry_separator == '|'
        assert config.field_separator == ';'
        assert config.output_fields == ['hour', 'temp']
        assert config.preamble == 'TEST:'
    
    def test_merge_cli_overrides_file(self):
        """Test CLI arguments override file configuration."""
        file_config = WeatherConfig(
            zipcode="10001",
            api_key="file_key",
            forecast_hours=5,
            forecast_day="today",
            entry_separator="#",
            field_separator=",",
            output_fields=["hour", "icon", "temp"],
            preamble=""
        )
        
        cli_args = type('Args', (), {
            'zipcode': '90210',
            'api_key': None,
            'hours': 8,
            'day': None,
            'entry_sep': '|',
            'field_sep': None,
            'fields': None,
            'preamble': 'WEATHER:'
        })()
        
        config = merge_config(file_config, cli_args)
        assert config.zipcode == '90210'  # Overridden
        assert config.api_key == 'file_key'  # Not overridden (CLI is None)
        assert config.forecast_hours == 8  # Overridden
        assert config.forecast_day == 'today'  # Not overridden
        assert config.entry_separator == '|'  # Overridden
        assert config.field_separator == ','  # Not overridden
        assert config.output_fields == ["hour", "icon", "temp"]  # Not overridden
        assert config.preamble == 'WEATHER:'  # Overridden
    
    def test_merge_with_dict_args(self):
        """Test merging works with dictionary-like CLI args."""
        file_config = WeatherConfig(zipcode="10001", api_key="file_key")
        
        cli_args = {
            'zipcode': '90210',
            'hours': 10
        }
        
        config = merge_config(file_config, cli_args)
        assert config.zipcode == '90210'
        assert config.forecast_hours == 10
        assert config.api_key == 'file_key'
    
    def test_merge_fields_as_string(self):
        """Test merging handles fields as comma-separated string."""
        file_config = WeatherConfig(zipcode="10001", api_key="key")
        
        cli_args = type('Args', (), {
            'zipcode': None,
            'api_key': None,
            'hours': None,
            'day': None,
            'entry_sep': None,
            'field_sep': None,
            'fields': 'hour,temp,humidity',
            'preamble': None
        })()
        
        config = merge_config(file_config, cli_args)
        assert config.output_fields == ['hour', 'temp', 'humidity']
    
    def test_merge_fields_as_list(self):
        """Test merging handles fields as list."""
        file_config = WeatherConfig(zipcode="10001", api_key="key")
        
        cli_args = type('Args', (), {
            'zipcode': None,
            'api_key': None,
            'hours': None,
            'day': None,
            'entry_sep': None,
            'field_sep': None,
            'fields': ['hour', 'temp', 'humidity'],
            'preamble': None
        })()
        
        config = merge_config(file_config, cli_args)
        assert config.output_fields == ['hour', 'temp', 'humidity']

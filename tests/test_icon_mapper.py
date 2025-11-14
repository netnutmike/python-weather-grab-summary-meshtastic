"""Unit tests for icon_mapper module."""

import pytest
from weather_formatter.icon_mapper import IconMapper


class TestIconMapper:
    """Tests for IconMapper class."""
    
    def test_initialization(self):
        """Test IconMapper initializes correctly."""
        mappings = {
            "clear sky": "9",
            "rain": "2",
            "default": "?"
        }
        mapper = IconMapper(mappings)
        
        assert mapper.default_icon == "?"
        assert "clear sky" in mapper.mappings
    
    def test_map_condition_exact_match(self):
        """Test mapping with exact condition match."""
        mappings = {
            "clear sky": "9",
            "rain": "2",
            "default": "?"
        }
        mapper = IconMapper(mappings)
        
        assert mapper.map_condition("clear sky") == "9"
        assert mapper.map_condition("rain") == "2"
    
    def test_map_condition_case_insensitive(self):
        """Test mapping is case-insensitive."""
        mappings = {
            "clear sky": "9",
            "rain": "2",
            "default": "?"
        }
        mapper = IconMapper(mappings)
        
        assert mapper.map_condition("Clear Sky") == "9"
        assert mapper.map_condition("CLEAR SKY") == "9"
        assert mapper.map_condition("clear SKY") == "9"
        assert mapper.map_condition("RAIN") == "2"
    
    def test_map_condition_strips_whitespace(self):
        """Test mapping strips leading/trailing whitespace."""
        mappings = {
            "clear sky": "9",
            "default": "?"
        }
        mapper = IconMapper(mappings)
        
        assert mapper.map_condition("  clear sky  ") == "9"
        assert mapper.map_condition("\tclear sky\n") == "9"
    
    def test_map_condition_unknown_returns_default(self):
        """Test unknown condition returns default icon."""
        mappings = {
            "clear sky": "9",
            "default": "?"
        }
        mapper = IconMapper(mappings)
        
        assert mapper.map_condition("unknown condition") == "?"
        assert mapper.map_condition("tornado") == "?"
    
    def test_map_condition_no_default_specified(self):
        """Test behavior when no default is specified."""
        mappings = {
            "clear sky": "9",
            "rain": "2"
        }
        mapper = IconMapper(mappings)
        
        # Should use "?" as fallback default
        assert mapper.map_condition("unknown") == "?"
    
    def test_normalize_mappings(self):
        """Test that mappings are normalized during initialization."""
        mappings = {
            "Clear Sky": "9",
            "  RAIN  ": "2",
            "Snow\t": "8",
            "default": "?"
        }
        mapper = IconMapper(mappings)
        
        # All keys should be normalized
        assert "clear sky" in mapper.mappings
        assert "rain" in mapper.mappings
        assert "snow" in mapper.mappings
        
        # Original keys should not exist
        assert "Clear Sky" not in mapper.mappings
        assert "  RAIN  " not in mapper.mappings
    
    def test_get_default_mappings(self):
        """Test default mappings are comprehensive."""
        mappings = IconMapper.get_default_mappings()
        
        # Check key conditions are present
        assert "clear sky" in mappings
        assert "rain" in mappings
        assert "snow" in mappings
        assert "thunderstorm" in mappings
        assert "fog" in mappings
        assert "default" in mappings
        
        # Check icon codes
        assert mappings["clear sky"] == "9"
        assert mappings["snow"] == "8"
        assert mappings["thunderstorm"] == "5"
        assert mappings["default"] == "?"
    
    def test_default_mappings_coverage(self):
        """Test default mappings cover common OpenWeatherMap conditions."""
        mappings = IconMapper.get_default_mappings()
        mapper = IconMapper(mappings)
        
        # Test various common conditions
        assert mapper.map_condition("clear sky") == "9"
        assert mapper.map_condition("few clouds") == "4"
        assert mapper.map_condition("scattered clouds") == "4"
        assert mapper.map_condition("broken clouds") == "0"
        assert mapper.map_condition("overcast clouds") == "0"
        assert mapper.map_condition("light rain") == "2"
        assert mapper.map_condition("moderate rain") == "7"
        assert mapper.map_condition("heavy rain") == "6"
        assert mapper.map_condition("thunderstorm") == "5"
        assert mapper.map_condition("snow") == "8"
        assert mapper.map_condition("mist") == "1"
        assert mapper.map_condition("fog") == "1"
    
    def test_custom_icon_codes(self):
        """Test using custom icon codes."""
        mappings = {
            "clear sky": "☀️",
            "rain": "🌧️",
            "snow": "❄️",
            "default": "❓"
        }
        mapper = IconMapper(mappings)
        
        assert mapper.map_condition("clear sky") == "☀️"
        assert mapper.map_condition("rain") == "🌧️"
        assert mapper.map_condition("snow") == "❄️"
        assert mapper.map_condition("unknown") == "❓"
    
    def test_empty_mappings(self):
        """Test behavior with empty mappings."""
        mapper = IconMapper({})
        
        # Should use default fallback
        assert mapper.map_condition("any condition") == "?"

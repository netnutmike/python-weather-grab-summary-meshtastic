"""
Icon mapping module for weather conditions.

This module provides functionality to map weather condition strings
from the Weather API to custom icon codes.
"""

from typing import Dict


class IconMapper:
    """Maps weather conditions to icon codes.
    
    The IconMapper handles mapping weather condition descriptions from the
    Weather API to custom icon codes. It supports case-insensitive matching
    and provides a default icon for unmapped conditions.
    
    Attributes:
        mappings: Dictionary of normalized condition strings to icon codes
        default_icon: Icon code to use for unmapped conditions
        
    Example:
        >>> # Use default mappings
        >>> mapper = IconMapper(IconMapper.get_default_mappings())
        >>> icon = mapper.map_condition("Clear Sky")
        >>> print(icon)  # "9"
        >>> 
        >>> # Use custom mappings
        >>> custom_mappings = {
        ...     "clear sky": "☀️",
        ...     "rain": "🌧️",
        ...     "default": "❓"
        ... }
        >>> mapper = IconMapper(custom_mappings)
        >>> icon = mapper.map_condition("rain")
        >>> print(icon)  # "🌧️"
    """
    
    def __init__(self, mappings: Dict[str, str]):
        """Initialize IconMapper with custom mappings.
        
        The mappings are normalized (lowercased and stripped) for case-insensitive
        matching. The "default" key is used for conditions that don't match any
        mapping.
        
        Args:
            mappings: Dictionary mapping weather condition strings to icon codes.
                     Should include a "default" key for unmapped conditions.
        """
        self.mappings = self._normalize_mappings(mappings)
        self.default_icon = mappings.get("default", "?")
    
    def map_condition(self, condition: str) -> str:
        """Map weather condition to icon code.
        
        Performs case-insensitive lookup of the condition string in the
        configured mappings. Returns the default icon if no mapping is found.
        
        Args:
            condition: Weather condition string from the API
            
        Returns:
            Icon code string corresponding to the condition
            
        Example:
            >>> mapper = IconMapper({"clear sky": "9", "default": "?"})
            >>> mapper.map_condition("Clear Sky")
            '9'
            >>> mapper.map_condition("unknown condition")
            '?'
        """
        normalized_condition = condition.lower().strip()
        return self.mappings.get(normalized_condition, self.default_icon)
    
    def _normalize_mappings(self, mappings: Dict[str, str]) -> Dict[str, str]:
        """Normalize condition strings for case-insensitive matching.
        
        Converts all mapping keys to lowercase and strips whitespace to enable
        case-insensitive and whitespace-tolerant condition matching.
        
        Args:
            mappings: Original mappings dictionary
            
        Returns:
            New dictionary with normalized keys
        """
        return {key.lower().strip(): value for key, value in mappings.items()}
    
    @staticmethod
    def get_default_mappings() -> Dict[str, str]:
        """Return default icon mappings for common weather conditions.
        
        Provides default mappings for common OpenWeatherMap condition descriptions
        to icon codes:
        - 0: cloudy
        - 1: foggy/misty
        - 2: light rain
        - 3: partially sunny and raining
        - 4: partly cloudy
        - 5: thunderstorms
        - 6: heavy rain
        - 7: moderate rain
        - 8: snowing
        - 9: sunny/clear
        - ;: windy
        - ?: unknown/default
        
        Returns:
            Dictionary mapping condition strings to icon codes
        """
        return {
            # Clear conditions
            "clear sky": "9",
            "clear": "9",
            "sunny": "9",
            
            # Cloudy conditions
            "few clouds": "4",
            "scattered clouds": "4",
            "partly cloudy": "4",
            "broken clouds": "0",
            "overcast clouds": "0",
            "overcast": "0",
            "cloudy": "0",
            
            # Rain conditions
            "light rain": "7",
            "light intensity rain": "7",
            "drizzle": "7",
            "light intensity drizzle": "7",
            "moderate rain": "7",
            "heavy intensity rain": "6",
            "heavy rain": "6",
            "very heavy rain": "6",
            "extreme rain": "6",
            "rain": "7",
            
            # Partially sunny with rain
            "light intensity shower rain": "7",
            "shower rain": "7",
            
            # Thunderstorm conditions
            "thunderstorm": "5",
            "thunderstorm with light rain": "5",
            "thunderstorm with rain": "5",
            "thunderstorm with heavy rain": "5",
            "light thunderstorm": "5",
            "heavy thunderstorm": "5",
            "ragged thunderstorm": "5",
            
            # Snow conditions
            "snow": "8",
            "light snow": "8",
            "heavy snow": "8",
            "sleet": "3",
            "light shower sleet": "3",
            "shower sleet": "3",
            "light rain and snow": "3",
            "rain and snow": "3",
            "light shower snow": "2",
            "shower snow": "2",
            "heavy shower snow": "8",
            
            # Fog/Mist conditions
            "mist": "1",
            "fog": "1",
            "haze": "1",
            "smoke": "1",
            "dust": "1",
            "sand": "1",
            
            # Windy conditions
            "windy": ";",
            "squalls": ";",
            "tornado": "<",
            
            # Default for unknown conditions
            "default": "?"
        }

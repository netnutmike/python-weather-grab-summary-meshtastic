"""Weather API client for retrieving weather data from OpenWeatherMap."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError


@dataclass
class WeatherData:
    """Structured weather data from API response.
    
    Attributes:
        timestamp: DateTime of the weather data point
        hour: Hour in 12-hour format (e.g., "1pm", "2pm")
        temp: Temperature in configured units
        feels_like: Feels-like temperature
        condition: Weather condition description
        condition_code: Numeric weather condition code
        precip: Precipitation probability (0-100) or amount
        humidity: Humidity percentage
        wind_speed: Wind speed
        wind_direction: Wind direction in degrees
        pressure: Atmospheric pressure
        uv_index: UV index (optional)
        visibility: Visibility distance (optional)
        dew_point: Dew point temperature (optional)
        raw_data: Complete API response for extensibility
    """
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
    uv_index: Optional[float] = None
    visibility: Optional[int] = None
    dew_point: Optional[float] = None
    raw_data: Dict[str, Any] = field(default_factory=dict)



class WeatherAPIError(Exception):
    """Custom exception for Weather API errors."""
    pass


class WeatherClient:
    """Client for OpenWeatherMap API.
    
    Handles API requests for current weather and hourly forecasts.
    Provides error handling for network issues and API errors.
    
    Example:
        >>> client = WeatherClient(api_key="your_api_key")
        >>> current = client.get_current_weather("10001")
        >>> print(f"Current temp: {current.temp}°F")
        >>> forecast = client.get_hourly_forecast("10001", hours=5, day="today")
        >>> for entry in forecast:
        ...     print(f"{entry.hour}: {entry.temp}°F, {entry.condition}")
    """
    
    def __init__(self, api_key: str):
        """Initialize WeatherClient with API key.
        
        Sets up the HTTP session with a 10-second timeout for all requests.
        
        Args:
            api_key: OpenWeatherMap API key
        """
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.session = requests.Session()
        self.session.timeout = 10

    
    def get_current_weather(self, zipcode: str) -> WeatherData:
        """Get current weather for a zipcode.
        
        Retrieves current weather conditions including temperature, feels-like
        temperature, weather condition, humidity, wind, and pressure.
        
        Args:
            zipcode: US ZIP code (5 digits)
            
        Returns:
            WeatherData object with current weather information
            
        Raises:
            WeatherAPIError: If API request fails or returns invalid data
            
        Example:
            >>> client = WeatherClient("your_api_key")
            >>> weather = client.get_current_weather("10001")
            >>> print(f"Temperature: {weather.temp}°F")
            >>> print(f"Condition: {weather.condition}")
        """
        endpoint = f"{self.base_url}/weather"
        params = {
            "zip": f"{zipcode},US",
            "appid": self.api_key,
            "units": "imperial"
        }
        
        data = self._make_request(endpoint, params)
        
        # Parse response into WeatherData
        dt = datetime.fromtimestamp(data["dt"])
        hour_12 = dt.strftime("%-I%p").lower()
        
        weather_info = data["weather"][0] if data.get("weather") else {}
        main_info = data.get("main", {})
        wind_info = data.get("wind", {})
        
        return WeatherData(
            timestamp=dt,
            hour=hour_12,
            temp=main_info.get("temp", 0.0),
            feels_like=main_info.get("feels_like", 0.0),
            condition=weather_info.get("description", "unknown"),
            condition_code=weather_info.get("id", 0),
            precip=data.get("rain", {}).get("1h", 0.0) + data.get("snow", {}).get("1h", 0.0),
            humidity=main_info.get("humidity", 0),
            wind_speed=wind_info.get("speed", 0.0),
            wind_direction=wind_info.get("deg", 0),
            pressure=main_info.get("pressure", 0),
            visibility=data.get("visibility"),
            raw_data=data
        )

    
    def get_hourly_forecast(self, zipcode: str, hours: int, day: str = "today") -> List[WeatherData]:
        """Get hourly forecast for a zipcode.
        
        Retrieves forecast data for the specified number of hours. The forecast
        can be filtered to show only today's or tomorrow's data. Note that
        OpenWeatherMap provides forecasts in 3-hour intervals, so the actual
        number of entries may vary slightly.
        
        Args:
            zipcode: US ZIP code (5 digits)
            hours: Number of forecast hours to retrieve
            day: "today" or "tomorrow" to filter forecast data (default: "today")
            
        Returns:
            List of WeatherData objects for the forecast period
            
        Raises:
            WeatherAPIError: If API request fails or returns invalid data
            
        Example:
            >>> client = WeatherClient("your_api_key")
            >>> forecast = client.get_hourly_forecast("10001", hours=8, day="tomorrow")
            >>> for entry in forecast:
            ...     print(f"{entry.hour}: {entry.temp}°F, {entry.precip}% chance of rain")
        """
        endpoint = f"{self.base_url}/forecast"
        params = {
            "zip": f"{zipcode},US",
            "appid": self.api_key,
            "units": "imperial"
        }
        
        data = self._make_request(endpoint, params)
        
        forecast_list = []
        now = datetime.now()
        
        # Determine target date based on day parameter
        if day.lower() == "tomorrow":
            target_date = now.date().replace(day=now.day + 1)
        else:
            target_date = now.date()
        
        # Parse forecast entries
        for item in data.get("list", []):
            dt = datetime.fromtimestamp(item["dt"])
            
            # Filter by target date
            if dt.date() != target_date:
                continue
            
            # Stop when we have enough hours
            if len(forecast_list) >= hours:
                break
            
            hour_12 = dt.strftime("%-I%p").lower()
            weather_info = item["weather"][0] if item.get("weather") else {}
            main_info = item.get("main", {})
            wind_info = item.get("wind", {})
            
            # Calculate precipitation probability
            precip_prob = item.get("pop", 0.0) * 100  # Convert to percentage
            
            weather_data = WeatherData(
                timestamp=dt,
                hour=hour_12,
                temp=main_info.get("temp", 0.0),
                feels_like=main_info.get("feels_like", 0.0),
                condition=weather_info.get("description", "unknown"),
                condition_code=weather_info.get("id", 0),
                precip=precip_prob,
                humidity=main_info.get("humidity", 0),
                wind_speed=wind_info.get("speed", 0.0),
                wind_direction=wind_info.get("deg", 0),
                pressure=main_info.get("pressure", 0),
                visibility=item.get("visibility"),
                raw_data=item
            )
            
            forecast_list.append(weather_data)
        
        return forecast_list

    
    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make HTTP request to API with comprehensive error handling.
        
        Args:
            endpoint: API endpoint URL
            params: Query parameters for the request
            
        Returns:
            Parsed JSON response as dictionary
            
        Raises:
            WeatherAPIError: For all API and network errors with user-friendly messages
        """
        try:
            response = self.session.get(endpoint, params=params, timeout=10)
            
            # Handle HTTP error status codes
            if response.status_code == 401:
                raise WeatherAPIError(
                    "Invalid API key. Please check your OpenWeatherMap API key in the configuration."
                )
            elif response.status_code == 404:
                raise WeatherAPIError(
                    "Invalid zipcode. Please provide a valid 5-digit US ZIP code."
                )
            elif response.status_code == 429:
                raise WeatherAPIError(
                    "API rate limit exceeded. Please wait a moment and try again."
                )
            elif response.status_code >= 400:
                raise WeatherAPIError(
                    f"API error: {response.status_code} - {response.text}"
                )
            
            # Parse JSON response
            try:
                data = response.json()
            except ValueError as e:
                raise WeatherAPIError(
                    f"Invalid JSON response from API: {str(e)}"
                )
            
            return data
            
        except Timeout:
            raise WeatherAPIError(
                "Request timed out. Please check your internet connection and try again."
            )
        except ConnectionError:
            raise WeatherAPIError(
                "Connection failed. Please check your internet connection and try again."
            )
        except RequestException as e:
            raise WeatherAPIError(
                f"Network error occurred: {str(e)}"
            )

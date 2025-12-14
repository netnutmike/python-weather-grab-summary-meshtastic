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
        precip: Precipitation amount (mm/hour)
        humidity: Humidity percentage
        wind_speed: Wind speed
        wind_direction: Wind direction in degrees
        pressure: Atmospheric pressure
        uv_index: UV index (optional)
        visibility: Visibility distance (optional)
        dew_point: Dew point temperature (optional)
        precip_probability: Precipitation probability 0-100% (optional, forecast only)
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
    precip_probability: Optional[float] = None
    raw_data: Dict[str, Any] = field(default_factory=dict)



class WeatherAPIError(Exception):
    """Custom exception for Weather API errors."""
    pass


class WeatherClient:
    """Client for OpenWeatherMap API v3.
    
    Handles API requests for current weather and hourly forecasts using
    latitude and longitude coordinates. Provides geocoding to convert
    ZIP codes to coordinates.
    
    Example:
        >>> client = WeatherClient(api_key="your_api_key")
        >>> # Using lat/lon directly
        >>> current = client.get_current_weather(lat=40.7128, lon=-74.0060)
        >>> print(f"Current temp: {current.temp}°F")
        >>> # Using zipcode (auto-converts to lat/lon)
        >>> lat, lon = client.geocode_zipcode("10001")
        >>> forecast = client.get_hourly_forecast(lat=lat, lon=lon, hours=5, day="today")
        >>> for entry in forecast:
        ...     print(f"{entry.hour}: {entry.temp}°F, {entry.condition}")
    """
    
    def __init__(self, api_key: str):
        """Initialize WeatherClient with API key.
        
        Sets up the HTTP session with a 10-second timeout for all requests.
        Uses API v3 endpoints with lat/lon coordinates.
        
        Args:
            api_key: OpenWeatherMap API key
        """
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/3.0"
        self.geo_url = "http://api.openweathermap.org/geo/1.0"
        self.session = requests.Session()
        self.session.timeout = 10

    def geocode_zipcode(self, zipcode: str) -> tuple[float, float]:
        """Convert US ZIP code to latitude and longitude coordinates.
        
        Uses OpenWeatherMap's Geocoding API to convert a ZIP code to coordinates.
        
        Args:
            zipcode: US ZIP code (5 digits)
            
        Returns:
            Tuple of (latitude, longitude)
            
        Raises:
            WeatherAPIError: If geocoding fails or ZIP code is invalid
            
        Example:
            >>> client = WeatherClient("your_api_key")
            >>> lat, lon = client.geocode_zipcode("10001")
            >>> print(f"Coordinates: {lat}, {lon}")
        """
        endpoint = f"{self.geo_url}/zip"
        params = {
            "zip": f"{zipcode},US",
            "appid": self.api_key
        }
        
        data = self._make_request(endpoint, params)
        
        lat = data.get("lat")
        lon = data.get("lon")
        
        if lat is None or lon is None:
            raise WeatherAPIError(
                f"Could not geocode ZIP code {zipcode}. Please verify it's a valid US ZIP code."
            )
        
        return lat, lon
    
    def get_current_weather(self, lat: float, lon: float) -> WeatherData:
        """Get current weather for coordinates.
        
        Retrieves current weather conditions including temperature, feels-like
        temperature, weather condition, humidity, wind, and pressure.
        
        Args:
            lat: Latitude coordinate
            lon: Longitude coordinate
            
        Returns:
            WeatherData object with current weather information
            
        Raises:
            WeatherAPIError: If API request fails or returns invalid data
            
        Example:
            >>> client = WeatherClient("your_api_key")
            >>> weather = client.get_current_weather(lat=40.7128, lon=-74.0060)
            >>> print(f"Temperature: {weather.temp}°F")
            >>> print(f"Condition: {weather.condition}")
        """
        endpoint = f"{self.base_url}/onecall"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "imperial",
            "exclude": "minutely,daily,alerts"
        }
        
        data = self._make_request(endpoint, params)
        
        # Parse current weather from response
        current = data.get("current", {})
        dt = datetime.fromtimestamp(current.get("dt", 0))
        hour_12 = dt.strftime("%-I%p").lower()
        
        weather_info = current.get("weather", [{}])[0]
        
        return WeatherData(
            timestamp=dt,
            hour=hour_12,
            temp=current.get("temp", 0.0),
            feels_like=current.get("feels_like", 0.0),
            condition=weather_info.get("description", "unknown"),
            condition_code=weather_info.get("id", 0),
            precip=current.get("rain", {}).get("1h", 0.0) + current.get("snow", {}).get("1h", 0.0),
            humidity=current.get("humidity", 0),
            wind_speed=current.get("wind_speed", 0.0),
            wind_direction=current.get("wind_deg", 0),
            pressure=current.get("pressure", 0),
            uv_index=current.get("uvi"),
            visibility=current.get("visibility"),
            dew_point=current.get("dew_point"),
            raw_data=current
        )

    def get_hourly_forecast(self, lat: float, lon: float, hours: int, day: str = "today") -> List[WeatherData]:
        """Get hourly forecast for coordinates.
        
        Retrieves forecast data for the specified number of hours. The forecast
        can be filtered to show only today's or tomorrow's data. API v3 provides
        hourly forecasts for up to 48 hours.
        
        Args:
            lat: Latitude coordinate
            lon: Longitude coordinate
            hours: Number of forecast hours to retrieve
            day: "today" or "tomorrow" to filter forecast data (default: "today")
            
        Returns:
            List of WeatherData objects for the forecast period
            
        Raises:
            WeatherAPIError: If API request fails or returns invalid data
            
        Example:
            >>> client = WeatherClient("your_api_key")
            >>> forecast = client.get_hourly_forecast(lat=40.7128, lon=-74.0060, hours=8, day="tomorrow")
            >>> for entry in forecast:
            ...     print(f"{entry.hour}: {entry.temp}°F, {entry.precip}% chance of rain")
        """
        endpoint = f"{self.base_url}/onecall"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "imperial",
            "exclude": "current,minutely,daily,alerts"
        }
        
        data = self._make_request(endpoint, params)
        
        forecast_list = []
        now = datetime.now()
        
        # Determine target date based on day parameter
        if day.lower() == "tomorrow":
            from datetime import timedelta
            target_date = (now + timedelta(days=1)).date()
        else:
            target_date = now.date()
        
        # Parse hourly forecast entries
        for item in data.get("hourly", []):
            dt = datetime.fromtimestamp(item["dt"])
            
            # Filter by target date
            if dt.date() != target_date:
                continue
            
            # Stop when we have enough hours
            if len(forecast_list) >= hours:
                break
            
            hour_12 = dt.strftime("%-I%p").lower()
            weather_info = item.get("weather", [{}])[0]
            
            # Calculate actual precipitation amount (rain + snow)
            precip_amount = item.get("rain", {}).get("1h", 0.0) + item.get("snow", {}).get("1h", 0.0)
            # Get precipitation probability
            precip_prob = item.get("pop", 0.0) * 100  # Convert to percentage
            
            weather_data = WeatherData(
                timestamp=dt,
                hour=hour_12,
                temp=item.get("temp", 0.0),
                feels_like=item.get("feels_like", 0.0),
                condition=weather_info.get("description", "unknown"),
                condition_code=weather_info.get("id", 0),
                precip=precip_amount,
                humidity=item.get("humidity", 0),
                wind_speed=item.get("wind_speed", 0.0),
                wind_direction=item.get("wind_deg", 0),
                pressure=item.get("pressure", 0),
                uv_index=item.get("uvi"),
                visibility=item.get("visibility"),
                dew_point=item.get("dew_point"),
                precip_probability=precip_prob,
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
                    "Location not found. Please check your coordinates or ZIP code."
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

"""Unit tests for weather_client module."""

import pytest
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
from weather_formatter.weather_client import WeatherClient, WeatherData, WeatherAPIError


class TestWeatherData:
    """Tests for WeatherData dataclass."""
    
    def test_weather_data_creation(self):
        """Test creating WeatherData instance."""
        dt = datetime.now()
        data = WeatherData(
            timestamp=dt,
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
            uv_index=3.5,
            visibility=10000,
            dew_point=55.0,
            raw_data={"test": "data"}
        )
        
        assert data.timestamp == dt
        assert data.hour == "1pm"
        assert data.temp == 75.0
        assert data.feels_like == 73.0
        assert data.condition == "clear sky"
        assert data.condition_code == 800
        assert data.precip == 0.0
        assert data.humidity == 60
        assert data.wind_speed == 5.5
        assert data.wind_direction == 180
        assert data.pressure == 1013
        assert data.uv_index == 3.5
        assert data.visibility == 10000
        assert data.dew_point == 55.0
        assert data.raw_data == {"test": "data"}
    
    def test_weather_data_optional_fields(self):
        """Test WeatherData with optional fields as None."""
        dt = datetime.now()
        data = WeatherData(
            timestamp=dt,
            hour="1pm",
            temp=75.0,
            feels_like=73.0,
            condition="clear sky",
            condition_code=800,
            precip=0.0,
            humidity=60,
            wind_speed=5.5,
            wind_direction=180,
            pressure=1013
        )
        
        assert data.uv_index is None
        assert data.visibility is None
        assert data.dew_point is None
        assert data.raw_data == {}


class TestWeatherClient:
    """Tests for WeatherClient class."""
    
    def test_initialization(self):
        """Test WeatherClient initializes correctly."""
        client = WeatherClient("test_api_key")
        
        assert client.api_key == "test_api_key"
        assert client.base_url == "https://api.openweathermap.org/data/3.0"
        assert client.geo_url == "http://api.openweathermap.org/geo/1.0"
        assert client.session is not None
    
    @patch('weather_formatter.weather_client.requests.Session')
    def test_geocode_zipcode_success(self, mock_session_class):
        """Test successful ZIP code geocoding."""
        mock_response_data = {
            "lat": 40.7128,
            "lon": -74.0060,
            "name": "New York"
        }
        
        mock_session = MagicMock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        client = WeatherClient("test_api_key")
        client.session = mock_session
        
        lat, lon = client.geocode_zipcode("10001")
        
        assert lat == 40.7128
        assert lon == -74.0060
        
        # Verify API call
        mock_session.get.assert_called_once()
        call_args = mock_session.get.call_args
        assert "geo" in call_args[0][0]
        assert call_args[1]["params"]["zip"] == "10001,US"
        assert call_args[1]["params"]["appid"] == "test_api_key"
    
    @patch('weather_formatter.weather_client.requests.Session')
    def test_get_current_weather_success(self, mock_session_class):
        """Test successful current weather retrieval."""
        # Mock response data for One Call API 3.0
        mock_response_data = {
            "current": {
                "dt": 1609459200,  # 2021-01-01 00:00:00 UTC
                "temp": 75.0,
                "feels_like": 73.0,
                "humidity": 60,
                "pressure": 1013,
                "wind_speed": 5.5,
                "wind_deg": 180,
                "visibility": 10000,
                "uvi": 3.5,
                "dew_point": 55.0,
                "weather": [
                    {
                        "id": 800,
                        "description": "clear sky"
                    }
                ],
                "rain": {},
                "snow": {}
            }
        }
        
        # Setup mock
        mock_session = MagicMock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        client = WeatherClient("test_api_key")
        client.session = mock_session
        
        weather = client.get_current_weather(lat=40.7128, lon=-74.0060)
        
        assert isinstance(weather, WeatherData)
        assert weather.temp == 75.0
        assert weather.feels_like == 73.0
        assert weather.condition == "clear sky"
        assert weather.condition_code == 800
        assert weather.humidity == 60
        assert weather.wind_speed == 5.5
        assert weather.wind_direction == 180
        assert weather.pressure == 1013
        assert weather.visibility == 10000
        assert weather.uv_index == 3.5
        assert weather.dew_point == 55.0
        
        # Verify API call
        mock_session.get.assert_called_once()
        call_args = mock_session.get.call_args
        assert "onecall" in call_args[0][0]
        assert call_args[1]["params"]["lat"] == 40.7128
        assert call_args[1]["params"]["lon"] == -74.0060
        assert call_args[1]["params"]["appid"] == "test_api_key"
        assert call_args[1]["params"]["units"] == "imperial"
    
    @patch('weather_formatter.weather_client.requests.Session')
    def test_get_hourly_forecast_success(self, mock_session_class):
        """Test successful hourly forecast retrieval."""
        # Create timestamps for today
        now = datetime.now()
        base_timestamp = int(now.replace(hour=12, minute=0, second=0, microsecond=0).timestamp())
        
        mock_response_data = {
            "hourly": [
                {
                    "dt": base_timestamp,
                    "temp": 75.0,
                    "feels_like": 73.0,
                    "humidity": 60,
                    "pressure": 1013,
                    "wind_speed": 5.5,
                    "wind_deg": 180,
                    "visibility": 10000,
                    "uvi": 3.5,
                    "dew_point": 55.0,
                    "weather": [{"id": 800, "description": "clear sky"}],
                    "pop": 0.0
                },
                {
                    "dt": base_timestamp + 3600,
                    "temp": 76.0,
                    "feels_like": 74.0,
                    "humidity": 58,
                    "pressure": 1012,
                    "wind_speed": 6.0,
                    "wind_deg": 190,
                    "visibility": 10000,
                    "uvi": 4.0,
                    "dew_point": 56.0,
                    "weather": [{"id": 801, "description": "few clouds"}],
                    "pop": 0.1
                },
                {
                    "dt": base_timestamp + 7200,
                    "temp": 74.0,
                    "feels_like": 72.0,
                    "humidity": 70,
                    "pressure": 1011,
                    "wind_speed": 7.0,
                    "wind_deg": 200,
                    "visibility": 8000,
                    "uvi": 3.0,
                    "dew_point": 58.0,
                    "weather": [{"id": 500, "description": "light rain"}],
                    "pop": 0.5
                }
            ]
        }
        
        # Setup mock
        mock_session = MagicMock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        client = WeatherClient("test_api_key")
        client.session = mock_session
        
        forecast = client.get_hourly_forecast(lat=40.7128, lon=-74.0060, hours=3, day="today")
        
        assert len(forecast) <= 3
        assert all(isinstance(w, WeatherData) for w in forecast)
        
        # Verify API call
        mock_session.get.assert_called_once()
        call_args = mock_session.get.call_args
        assert "onecall" in call_args[0][0]
        assert call_args[1]["params"]["lat"] == 40.7128
        assert call_args[1]["params"]["lon"] == -74.0060
    
    @patch('weather_formatter.weather_client.requests.Session')
    def test_make_request_invalid_api_key(self, mock_session_class):
        """Test error handling for invalid API key."""
        mock_session = MagicMock()
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Invalid API key"
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        client = WeatherClient("invalid_key")
        client.session = mock_session
        
        with pytest.raises(WeatherAPIError) as exc_info:
            client.get_current_weather("10001")
        
        assert "Invalid API key" in str(exc_info.value)
    
    @patch('weather_formatter.weather_client.requests.Session')
    def test_make_request_location_not_found(self, mock_session_class):
        """Test error handling for location not found."""
        mock_session = MagicMock()
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Location not found"
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        client = WeatherClient("test_key")
        client.session = mock_session
        
        with pytest.raises(WeatherAPIError) as exc_info:
            client.get_current_weather(lat=999, lon=999)
        
        assert "Location not found" in str(exc_info.value)
    
    @patch('weather_formatter.weather_client.requests.Session')
    def test_make_request_rate_limit(self, mock_session_class):
        """Test error handling for rate limit exceeded."""
        mock_session = MagicMock()
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.text = "Rate limit exceeded"
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        client = WeatherClient("test_key")
        client.session = mock_session
        
        with pytest.raises(WeatherAPIError) as exc_info:
            client.get_current_weather("10001")
        
        assert "rate limit" in str(exc_info.value).lower()
    
    @patch('weather_formatter.weather_client.requests.Session')
    def test_make_request_timeout(self, mock_session_class):
        """Test error handling for request timeout."""
        from requests.exceptions import Timeout
        
        mock_session = MagicMock()
        mock_session.get.side_effect = Timeout("Request timed out")
        mock_session_class.return_value = mock_session
        
        client = WeatherClient("test_key")
        client.session = mock_session
        
        with pytest.raises(WeatherAPIError) as exc_info:
            client.get_current_weather(lat=40.7128, lon=-74.0060)
        
        assert "timed out" in str(exc_info.value).lower()
    
    @patch('weather_formatter.weather_client.requests.Session')
    def test_make_request_connection_error(self, mock_session_class):
        """Test error handling for connection error."""
        from requests.exceptions import ConnectionError
        
        mock_session = MagicMock()
        mock_session.get.side_effect = ConnectionError("Connection failed")
        mock_session_class.return_value = mock_session
        
        client = WeatherClient("test_key")
        client.session = mock_session
        
        with pytest.raises(WeatherAPIError) as exc_info:
            client.get_current_weather(lat=40.7128, lon=-74.0060)
        
        assert "connection" in str(exc_info.value).lower()
    
    @patch('weather_formatter.weather_client.requests.Session')
    def test_make_request_invalid_json(self, mock_session_class):
        """Test error handling for invalid JSON response."""
        mock_session = MagicMock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        client = WeatherClient("test_key")
        client.session = mock_session
        
        with pytest.raises(WeatherAPIError) as exc_info:
            client.get_current_weather(lat=40.7128, lon=-74.0060)
        
        assert "Invalid JSON" in str(exc_info.value)
    
    @patch('weather_formatter.weather_client.requests.Session')
    def test_get_current_weather_with_precipitation(self, mock_session_class):
        """Test current weather with rain and snow data."""
        mock_response_data = {
            "current": {
                "dt": 1609459200,
                "temp": 65.0,
                "feels_like": 63.0,
                "humidity": 80,
                "pressure": 1010,
                "wind_speed": 10.0,
                "wind_deg": 270,
                "visibility": 5000,
                "weather": [{"id": 500, "description": "light rain"}],
                "rain": {"1h": 2.5},
                "snow": {"1h": 0.5}
            }
        }
        
        mock_session = MagicMock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        client = WeatherClient("test_api_key")
        client.session = mock_session
        
        weather = client.get_current_weather(lat=40.7128, lon=-74.0060)
        
        # Precipitation should be sum of rain and snow
        assert weather.precip == 3.0
        assert weather.condition == "light rain"
    
    @patch('weather_formatter.weather_client.requests.Session')
    def test_hourly_forecast_filters_by_day(self, mock_session_class):
        """Test that hourly forecast filters entries by target day."""
        now = datetime.now()
        today_timestamp = int(now.replace(hour=12, minute=0, second=0, microsecond=0).timestamp())
        tomorrow_timestamp = today_timestamp + 86400  # +24 hours
        
        mock_response_data = {
            "hourly": [
                {
                    "dt": today_timestamp,
                    "temp": 75.0,
                    "feels_like": 73.0,
                    "humidity": 60,
                    "pressure": 1013,
                    "wind_speed": 5.0,
                    "wind_deg": 180,
                    "weather": [{"id": 800, "description": "clear"}],
                    "pop": 0.0
                },
                {
                    "dt": tomorrow_timestamp,
                    "temp": 70.0,
                    "feels_like": 68.0,
                    "humidity": 65,
                    "pressure": 1012,
                    "wind_speed": 6.0,
                    "wind_deg": 190,
                    "weather": [{"id": 801, "description": "clouds"}],
                    "pop": 0.1
                }
            ]
        }
        
        mock_session = MagicMock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        client = WeatherClient("test_api_key")
        client.session = mock_session
        
        # Request today's forecast - should only get today's entries
        forecast_today = client.get_hourly_forecast(lat=40.7128, lon=-74.0060, hours=5, day="today")
        
        # All entries should be from today
        for entry in forecast_today:
            assert entry.timestamp.date() == now.date()

"""Integration tests for Weather Formatter application.

These tests verify the complete end-to-end flow from CLI to output,
including configuration loading, API interaction, and output formatting.
"""

import pytest
import tempfile
import os
import sys
from unittest.mock import patch, Mock, MagicMock
from datetime import datetime
from io import StringIO

from weather_formatter.cli import main, parse_arguments
from weather_formatter.config import WeatherConfig


class TestEndToEndFlow:
    """Test complete application flow with mocked API."""
    
    def create_mock_api_responses(self):
        """Create mock API response data for testing."""
        now = datetime.now()
        base_timestamp = int(now.replace(hour=12, minute=0, second=0, microsecond=0).timestamp())
        
        current_weather_response = {
            "dt": base_timestamp,
            "weather": [{"id": 800, "description": "clear sky"}],
            "main": {
                "temp": 74.0,
                "feels_like": 72.0,
                "humidity": 60,
                "pressure": 1013
            },
            "wind": {"speed": 5.0, "deg": 180},
            "visibility": 10000,
            "rain": {},
            "snow": {}
        }
        
        forecast_response = {
            "list": [
                {
                    "dt": base_timestamp + (i * 3600),
                    "weather": [{"id": 800, "description": "clear sky"}],
                    "main": {
                        "temp": 75.0 + i,
                        "feels_like": 73.0 + i,
                        "humidity": 60 - i,
                        "pressure": 1013
                    },
                    "wind": {"speed": 5.0 + i * 0.5, "deg": 180},
                    "pop": i * 0.1,
                    "visibility": 10000
                }
                for i in range(5)
            ]
        }
        
        return current_weather_response, forecast_response
    
    @patch('weather_formatter.weather_client.requests.Session')
    def test_complete_flow_with_config_file(self, mock_session_class):
        """Test complete flow from config file to output."""
        # Create temporary config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("""
zipcode: "10001"
api_key: "test_api_key"
forecast_hours: 3
forecast_day: "today"
entry_separator: "#"
field_separator: ","
output_fields:
  - hour
  - icon
  - temp
  - precip
icon_mappings:
  "clear sky": "9"
  "default": "?"
""")
            f.flush()
            config_path = f.name
        
        try:
            # Setup mock API responses
            current_response, forecast_response = self.create_mock_api_responses()
            
            mock_session = MagicMock()
            mock_response_current = Mock()
            mock_response_current.status_code = 200
            mock_response_current.json.return_value = current_response
            
            mock_response_forecast = Mock()
            mock_response_forecast.status_code = 200
            mock_response_forecast.json.return_value = forecast_response
            
            # Return different responses for different endpoints
            def get_side_effect(url, **kwargs):
                if 'weather' in url and 'forecast' not in url:
                    return mock_response_current
                else:
                    return mock_response_forecast
            
            mock_session.get.side_effect = get_side_effect
            mock_session_class.return_value = mock_session
            
            # Capture stdout
            captured_output = StringIO()
            
            # Run main with mocked arguments
            with patch('sys.argv', ['weather-formatter', '--config', config_path]):
                with patch('sys.stdout', captured_output):
                    exit_code = main()
            
            # Verify exit code
            assert exit_code == 0
            
            # Verify output format
            output = captured_output.getvalue().strip()
            assert output.startswith('#')
            assert output.endswith('#')
            assert '#74#' in output  # Current temp
            assert '9' in output  # Icon code for clear sky
            
        finally:
            os.unlink(config_path)
    
    @patch('weather_formatter.weather_client.requests.Session')
    def test_complete_flow_with_cli_only(self, mock_session_class):
        """Test complete flow using only CLI arguments (no config file)."""
        # Setup mock API responses
        current_response, forecast_response = self.create_mock_api_responses()
        
        mock_session = MagicMock()
        mock_response_current = Mock()
        mock_response_current.status_code = 200
        mock_response_current.json.return_value = current_response
        
        mock_response_forecast = Mock()
        mock_response_forecast.status_code = 200
        mock_response_forecast.json.return_value = forecast_response
        
        def get_side_effect(url, **kwargs):
            if 'weather' in url and 'forecast' not in url:
                return mock_response_current
            else:
                return mock_response_forecast
        
        mock_session.get.side_effect = get_side_effect
        mock_session_class.return_value = mock_session
        
        # Use a non-existent config file path
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = os.path.join(tmpdir, 'nonexistent.yaml')
            
            # Capture stdout and stderr
            captured_output = StringIO()
            captured_error = StringIO()
            
            # Run main with CLI arguments
            with patch('sys.argv', [
                'weather-formatter',
                '--config', config_path,
                '-z', '10001',
                '-k', 'test_api_key',
                '--hours', '3'
            ]):
                with patch('sys.stdout', captured_output):
                    with patch('sys.stderr', captured_error):
                        exit_code = main()
            
            # Should create config file and exit
            assert exit_code == 0
            assert os.path.exists(config_path)
            assert 'Created default configuration file' in captured_error.getvalue()


class TestConfigFileAndCLIOverrides:
    """Test configuration merging scenarios."""
    
    @patch('weather_formatter.weather_client.requests.Session')
    def test_cli_overrides_config_file(self, mock_session_class):
        """Test that CLI arguments override config file settings."""
        # Create config file with specific settings
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("""
zipcode: "10001"
api_key: "file_api_key"
forecast_hours: 5
forecast_day: "today"
entry_separator: "#"
field_separator: ","
output_fields:
  - hour
  - temp
icon_mappings:
  "clear sky": "9"
  "default": "?"
""")
            f.flush()
            config_path = f.name
        
        try:
            # Setup mock API responses
            now = datetime.now()
            base_timestamp = int(now.replace(hour=12, minute=0, second=0, microsecond=0).timestamp())
            
            current_response = {
                "dt": base_timestamp,
                "weather": [{"id": 800, "description": "clear sky"}],
                "main": {"temp": 74.0, "feels_like": 72.0, "humidity": 60, "pressure": 1013},
                "wind": {"speed": 5.0, "deg": 180},
                "visibility": 10000,
                "rain": {},
                "snow": {}
            }
            
            forecast_response = {
                "list": [
                    {
                        "dt": base_timestamp + 3600,
                        "weather": [{"id": 800, "description": "clear sky"}],
                        "main": {"temp": 75.0, "feels_like": 73.0, "humidity": 60, "pressure": 1013},
                        "wind": {"speed": 5.0, "deg": 180},
                        "pop": 0.0,
                        "visibility": 10000
                    }
                ]
            }
            
            mock_session = MagicMock()
            mock_response_current = Mock()
            mock_response_current.status_code = 200
            mock_response_current.json.return_value = current_response
            
            mock_response_forecast = Mock()
            mock_response_forecast.status_code = 200
            mock_response_forecast.json.return_value = forecast_response
            
            def get_side_effect(url, **kwargs):
                if 'weather' in url and 'forecast' not in url:
                    return mock_response_current
                else:
                    return mock_response_forecast
            
            mock_session.get.side_effect = get_side_effect
            mock_session_class.return_value = mock_session
            
            # Capture stdout
            captured_output = StringIO()
            
            # Run with CLI overrides
            with patch('sys.argv', [
                'weather-formatter',
                '--config', config_path,
                '-z', '90210',  # Override zipcode
                '--hours', '2',  # Override hours
                '--entry-sep', '|',  # Override separator
                '--preamble', 'WEATHER:'  # Add preamble
            ]):
                with patch('sys.stdout', captured_output):
                    exit_code = main()
            
            # Verify exit code
            assert exit_code == 0
            
            # Verify output uses CLI overrides
            output = captured_output.getvalue().strip()
            assert output.startswith('WEATHER:')  # Preamble from CLI
            assert '|' in output  # Entry separator from CLI
            
            # Verify API was called with overridden zipcode
            calls = mock_session.get.call_args_list
            assert any('90210' in str(call) for call in calls)
            
        finally:
            os.unlink(config_path)
    
    @patch('weather_formatter.weather_client.requests.Session')
    def test_partial_cli_overrides(self, mock_session_class):
        """Test that only specified CLI arguments override config."""
        # Create config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("""
zipcode: "10001"
api_key: "test_api_key"
forecast_hours: 5
entry_separator: "#"
field_separator: ","
preamble: "DEFAULT:"
output_fields:
  - hour
  - temp
icon_mappings:
  "clear sky": "9"
  "default": "?"
""")
            f.flush()
            config_path = f.name
        
        try:
            # Setup mock API responses
            now = datetime.now()
            base_timestamp = int(now.replace(hour=12, minute=0, second=0, microsecond=0).timestamp())
            
            current_response = {
                "dt": base_timestamp,
                "weather": [{"id": 800, "description": "clear sky"}],
                "main": {"temp": 74.0, "feels_like": 72.0, "humidity": 60, "pressure": 1013},
                "wind": {"speed": 5.0, "deg": 180},
                "visibility": 10000,
                "rain": {},
                "snow": {}
            }
            
            forecast_response = {
                "list": [
                    {
                        "dt": base_timestamp + 3600,
                        "weather": [{"id": 800, "description": "clear sky"}],
                        "main": {"temp": 75.0, "feels_like": 73.0, "humidity": 60, "pressure": 1013},
                        "wind": {"speed": 5.0, "deg": 180},
                        "pop": 0.0,
                        "visibility": 10000
                    }
                ]
            }
            
            mock_session = MagicMock()
            mock_response_current = Mock()
            mock_response_current.status_code = 200
            mock_response_current.json.return_value = current_response
            
            mock_response_forecast = Mock()
            mock_response_forecast.status_code = 200
            mock_response_forecast.json.return_value = forecast_response
            
            def get_side_effect(url, **kwargs):
                if 'weather' in url and 'forecast' not in url:
                    return mock_response_current
                else:
                    return mock_response_forecast
            
            mock_session.get.side_effect = get_side_effect
            mock_session_class.return_value = mock_session
            
            # Capture stdout
            captured_output = StringIO()
            
            # Run with only hours override
            with patch('sys.argv', [
                'weather-formatter',
                '--config', config_path,
                '--hours', '3'  # Only override hours
            ]):
                with patch('sys.stdout', captured_output):
                    exit_code = main()
            
            # Verify exit code
            assert exit_code == 0
            
            # Verify output uses config file settings except hours
            output = captured_output.getvalue().strip()
            assert output.startswith('DEFAULT:')  # Preamble from config
            assert '#' in output  # Entry separator from config
            
        finally:
            os.unlink(config_path)


class TestErrorHandling:
    """Test error handling scenarios."""
    
    def test_missing_required_config(self):
        """Test error when required configuration is missing."""
        # Create config file without required fields
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("""
forecast_hours: 5
""")
            f.flush()
            config_path = f.name
        
        try:
            # Capture stderr
            captured_error = StringIO()
            
            # Run main
            with patch('sys.argv', ['weather-formatter', '--config', config_path]):
                with patch('sys.stderr', captured_error):
                    exit_code = main()
            
            # Should fail with configuration error
            assert exit_code == 1
            error_output = captured_error.getvalue()
            assert 'Configuration errors' in error_output or 'required' in error_output.lower()
            
        finally:
            os.unlink(config_path)
    
    def test_invalid_zipcode_format(self):
        """Test error when zipcode format is invalid."""
        # Create config file with invalid zipcode
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("""
zipcode: "123"
api_key: "test_key"
""")
            f.flush()
            config_path = f.name
        
        try:
            # Capture stderr
            captured_error = StringIO()
            
            # Run main
            with patch('sys.argv', ['weather-formatter', '--config', config_path]):
                with patch('sys.stderr', captured_error):
                    exit_code = main()
            
            # Should fail with validation error
            assert exit_code == 1
            error_output = captured_error.getvalue()
            assert '5-digit' in error_output or 'zipcode' in error_output.lower()
            
        finally:
            os.unlink(config_path)
    
    def test_invalid_cli_zipcode(self):
        """Test error when CLI zipcode is invalid."""
        # Capture stderr
        captured_error = StringIO()
        
        # Run with invalid zipcode
        with patch('sys.argv', [
            'weather-formatter',
            '-z', 'abc',
            '-k', 'test_key'
        ]):
            with patch('sys.stderr', captured_error):
                exit_code = main()
        
        # Should fail with validation error
        assert exit_code == 1
        error_output = captured_error.getvalue()
        assert 'zipcode' in error_output.lower()
    
    @patch('weather_formatter.weather_client.requests.Session')
    def test_api_error_invalid_key(self, mock_session_class):
        """Test error handling for invalid API key."""
        # Create valid config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("""
zipcode: "10001"
api_key: "invalid_key"
""")
            f.flush()
            config_path = f.name
        
        try:
            # Setup mock to return 401 error
            mock_session = MagicMock()
            mock_response = Mock()
            mock_response.status_code = 401
            mock_response.text = "Invalid API key"
            mock_session.get.return_value = mock_response
            mock_session_class.return_value = mock_session
            
            # Capture stderr
            captured_error = StringIO()
            
            # Run main
            with patch('sys.argv', ['weather-formatter', '--config', config_path]):
                with patch('sys.stderr', captured_error):
                    exit_code = main()
            
            # Should fail with API error
            assert exit_code == 2
            error_output = captured_error.getvalue()
            assert 'API' in error_output or 'api' in error_output.lower()
            
        finally:
            os.unlink(config_path)
    
    @patch('weather_formatter.weather_client.requests.Session')
    def test_api_error_invalid_zipcode(self, mock_session_class):
        """Test error handling for invalid zipcode from API."""
        # Create config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("""
zipcode: "00000"
api_key: "test_key"
""")
            f.flush()
            config_path = f.name
        
        try:
            # Setup mock to return 404 error
            mock_session = MagicMock()
            mock_response = Mock()
            mock_response.status_code = 404
            mock_response.text = "City not found"
            mock_session.get.return_value = mock_response
            mock_session_class.return_value = mock_session
            
            # Capture stderr
            captured_error = StringIO()
            
            # Run main
            with patch('sys.argv', ['weather-formatter', '--config', config_path]):
                with patch('sys.stderr', captured_error):
                    exit_code = main()
            
            # Should fail with API error
            assert exit_code == 2
            error_output = captured_error.getvalue()
            assert 'zipcode' in error_output.lower() or 'not found' in error_output.lower()
            
        finally:
            os.unlink(config_path)
    
    @patch('weather_formatter.weather_client.requests.Session')
    def test_api_error_rate_limit(self, mock_session_class):
        """Test error handling for API rate limit."""
        # Create config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("""
zipcode: "10001"
api_key: "test_key"
""")
            f.flush()
            config_path = f.name
        
        try:
            # Setup mock to return 429 error
            mock_session = MagicMock()
            mock_response = Mock()
            mock_response.status_code = 429
            mock_response.text = "Rate limit exceeded"
            mock_session.get.return_value = mock_response
            mock_session_class.return_value = mock_session
            
            # Capture stderr
            captured_error = StringIO()
            
            # Run main
            with patch('sys.argv', ['weather-formatter', '--config', config_path]):
                with patch('sys.stderr', captured_error):
                    exit_code = main()
            
            # Should fail with API error
            assert exit_code == 2
            error_output = captured_error.getvalue()
            assert 'rate limit' in error_output.lower() or 'API' in error_output
            
        finally:
            os.unlink(config_path)
    
    @patch('weather_formatter.weather_client.requests.Session')
    def test_network_timeout_error(self, mock_session_class):
        """Test error handling for network timeout."""
        from requests.exceptions import Timeout
        
        # Create config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("""
zipcode: "10001"
api_key: "test_key"
""")
            f.flush()
            config_path = f.name
        
        try:
            # Setup mock to raise timeout
            mock_session = MagicMock()
            mock_session.get.side_effect = Timeout("Request timed out")
            mock_session_class.return_value = mock_session
            
            # Capture stderr
            captured_error = StringIO()
            
            # Run main
            with patch('sys.argv', ['weather-formatter', '--config', config_path]):
                with patch('sys.stderr', captured_error):
                    exit_code = main()
            
            # Should fail with API error
            assert exit_code == 2
            error_output = captured_error.getvalue()
            assert 'timed out' in error_output.lower() or 'timeout' in error_output.lower()
            
        finally:
            os.unlink(config_path)
    
    @patch('weather_formatter.weather_client.requests.Session')
    def test_connection_error(self, mock_session_class):
        """Test error handling for connection error."""
        from requests.exceptions import ConnectionError
        
        # Create config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("""
zipcode: "10001"
api_key: "test_key"
""")
            f.flush()
            config_path = f.name
        
        try:
            # Setup mock to raise connection error
            mock_session = MagicMock()
            mock_session.get.side_effect = ConnectionError("Connection failed")
            mock_session_class.return_value = mock_session
            
            # Capture stderr
            captured_error = StringIO()
            
            # Run main
            with patch('sys.argv', ['weather-formatter', '--config', config_path]):
                with patch('sys.stderr', captured_error):
                    exit_code = main()
            
            # Should fail with API error
            assert exit_code == 2
            error_output = captured_error.getvalue()
            assert 'connection' in error_output.lower() or 'error' in error_output.lower()
            
        finally:
            os.unlink(config_path)
    
    def test_malformed_yaml_config(self):
        """Test error handling for malformed YAML config."""
        # Create malformed config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("""
zipcode: "10001"
api_key: [invalid yaml structure
""")
            f.flush()
            config_path = f.name
        
        try:
            # Capture stderr
            captured_error = StringIO()
            
            # Run main
            with patch('sys.argv', ['weather-formatter', '--config', config_path]):
                with patch('sys.stderr', captured_error):
                    exit_code = main()
            
            # Should fail with configuration error
            assert exit_code == 1
            
        finally:
            os.unlink(config_path)
    
    def test_invalid_forecast_hours(self):
        """Test error handling for invalid forecast hours."""
        # Capture stderr
        captured_error = StringIO()
        
        # Run with invalid hours
        with patch('sys.argv', [
            'weather-formatter',
            '-z', '10001',
            '-k', 'test_key',
            '--hours', '0'
        ]):
            with patch('sys.stderr', captured_error):
                exit_code = main()
        
        # Should fail with validation error
        assert exit_code == 1
        error_output = captured_error.getvalue()
        assert 'hours' in error_output.lower() or 'positive' in error_output.lower()


class TestOutputFormatting:
    """Test different output formatting scenarios."""
    
    @patch('weather_formatter.weather_client.requests.Session')
    def test_custom_field_selection(self, mock_session_class):
        """Test output with custom field selection."""
        # Create config with custom fields
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("""
zipcode: "10001"
api_key: "test_key"
forecast_hours: 2
output_fields:
  - hour
  - temp
  - humidity
  - wind_speed
icon_mappings:
  "clear sky": "9"
  "default": "?"
""")
            f.flush()
            config_path = f.name
        
        try:
            # Setup mock API responses
            now = datetime.now()
            base_timestamp = int(now.replace(hour=12, minute=0, second=0, microsecond=0).timestamp())
            
            current_response = {
                "dt": base_timestamp,
                "weather": [{"id": 800, "description": "clear sky"}],
                "main": {"temp": 74.0, "feels_like": 72.0, "humidity": 60, "pressure": 1013},
                "wind": {"speed": 5.5, "deg": 180},
                "visibility": 10000,
                "rain": {},
                "snow": {}
            }
            
            forecast_response = {
                "list": [
                    {
                        "dt": base_timestamp + 3600,
                        "weather": [{"id": 800, "description": "clear sky"}],
                        "main": {"temp": 75.0, "feels_like": 73.0, "humidity": 58, "pressure": 1013},
                        "wind": {"speed": 6.0, "deg": 180},
                        "pop": 0.0,
                        "visibility": 10000
                    }
                ]
            }
            
            mock_session = MagicMock()
            mock_response_current = Mock()
            mock_response_current.status_code = 200
            mock_response_current.json.return_value = current_response
            
            mock_response_forecast = Mock()
            mock_response_forecast.status_code = 200
            mock_response_forecast.json.return_value = forecast_response
            
            def get_side_effect(url, **kwargs):
                if 'weather' in url and 'forecast' not in url:
                    return mock_response_current
                else:
                    return mock_response_forecast
            
            mock_session.get.side_effect = get_side_effect
            mock_session_class.return_value = mock_session
            
            # Capture stdout
            captured_output = StringIO()
            
            # Run main
            with patch('sys.argv', ['weather-formatter', '--config', config_path]):
                with patch('sys.stdout', captured_output):
                    exit_code = main()
            
            # Verify exit code
            assert exit_code == 0
            
            # Verify output contains custom fields
            output = captured_output.getvalue().strip()
            # Should contain hour, temp, humidity, wind_speed
            assert ',' in output  # Field separator
            
        finally:
            os.unlink(config_path)
    
    @patch('weather_formatter.weather_client.requests.Session')
    def test_tomorrow_forecast(self, mock_session_class):
        """Test requesting tomorrow's forecast."""
        # Create config for tomorrow
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("""
zipcode: "10001"
api_key: "test_key"
forecast_hours: 3
forecast_day: "tomorrow"
output_fields:
  - hour
  - temp
icon_mappings:
  "clear sky": "9"
  "default": "?"
""")
            f.flush()
            config_path = f.name
        
        try:
            # Setup mock API responses with tomorrow's data
            now = datetime.now()
            base_timestamp = int(now.replace(hour=12, minute=0, second=0, microsecond=0).timestamp())
            tomorrow_timestamp = base_timestamp + 86400  # +24 hours
            
            current_response = {
                "dt": base_timestamp,
                "weather": [{"id": 800, "description": "clear sky"}],
                "main": {"temp": 74.0, "feels_like": 72.0, "humidity": 60, "pressure": 1013},
                "wind": {"speed": 5.0, "deg": 180},
                "visibility": 10000,
                "rain": {},
                "snow": {}
            }
            
            forecast_response = {
                "list": [
                    {
                        "dt": tomorrow_timestamp + (i * 3600),
                        "weather": [{"id": 800, "description": "clear sky"}],
                        "main": {"temp": 70.0 + i, "feels_like": 68.0 + i, "humidity": 60, "pressure": 1013},
                        "wind": {"speed": 5.0, "deg": 180},
                        "pop": 0.0,
                        "visibility": 10000
                    }
                    for i in range(5)
                ]
            }
            
            mock_session = MagicMock()
            mock_response_current = Mock()
            mock_response_current.status_code = 200
            mock_response_current.json.return_value = current_response
            
            mock_response_forecast = Mock()
            mock_response_forecast.status_code = 200
            mock_response_forecast.json.return_value = forecast_response
            
            def get_side_effect(url, **kwargs):
                if 'weather' in url and 'forecast' not in url:
                    return mock_response_current
                else:
                    return mock_response_forecast
            
            mock_session.get.side_effect = get_side_effect
            mock_session_class.return_value = mock_session
            
            # Capture stdout
            captured_output = StringIO()
            
            # Run main
            with patch('sys.argv', ['weather-formatter', '--config', config_path]):
                with patch('sys.stdout', captured_output):
                    exit_code = main()
            
            # Verify exit code
            assert exit_code == 0
            
            # Verify output exists
            output = captured_output.getvalue().strip()
            assert len(output) > 0
            assert '#' in output
            
        finally:
            os.unlink(config_path)

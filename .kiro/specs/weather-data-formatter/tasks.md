# Implementation Plan

- [x] 1. Set up project structure and dependencies
  - Create directory structure for the weather_formatter package
  - Create `__init__.py` files for package structure
  - Create `setup.py` with package metadata and dependencies
  - Create `requirements.txt` with pinned dependencies (requests, PyYAML, python-dateutil)
  - Create `.gitignore` file for Python projects (include `weather_config.yaml`, `__pycache__`, `*.pyc`, `.env`, etc.)
  - _Requirements: 9.1, 9.2, 9.3_

- [x] 2. Implement configuration management module
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6_

- [x] 2.1 Create WeatherConfig dataclass
  - Define `WeatherConfig` dataclass in `config.py` with all configuration fields (zipcode, api_key, forecast_hours, forecast_day, entry_separator, field_separator, output_fields, icon_mappings, preamble)
  - Implement `validate()` method to check required fields and valid values
  - Add type hints for all fields
  - _Requirements: 4.2, 4.3_

- [x] 2.2 Implement YAML configuration loading
  - Write `load_config()` function to read and parse YAML file from current working directory
  - Handle missing file gracefully (return None or default config)
  - Handle malformed YAML with clear error messages
  - Apply default values for missing optional fields
  - _Requirements: 4.1, 4.2, 4.5, 4.6_

- [x] 2.3 Implement default config file creation
  - Write `create_default_config()` function to generate example `weather_config.yaml`
  - Include all configuration options with comments explaining each setting
  - Include default icon mappings for common weather conditions
  - Save file to current working directory
  - _Requirements: 4.4_

- [x] 2.4 Implement config merging logic
  - Write `merge_config()` function to combine file config with CLI arguments
  - Ensure CLI arguments override file config values
  - Handle None values appropriately (don't override with None)
  - _Requirements: 5.3_

- [x] 3. Implement icon mapping module
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [x] 3.1 Create IconMapper class
  - Implement `IconMapper` class in `icon_mapper.py`
  - Initialize with custom mappings dictionary
  - Store default icon for unmapped conditions
  - _Requirements: 3.2, 3.3_

- [x] 3.2 Implement condition mapping logic
  - Write `map_condition()` method to map weather condition strings to icon codes
  - Implement `_normalize_mappings()` to handle case-insensitive matching (lowercase, strip whitespace)
  - Return default icon when condition not found in mappings
  - _Requirements: 3.1, 3.4, 3.5_

- [x] 3.3 Create default icon mappings
  - Implement `get_default_mappings()` static method with default icon codes
  - Map common OpenWeatherMap conditions: clear sky→9, clouds→0/4, rain→2/6/7, thunderstorm→5, snow→8, fog/mist→1, windy→;
  - Include "default" mapping for unknown conditions
  - _Requirements: 3.1_

- [x] 4. Implement Weather API client module
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 6.1, 6.2, 6.3, 6.4, 6.5_

- [x] 4.1 Create WeatherData dataclass
  - Define `WeatherData` dataclass in `weather_client.py` with all weather fields
  - Include fields: timestamp, hour, temp, feels_like, condition, condition_code, precip, humidity, wind_speed, wind_direction, pressure, uv_index, visibility, dew_point
  - Add `raw_data` field to store complete API response for extensibility
  - _Requirements: 1.3, 1.5, 2.5, 2.6_

- [x] 4.2 Create WeatherClient class structure
  - Implement `WeatherClient` class with initialization
  - Store API key and base URL
  - Set up requests session with timeout (10 seconds)
  - _Requirements: 1.1, 1.2_

- [x] 4.3 Implement current weather retrieval
  - Write `get_current_weather()` method to fetch current weather by zipcode
  - Make API call to OpenWeatherMap current weather endpoint
  - Parse JSON response into WeatherData object
  - Extract current temperature for output
  - _Requirements: 1.1_

- [x] 4.4 Implement hourly forecast retrieval
  - Write `get_hourly_forecast()` method to fetch forecast data
  - Support configurable number of hours parameter
  - Support "today" and "tomorrow" day parameter
  - Filter forecast data based on day selection (today vs tomorrow)
  - Parse JSON response into list of WeatherData objects
  - _Requirements: 1.2, 1.3, 1.4, 6.1, 6.2, 6.3, 6.4_

- [x] 4.5 Implement API error handling
  - Write `_make_request()` helper method for HTTP requests
  - Handle network errors (timeout, connection refused) with user-friendly messages
  - Handle API errors (invalid key, rate limit, invalid zipcode) with specific error messages
  - Handle invalid JSON responses
  - Raise custom exceptions with clear error messages
  - _Requirements: 1.6, 6.5_

- [x] 5. Implement data formatting module
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 7.1, 7.2, 7.3, 7.4, 7.5_

- [x] 5.1 Create WeatherFormatter class
  - Implement `WeatherFormatter` class in `formatter.py`
  - Initialize with WeatherConfig and IconMapper
  - Store configuration for separators and output fields
  - _Requirements: 2.3, 2.4_

- [x] 5.2 Implement field value extraction
  - Write `_get_field_value()` method to extract field values from WeatherData
  - Support standard field names (hour, icon, temp, precip, etc.)
  - Support custom field names by accessing raw_data dictionary
  - Handle missing fields gracefully (skip or use placeholder)
  - Format hour in 12-hour format (e.g., "1pm", "2pm")
  - Apply icon mapping for "icon" field
  - _Requirements: 2.5, 2.6, 2.7_

- [x] 5.3 Implement single entry formatting
  - Write `_format_entry()` method to format one forecast entry
  - Extract configured fields in order
  - Join field values with field separator
  - _Requirements: 2.2, 2.4_

- [x] 5.4 Implement complete output formatting
  - Write `format_output()` method to create full output string
  - Start with entry separator
  - Add current temperature
  - Add entry separator
  - Add each forecast entry with entry separator
  - End with entry separator
  - Apply preamble if configured
  - _Requirements: 2.1, 2.2, 7.1, 7.2, 7.3, 7.4, 7.5_

- [x] 5.5 Implement preamble application
  - Write `_apply_preamble()` method to prefix output with preamble string
  - Handle empty preamble (no prefix)
  - Support multi-character and special character preambles
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [x] 6. Implement CLI interface
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 6.1 Create argument parser
  - Implement `parse_arguments()` function in `cli.py` using argparse
  - Define all command-line arguments: --zipcode, --config, --hours, --day, --entry-sep, --field-sep, --fields, --preamble, --api-key, --help
  - Add short flags for common arguments (-z, -c, -h, -d, -e, -f, -p, -k)
  - Add help text for each argument
  - Set appropriate default values
  - _Requirements: 5.2, 5.4_

- [x] 6.2 Implement input validation
  - Validate zipcode format (5 digits for US)
  - Validate forecast_day value (today or tomorrow)
  - Validate forecast_hours is positive integer
  - Display clear error messages for invalid inputs
  - _Requirements: 5.5, 6.5_

- [x] 6.3 Implement main application flow
  - Write `main()` function as entry point
  - Load configuration from file
  - Parse command-line arguments
  - Merge configurations (CLI overrides file)
  - Validate final configuration
  - Create default config file if none exists
  - Initialize WeatherClient, IconMapper, and WeatherFormatter
  - Fetch weather data
  - Format output
  - Print output to stdout
  - Handle errors and return appropriate exit codes
  - _Requirements: 5.1, 5.3_

- [x] 7. Create documentation
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [x] 7.1 Write README.md
  - Add project overview and description
  - Add installation instructions (pip install, requirements)
  - Add quick start guide with example usage
  - Document all command-line arguments with examples
  - Document configuration file structure with examples
  - Add example outputs with different configurations
  - Include section on obtaining OpenWeatherMap API key
  - Add troubleshooting section for common issues
  - _Requirements: 8.1, 8.4, 8.5_

- [x] 7.2 Create example configuration file
  - Create `examples/example_config.yaml` with comprehensive comments
  - Show all available configuration options
  - Include multiple icon mapping examples
  - Include multiple output field combinations
  - _Requirements: 8.3_

- [x] 7.3 Add inline code documentation
  - Add docstrings to all classes and public methods
  - Include parameter descriptions and return types
  - Add usage examples in docstrings where helpful
  - _Requirements: 8.2_

- [x] 8. Write unit tests
  - Create `tests/` directory structure
  - Write unit tests for config module (YAML parsing, validation, merging)
  - Write unit tests for icon_mapper module (condition matching, defaults)
  - Write unit tests for formatter module (field extraction, output formatting, preamble)
  - Write unit tests for weather_client module with mocked API responses
  - Use pytest as testing framework
  - _Requirements: All requirements (validation)_

- [x] 9. Create integration tests
  - Write end-to-end test with mocked API
  - Test complete flow from CLI to output
  - Test config file + CLI override scenarios
  - Test error handling scenarios
  - _Requirements: All requirements (validation)_

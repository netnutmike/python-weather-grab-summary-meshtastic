# Changelog: API v3.0 Upgrade

## Version 2.0.0 - OpenWeatherMap API v3 Migration

**Release Date:** December 5, 2024

This is a major version release with breaking changes requiring user action.

### Breaking Changes

#### API Version Upgrade
- Upgraded from OpenWeatherMap API v2.5 to v3.0 (One Call API 3.0)
- **Requires subscription to One Call API 3.0** (free tier available with 1,000 calls/day)
- API endpoints changed from `/data/2.5/` to `/data/3.0/`

#### Location Input Changes
- Primary location input is now **latitude and longitude** instead of ZIP codes
- ZIP codes are still supported but are automatically converted to coordinates using the Geocoding API
- This adds one extra API call when using ZIP codes (first time only)

### New Features

#### Automatic ZIP Code Geocoding
- Added `geocode_zipcode()` method to `WeatherClient` class
- Automatically converts US ZIP codes to latitude/longitude coordinates
- Uses OpenWeatherMap's Geocoding API v1.0

#### Enhanced Configuration Options
- Added `latitude` and `longitude` fields to `WeatherConfig`
- Config file now supports both coordinate-based and ZIP code-based location input
- Command-line arguments now include `--lat` and `--lon` options

#### Improved Weather Data
- UV index now included in current weather data
- Dew point temperature now available
- Better visibility data
- Hourly forecasts for up to 48 hours (vs 5 days with 3-hour intervals)

### Modified Files

#### `weather_formatter/weather_client.py`
- Updated `WeatherClient.__init__()` to use API v3.0 endpoints
- Added `geo_url` attribute for Geocoding API
- Added `geocode_zipcode(zipcode: str) -> tuple[float, float]` method
- Modified `get_current_weather()` to accept `lat` and `lon` parameters instead of `zipcode`
- Modified `get_hourly_forecast()` to accept `lat` and `lon` parameters instead of `zipcode`
- Updated API response parsing to match One Call API 3.0 structure
- Changed error message from "Invalid zipcode" to "Location not found"

#### `weather_formatter/config.py`
- Added `latitude: Optional[float]` field to `WeatherConfig` dataclass
- Added `longitude: Optional[float]` field to `WeatherConfig` dataclass
- Updated `validate()` method to check for either lat/lon or zipcode
- Updated `load_config()` to parse latitude and longitude from YAML
- Updated `merge_config()` to handle latitude and longitude CLI arguments
- Updated `create_default_config()` to include latitude/longitude examples

#### `weather_formatter/cli.py`
- Added `--lat` / `--latitude` command-line argument
- Added `--lon` / `--longitude` command-line argument
- Updated help text to mention coordinate-based location input
- Modified `main()` to handle coordinate determination (direct or via geocoding)
- Updated `validate_cli_arguments()` to validate latitude and longitude ranges
- Added geocoding logic before fetching weather data

#### `examples/example_config.yaml`
- Added latitude and longitude configuration examples
- Updated comments to explain both location input methods
- Added note about One Call API 3.0 subscription requirement

#### `README.md`
- Updated installation prerequisites to mention One Call API 3.0 subscription
- Added latitude/longitude to Quick Start guide
- Updated command-line arguments documentation
- Added examples using coordinates
- Updated API key section to explain subscription requirement
- Updated troubleshooting section for new error messages

#### `TROUBLESHOOTING.md`
- Added "Migration from API v2.5 to v3.0" section at the top
- Updated "Invalid API key" troubleshooting to mention subscription requirement
- Changed "Invalid zipcode" to "Location not found" error
- Added migration steps and what changed documentation

#### `tests/test_weather_client.py`
- Updated `test_initialization()` to check for v3.0 endpoints
- Added `test_geocode_zipcode_success()` test
- Modified all weather client tests to use lat/lon instead of zipcode
- Updated mock response data to match One Call API 3.0 structure
- Changed "Invalid zipcode" test to "Location not found" test
- Updated API endpoint assertions from "weather"/"forecast" to "onecall"

### New Files

#### `MIGRATION_GUIDE.md`
- Comprehensive guide for upgrading from API v2.5 to v3.0
- Step-by-step migration instructions
- Troubleshooting tips
- Benefits of the new API version

#### `CHANGELOG_V3.md`
- This file - detailed changelog of all modifications

### API Endpoints

#### Old (v2.5)
- Current Weather: `https://api.openweathermap.org/data/2.5/weather`
- Forecast: `https://api.openweathermap.org/data/2.5/forecast`

#### New (v3.0)
- One Call API: `https://api.openweathermap.org/data/3.0/onecall`
- Geocoding: `http://api.openweathermap.org/geo/1.0/zip`

### Backward Compatibility

#### What Still Works
- ZIP code-based location input (automatically converted to coordinates)
- All existing configuration file formats
- All existing command-line arguments
- All output formats and customization options

#### What Requires Action
- **Must subscribe to One Call API 3.0** (even for free tier)
- API keys must have One Call API 3.0 access enabled

### Performance Considerations

#### Using ZIP Codes
- Requires 2 API calls: 1 for geocoding + 1 for weather data
- Geocoding result could be cached in future versions

#### Using Coordinates
- Requires 1 API call: just the weather data
- Slightly faster than ZIP code method

### Testing

All existing tests have been updated to work with the new API structure:
- Mock responses updated to match One Call API 3.0 format
- Test assertions updated for new endpoint URLs
- New test added for geocoding functionality

### Documentation Updates

All documentation has been updated to reflect:
- One Call API 3.0 subscription requirement
- Latitude/longitude as primary location input
- ZIP code auto-conversion feature
- New command-line arguments
- Updated examples and troubleshooting

### Migration Path

For users upgrading from v2.5:
1. Subscribe to One Call API 3.0 (free tier available)
2. No configuration changes required (ZIP codes still work)
3. Optionally switch to coordinates for better performance

See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for detailed instructions.

### Bug Fixes

#### Preamble Formatting Issue
- **Fixed:** Preamble now properly replaces initial separator instead of adding extra separator
- **Before:** No separator between preamble and first field
- **After:** `WEATHER:#76#1pm,9,75#` (preamble replaces initial separator)
- **Impact:** Clean, consistent formatting when preamble is used
- **Files Modified:** `weather_formatter/formatter.py`, `tests/test_formatter.py`

### Known Issues

None at this time.

### Future Enhancements

Potential improvements for future versions:
- Cache geocoding results to reduce API calls
- Support for international postal codes
- Support for city name-based location input
- Batch geocoding for multiple locations

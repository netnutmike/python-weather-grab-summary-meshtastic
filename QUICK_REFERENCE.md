# Quick Reference: API v3.0

## Command-Line Usage

### Using Coordinates
```bash
weather-formatter --lat 40.7128 --lon -74.0060 -k YOUR_API_KEY
```

### Using ZIP Code (Auto-Converted)
```bash
weather-formatter -z 10001 -k YOUR_API_KEY
```

### With Forecast Options
```bash
weather-formatter -z 10001 --hours 8 --day tomorrow
```

## Configuration File

### Using Coordinates
```yaml
api_key: "your_api_key_here"
latitude: 40.7128
longitude: -74.0060
forecast_hours: 5
forecast_day: "today"
```

### Using ZIP Code
```yaml
api_key: "your_api_key_here"
zipcode: "10001"
forecast_hours: 5
forecast_day: "today"
```

## API Requirements

- **API Version:** One Call API 3.0
- **Subscription:** Required (free tier: 1,000 calls/day)
- **Subscribe at:** https://openweathermap.org/api/one-call-3

## Location Input Methods

| Method | Config | CLI | API Calls | Speed |
|--------|--------|-----|-----------|-------|
| Coordinates | `latitude` + `longitude` | `--lat` + `--lon` | 1 | Faster |
| ZIP Code | `zipcode` | `-z` | 2 | Slightly slower |

## Common Commands

### Test Configuration
```bash
weather-formatter -v
```

### Override Config File
```bash
weather-formatter --config my_config.yaml -z 90210
```

### Custom Output Format
```bash
weather-formatter -z 10001 --fields hour,icon,temp,humidity --entry-sep "|"
```

## Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "api_key is required" | No API key provided | Add to config or use `-k` flag |
| "Invalid API key" | Not subscribed to One Call API 3.0 | Subscribe at openweathermap.org |
| "Location not found" | Invalid coordinates or ZIP | Check lat/lon ranges or ZIP format |
| "Rate limit exceeded" | Too many API calls | Wait or upgrade plan |

## Coordinate Ranges

- **Latitude:** -90 to 90 (negative = South, positive = North)
- **Longitude:** -180 to 180 (negative = West, positive = East)

## Examples

### New York City
```yaml
latitude: 40.7128
longitude: -74.0060
# OR
zipcode: "10001"
```

### Los Angeles
```yaml
latitude: 34.0522
longitude: -118.2437
# OR
zipcode: "90001"
```

### Chicago
```yaml
latitude: 41.8781
longitude: -87.6298
# OR
zipcode: "60601"
```

## Find Your Coordinates

1. **From ZIP Code:** Run the app once with `-v` flag and your ZIP code
2. **Online Tool:** https://www.latlong.net/
3. **Google Maps:** Right-click any location → "What's here?"

## Output Format

Default output structure:
```
[preamble][sep][current_temp][sep][hour,icon,temp,precip][sep]...
```

Note: If a preamble is specified, it replaces the initial entry separator.

Example without preamble:
```
#76#1pm,9,75,0.0#2pm,9,76,0.0#3pm,9,76,0.0#
```

Example with preamble "WEATHER:":
```
WEATHER:#76#1pm,9,75,0.0#2pm,9,76,0.0#3pm,9,76,0.0#
```

## Available Output Fields

- `hour` - Hour (12-hour format)
- `icon` - Weather icon code
- `temp` - Temperature
- `feels_like` - Feels-like temperature
- `precip` - Precipitation amount (mm/hour)
- `precip_probability` - Precipitation probability (0-100%)
- `humidity` - Humidity percentage
- `wind_speed` - Wind speed
- `wind_direction` - Wind direction (degrees)
- `pressure` - Atmospheric pressure
- `uv_index` - UV index (NEW in v3.0)
- `visibility` - Visibility distance
- `dew_point` - Dew point (NEW in v3.0)

## Help Commands

```bash
weather-formatter --help          # Show all options
weather-formatter -v              # Verbose mode
```

## Documentation Files

- `README.md` - Full documentation
- `MIGRATION_GUIDE.md` - Upgrade instructions
- `TROUBLESHOOTING.md` - Problem solving
- `CHANGELOG_V3.md` - Complete change list
- `UPGRADE_SUMMARY.md` - Quick upgrade overview

# API v3.0 Upgrade Summary

## Quick Overview

Your weather grabber has been successfully upgraded from OpenWeatherMap API v2.5 to v3.0 (One Call API 3.0).

## What You Need to Do

### 1. Subscribe to One Call API 3.0 (Required)
- Go to: https://openweathermap.org/api/one-call-3
- Click "Subscribe" and select the **free tier** (1,000 calls/day)
- Wait a few minutes for activation
- Your existing API key will work after subscription

### 2. Choose Your Location Input Method

**Option A: Keep Using ZIP Codes (No Changes Needed)**
```yaml
# weather_config.yaml
zipcode: "10001"
```
The app will automatically convert ZIP codes to coordinates.

**Option B: Use Coordinates Directly (Slightly Faster)**
```yaml
# weather_config.yaml
latitude: 40.7128
longitude: -74.0060
```

## Key Changes

### What's New
✅ Hourly forecasts for 48 hours (vs 3-hour intervals)  
✅ UV index and dew point data  
✅ Automatic ZIP code to coordinate conversion  
✅ More accurate weather data  
✅ New command-line options: `--lat` and `--lon`

### What's Different
⚠️ Requires One Call API 3.0 subscription (free tier available)  
⚠️ Uses latitude/longitude internally (ZIP codes auto-converted)  
⚠️ API endpoints changed (handled automatically)

### What Still Works
✓ All existing ZIP codes  
✓ All configuration files  
✓ All command-line arguments  
✓ All output formats  
✓ All customization options

## Files Modified

- `weather_formatter/weather_client.py` - Updated to use API v3.0
- `weather_formatter/config.py` - Added lat/lon support
- `weather_formatter/cli.py` - Added lat/lon command-line options
- `examples/example_config.yaml` - Updated with lat/lon examples
- `README.md` - Updated documentation
- `TROUBLESHOOTING.md` - Added migration section
- `tests/test_weather_client.py` - Updated tests for API v3.0

## New Files

- `MIGRATION_GUIDE.md` - Detailed migration instructions
- `CHANGELOG_V3.md` - Complete list of changes
- `UPGRADE_SUMMARY.md` - This file

## Testing Your Setup

Run with verbose mode to verify everything works:

```bash
weather-formatter -v
```

Expected output:
```
Geocoding zipcode: 10001
Geocoded to: lat=40.7128, lon=-74.0060
Fetching current weather for lat=40.7128, lon=-74.0060
Current temperature: 75.0°F
Retrieved 5 forecast entries
```

## Need Help?

- **Migration Guide:** See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)
- **Troubleshooting:** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Full Changelog:** See [CHANGELOG_V3.md](CHANGELOG_V3.md)

## Benefits of Upgrading

1. **Better Data:** Hourly forecasts instead of 3-hour intervals
2. **More Features:** UV index, dew point, better visibility
3. **Flexibility:** Use ZIP codes OR coordinates
4. **Efficiency:** Single API call for current + forecast data
5. **Future-Proof:** Latest API version with ongoing support

## Bottom Line

**For most users:** Just subscribe to One Call API 3.0 and keep using your existing config. Everything else works the same!

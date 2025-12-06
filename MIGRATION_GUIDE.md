# Migration Guide: API v2.5 to v3.0

This guide will help you upgrade from OpenWeatherMap API v2.5 to v3.0 (One Call API 3.0).

## What Changed

### API Version
- **Old:** OpenWeatherMap API v2.5 (Current Weather & 5-day Forecast)
- **New:** OpenWeatherMap API v3.0 (One Call API 3.0)

### Location Input
- **Old:** ZIP codes only (`zipcode: "10001"`)
- **New:** Latitude and longitude coordinates (ZIP codes are automatically converted)

### API Subscription
- **Old:** Free tier with no subscription required
- **New:** Requires One Call API 3.0 subscription (free tier available with 1,000 calls/day)

### Forecast Data
- **Old:** 5-day forecast with 3-hour intervals
- **New:** Hourly forecast for 48 hours (more granular data)

### Additional Features
- **New:** UV index, dew point, and better visibility data
- **New:** Automatic ZIP code to coordinate conversion using Geocoding API

## Migration Steps

### Step 1: Subscribe to One Call API 3.0

1. Go to https://openweathermap.org/api/one-call-3
2. Click "Subscribe" 
3. Select the **free tier** (1,000 calls/day)
4. Wait a few minutes for the subscription to activate

**Important:** Even the free tier requires you to click "Subscribe". Your existing API key will work once you've subscribed.

### Step 2: Update Your Configuration (Optional)

You have two options for specifying location:

#### Option 1: Keep Using ZIP Codes (Easiest)

No changes needed! The application will automatically convert ZIP codes to coordinates:

```yaml
# weather_config.yaml
api_key: "your_api_key_here"
zipcode: "10001"  # Still works!
```

#### Option 2: Use Coordinates Directly (Slightly Faster)

For slightly better performance, you can specify coordinates directly:

```yaml
# weather_config.yaml
api_key: "your_api_key_here"
latitude: 40.7128
longitude: -74.0060
```

To find coordinates for your location:
- Use https://www.latlong.net/
- Or run the app once with a ZIP code and check the verbose output

### Step 3: Update Command-Line Usage (If Applicable)

If you use command-line arguments, you can now use coordinates:

**Old way (still works):**
```bash
weather-formatter -z 10001 -k YOUR_API_KEY
```

**New way (optional):**
```bash
weather-formatter --lat 40.7128 --lon -74.0060 -k YOUR_API_KEY
```

### Step 4: Test Your Setup

Run the application with verbose mode to verify everything works:

```bash
weather-formatter -v
```

You should see output like:
```
Geocoding zipcode: 10001
Geocoded to: lat=40.7128, lon=-74.0060
Fetching current weather for lat=40.7128, lon=-74.0060
Current temperature: 75.0°F
```

## Troubleshooting

### "Invalid API key" Error

**Cause:** You haven't subscribed to One Call API 3.0 yet.

**Solution:**
1. Go to https://openweathermap.org/api/one-call-3
2. Click "Subscribe" and select the free tier
3. Wait a few minutes and try again

### "Location not found" Error

**Cause:** Invalid coordinates or ZIP code.

**Solution:**
- Verify your ZIP code is a valid 5-digit US ZIP code
- If using coordinates, ensure latitude is between -90 and 90, longitude between -180 and 180

### Slower Performance

**Cause:** Using ZIP codes requires an extra API call to convert to coordinates.

**Solution:** Switch to using latitude/longitude directly in your config file.

## API Call Usage

### Before (API v2.5)
- 1 call for current weather
- 1 call for forecast
- **Total: 2 calls per run**

### After (API v3.0)
- 1 call for geocoding (if using ZIP code, cached after first use)
- 1 call for current weather + forecast (combined in One Call API)
- **Total: 1-2 calls per run**

The new API is actually more efficient if you use coordinates directly!

## Benefits of API v3.0

1. **Better Forecast Data:** Hourly forecasts for 48 hours instead of 3-hour intervals
2. **More Weather Data:** UV index, dew point, and improved visibility data
3. **Single API Call:** Current weather and forecast in one request
4. **Flexible Location:** Use either ZIP codes or coordinates
5. **Better Accuracy:** More precise weather data

## Rollback (If Needed)

If you need to rollback to the old version:

```bash
git checkout <previous-commit-hash>
```

However, we recommend staying on v3.0 for better data and features.

## Need Help?

See the [TROUBLESHOOTING.md](TROUBLESHOOTING.md) file for detailed troubleshooting steps.

## Summary

The migration is straightforward:
1. Subscribe to One Call API 3.0 (free tier available)
2. Keep using ZIP codes OR switch to coordinates
3. Enjoy better weather data!

No code changes or complex configuration updates required.

# Troubleshooting Guide

## Migration from API v2.5 to v3.0

**Important:** This application now uses OpenWeatherMap's One Call API 3.0, which requires:
1. A subscription (free tier available with 1,000 calls/day)
2. Latitude and longitude coordinates (ZIP codes are automatically converted)

### What Changed

- **API Version:** Upgraded from v2.5 to v3.0 (One Call API)
- **Location Input:** Now uses latitude/longitude instead of ZIP codes directly
- **Auto-Conversion:** ZIP codes are automatically converted to coordinates using the Geocoding API
- **Subscription Required:** One Call API 3.0 requires a subscription (free tier available)
- **Better Forecasts:** Hourly forecasts for 48 hours (vs 5 days with 3-hour intervals)

### Migration Steps

1. **Subscribe to One Call API 3.0:**
   - Go to https://openweathermap.org/api/one-call-3
   - Click "Subscribe" and select the free tier
   - Wait a few minutes for activation

2. **Update Your Config (Optional):**
   - You can keep using ZIP codes (they'll be auto-converted)
   - Or switch to lat/lon for slightly faster performance:
   ```yaml
   # Option 1: Keep using ZIP code (auto-converted)
   zipcode: "10001"
   
   # Option 2: Use coordinates directly
   latitude: 40.7128
   longitude: -74.0060
   ```

3. **No Code Changes Needed:** The application handles everything automatically

## "Invalid API Key" Error

If you're getting an "Invalid API key" error, follow these steps:

### Step 1: Test Your API Key

Run the diagnostic script to check if your API key is valid:

```bash
python test_api_key.py YOUR_API_KEY_HERE
```

Or if you have a config file:

```bash
python test_api_key.py $(grep 'api_key:' weather_config.yaml | cut -d':' -f2 | tr -d ' "')
```

### Step 2: Common Issues and Solutions

#### Issue 1: API Key Not Activated Yet

**Symptom:** You just created the API key
**Solution:** New OpenWeatherMap API keys can take **1-2 hours** to activate. Wait and try again later.

#### Issue 2: Extra Quotes or Spaces in Config File

**Symptom:** Config file has quotes around the API key
**Wrong:**
```yaml
api_key: "abc123def456"
```

**Correct:**
```yaml
api_key: abc123def456
```

Or if you must use quotes, make sure the CLI doesn't add extra ones:
```bash
# Wrong - adds extra quotes
weather-formatter -k "abc123"

# Correct
weather-formatter -k abc123
```

#### Issue 3: Wrong API Key

**Symptom:** Copied the wrong value from OpenWeatherMap
**Solution:** 
1. Go to https://home.openweathermap.org/api_keys
2. Copy the **API key** (not the API secret)
3. It should be a 32-character hexadecimal string

#### Issue 4: Not Subscribed to One Call API 3.0

**Symptom:** API key works for other OpenWeatherMap services but not this app
**Solution:** This application uses the One Call API 3.0, which requires a subscription:
1. Go to https://openweathermap.org/api/one-call-3
2. Click "Subscribe" and select the free tier (1,000 calls/day)
3. Wait a few minutes for the subscription to activate
4. Try again

The free tier includes:
- Current weather data
- Hourly forecast for 48 hours
- Daily forecast for 8 days
- 1,000 API calls per day

### Step 3: Verify Your Configuration

Check your `weather_config.yaml` file:

```bash
cat weather_config.yaml
```

Make sure it looks like this (with your actual values):

```yaml
api_key: your_actual_32_character_key_here

# Location (use either lat/lon or zipcode)
latitude: 40.7128
longitude: -74.0060
# OR
zipcode: "10001"

forecast_hours: 5
forecast_day: "today"
# ... rest of config
```

### Step 4: Test with Command Line Override

Try running with the API key directly on the command line:

```bash
# Create a minimal config first
python -m weather_formatter.cli --config weather_config.yaml

# Then override with your API key and location
python -m weather_formatter.cli --config weather_config.yaml -k YOUR_API_KEY -z 10001

# Or use coordinates directly
python -m weather_formatter.cli --config weather_config.yaml -k YOUR_API_KEY --lat 40.7128 --lon -74.0060
```

### Step 5: Enable Verbose Logging

Run with verbose mode to see more details:

```bash
python -m weather_formatter.cli --config weather_config.yaml -v
```

This will show you:
- What configuration is being loaded
- What API calls are being made
- More detailed error messages

## Still Having Issues?

If none of the above solutions work, please provide:

1. The output of the diagnostic script:
   ```bash
   python test_api_key.py YOUR_API_KEY
   ```

2. The exact command you're running

3. The full error message

4. Your config file (with API key masked):
   ```bash
   cat weather_config.yaml | sed 's/api_key:.*/api_key: [MASKED]/'
   ```

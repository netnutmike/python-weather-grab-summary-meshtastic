# Troubleshooting Guide

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

#### Issue 4: Using Free Tier with Wrong Endpoint

**Symptom:** API key works for some endpoints but not others
**Solution:** The free tier only supports certain endpoints. This app uses:
- `/weather` - Current weather (✅ Free tier)
- `/forecast` - 5-day forecast (✅ Free tier)

### Step 3: Verify Your Configuration

Check your `weather_config.yaml` file:

```bash
cat weather_config.yaml
```

Make sure it looks like this (with your actual values):

```yaml
api_key: your_actual_32_character_key_here
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

# Then override with your API key
python -m weather_formatter.cli --config weather_config.yaml -k YOUR_API_KEY -z 10001
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

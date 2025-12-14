# Local Setup Guide

This guide will help you set up and run the Weather Formatter locally on your machine.

## Prerequisites

- **Python 3.8+** (check with `python3 --version`)
- **pip3** (Python package manager)
- **OpenWeatherMap API Key** with One Call API 3.0 subscription

## Quick Setup Options

### Option 1: Automated Shell Script (Recommended)

```bash
# Make executable and run
chmod +x install_and_run.sh
./install_and_run.sh
```

### Option 2: Python Runner Script

```bash
# Run the Python setup script
python3 run_weather.py
```

### Option 3: Makefile Commands

```bash
# Install and setup
make setup

# Run the application
make run
```

### Option 4: Manual Installation

```bash
# Install dependencies
pip3 install -r requirements.txt

# Install package in development mode
pip3 install -e .

# Create default config
weather-formatter

# Edit config with your API key
nano weather_config.yaml

# Run the application
weather-formatter
```

## Configuration

### 1. Get API Key

1. Go to https://openweathermap.org/api/one-call-3
2. Sign up for an account
3. **Subscribe to One Call API 3.0** (free tier: 1,000 calls/day)
4. Copy your API key

### 2. Configure Location

Edit `weather_config.yaml`:

**Option A: Use ZIP Code (easier)**
```yaml
api_key: "your_api_key_here"
zipcode: "10001"
```

**Option B: Use Coordinates (faster)**
```yaml
api_key: "your_api_key_here"
latitude: 40.7128
longitude: -74.0060
```

## Running the Application

### Basic Usage

```bash
# Run with config file
weather-formatter

# Run with command line options
weather-formatter -z 10001 -k YOUR_API_KEY

# Run with coordinates
weather-formatter --lat 40.7128 --lon -74.0060 -k YOUR_API_KEY
```

### Advanced Usage

```bash
# Verbose mode (for debugging)
weather-formatter -v

# Custom output format
weather-formatter --fields hour,icon,temp,humidity --entry-sep "|"

# Tomorrow's forecast
weather-formatter --day tomorrow --hours 8

# Custom preamble
weather-formatter --preamble "WEATHER:"
```

## Example Output

```bash
$ weather-formatter
#76#1pm,9,75,0.0#2pm,9,76,0.0#3pm,9,76,0.0#4pm,9,75,0.0#5pm,9,74,0.0#
```

With preamble:
```bash
$ weather-formatter --preamble "WX:"
WX:#76#1pm,9,75,0.0#2pm,9,76,0.0#3pm,9,76,0.0#
```

## Troubleshooting

### "No module named 'yaml'" Error

```bash
pip3 install PyYAML
```

### "Invalid API key" Error

1. Verify your API key is correct
2. **Make sure you've subscribed to One Call API 3.0**
3. Wait a few minutes for new keys to activate

### "Location not found" Error

- Check ZIP code is valid 5-digit US ZIP
- Verify coordinates are in valid ranges (lat: -90 to 90, lon: -180 to 180)

### Import Errors

```bash
# Reinstall in development mode
pip3 install -e . --force-reinstall
```

## Development Commands

### Testing

```bash
# Run syntax check
make check

# Run tests (if pytest installed)
make test

# Manual syntax check
python3 -m py_compile weather_formatter/*.py
```

### Cleaning

```bash
# Clean build artifacts
make clean

# Or manually
rm -rf build/ dist/ *.egg-info/ __pycache__/
```

## File Structure

```
weather-formatter/
├── weather_formatter/          # Main package
│   ├── __init__.py
│   ├── cli.py                 # Command-line interface
│   ├── config.py              # Configuration management
│   ├── weather_client.py      # API client
│   ├── formatter.py           # Output formatting
│   └── icon_mapper.py         # Weather icon mapping
├── tests/                     # Test suite
├── examples/                  # Example configurations
├── weather_config.yaml        # Your configuration
├── requirements.txt           # Dependencies
├── setup.py                  # Package setup
├── run_weather.py            # Python runner script
├── install_and_run.sh        # Shell setup script
└── Makefile                  # Make commands
```

## Integration Examples

### Shell Script Integration

```bash
#!/bin/bash
WEATHER=$(weather-formatter)
echo "Current weather: $WEATHER"
```

### Python Integration

```python
import subprocess

# Run and capture output
result = subprocess.run(['weather-formatter'], capture_output=True, text=True)
weather_data = result.stdout.strip()
print(f"Weather: {weather_data}")
```

### Cron Job Example

```bash
# Add to crontab (crontab -e)
# Run every hour
0 * * * * /usr/local/bin/weather-formatter >> /var/log/weather.log 2>&1
```

## Performance Tips

1. **Use coordinates instead of ZIP codes** for faster response
2. **Cache results** if calling frequently
3. **Use appropriate forecast_hours** (don't request more than needed)

## Support

- **Documentation:** README.md
- **Migration Guide:** MIGRATION_GUIDE.md  
- **Troubleshooting:** TROUBLESHOOTING.md
- **API Reference:** QUICK_REFERENCE.md

## Version Information

- **Current Version:** 2.1.0
- **API Version:** OpenWeatherMap One Call API 3.0
- **Python Requirements:** 3.8+
# 🌤️ Run Weather Formatter Locally

## Quick Start (Choose One Method)

### Method 1: Automated Setup Script ⚡
```bash
./install_and_run.sh
```

### Method 2: Python Runner 🐍
```bash
python3 run_weather.py
```

### Method 3: Make Commands 🔨
```bash
make setup    # Install and create config
make run      # Run the application
```

### Method 4: Manual Steps 🛠️
```bash
pip3 install -r requirements.txt
pip3 install -e .
weather-formatter
```

## Prerequisites Check

Run this first to check your system:
```bash
python3 check_requirements.py
```

## Configuration

1. **Get API Key**: https://openweathermap.org/api/one-call-3
2. **Subscribe** to One Call API 3.0 (free tier available)
3. **Edit** `weather_config.yaml` with your API key and location

## Example Usage

```bash
# Basic usage
weather-formatter

# With ZIP code
weather-formatter -z 10001 -k YOUR_API_KEY

# With coordinates  
weather-formatter --lat 40.7128 --lon -74.0060 -k YOUR_API_KEY

# Custom format
weather-formatter --preamble "WX:" --fields hour,icon,temp
```

## Output Example

```
WX:#76#1pm,9,75,0.0#2pm,9,76,0.0#3pm,9,76,0.0#
```

## Troubleshooting

- **Missing dependencies**: `pip3 install -r requirements.txt`
- **Invalid API key**: Subscribe to One Call API 3.0
- **Import errors**: `pip3 install -e . --force-reinstall`

## Files Created

- `install_and_run.sh` - Automated setup script
- `run_weather.py` - Python runner script  
- `check_requirements.py` - System requirements checker
- `Makefile` - Make commands for development
- `LOCAL_SETUP.md` - Detailed setup guide

## Need Help?

- 📖 **Full Guide**: LOCAL_SETUP.md
- 🔧 **Troubleshooting**: TROUBLESHOOTING.md
- 📚 **Documentation**: README.md
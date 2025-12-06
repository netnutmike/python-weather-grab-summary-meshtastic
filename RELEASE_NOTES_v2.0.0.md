# Release Notes - Version 2.0.0

**Release Date:** December 5, 2024

## Overview

Weather Formatter 2.0.0 is a major release that upgrades the application to use OpenWeatherMap's One Call API 3.0, providing better weather data and more features while maintaining backward compatibility with existing configurations.

## 🚨 Breaking Changes

### API Subscription Required
- **Action Required:** Subscribe to One Call API 3.0 (free tier available)
- **Why:** OpenWeatherMap's One Call API 3.0 requires a subscription
- **Free Tier:** 1,000 API calls per day
- **How to Subscribe:** https://openweathermap.org/api/one-call-3

### API Version Upgrade
- Upgraded from API v2.5 to v3.0 (One Call API)
- Internal endpoints changed (handled automatically)
- No code changes required for end users

## ✨ New Features

### 1. Automatic ZIP Code Geocoding
- ZIP codes are automatically converted to latitude/longitude coordinates
- Uses OpenWeatherMap's Geocoding API
- Seamless experience - no configuration changes needed

### 2. Direct Coordinate Support
- New command-line options: `--lat` and `--lon`
- New config fields: `latitude` and `longitude`
- Slightly faster than ZIP code method (skips geocoding step)

### 3. Enhanced Weather Data
- **UV Index:** Now included in weather data
- **Dew Point:** Temperature at which dew forms
- **Better Visibility:** More accurate visibility data
- **Hourly Forecasts:** Up to 48 hours (vs 5 days with 3-hour intervals)

### 4. Improved Output Formatting
- Fixed: Entry separator now added after preamble for consistent parsing
- Example: `WEATHER:##76#1pm,9,75#` (separator after "WEATHER:")

## 🔧 Configuration Changes

### New Configuration Options

```yaml
# Option 1: Use coordinates directly (recommended)
latitude: 40.7128
longitude: -74.0060

# Option 2: Use ZIP code (auto-converted)
zipcode: "10001"
```

### Command-Line Options

```bash
# New: Use coordinates
weather-formatter --lat 40.7128 --lon -74.0060 -k YOUR_API_KEY

# Still works: Use ZIP code
weather-formatter -z 10001 -k YOUR_API_KEY
```

## 📊 Performance

### API Call Efficiency

**Using Coordinates:**
- 1 API call per run (weather data only)
- Recommended for best performance

**Using ZIP Codes:**
- 2 API calls per run (geocoding + weather data)
- Still efficient, automatic conversion

**Compared to v1.0.0:**
- Same or better efficiency
- More data in single call (current + forecast combined)

## 🐛 Bug Fixes

### Preamble Formatting
- **Issue:** No separator between preamble and first data field
- **Fixed:** Entry separator now added after preamble
- **Impact:** Consistent parsing when using preamble option

## 📦 Installation

### New Installation
```bash
pip install weather-formatter
```

### Upgrade from 1.x
```bash
pip install --upgrade weather-formatter
```

## 🔄 Migration Guide

### Quick Migration (3 Steps)

1. **Subscribe to One Call API 3.0**
   - Visit: https://openweathermap.org/api/one-call-3
   - Click "Subscribe" and select free tier
   - Wait a few minutes for activation

2. **Update Package**
   ```bash
   pip install --upgrade weather-formatter
   ```

3. **Test Your Setup**
   ```bash
   weather-formatter -v
   ```

### No Configuration Changes Required
- Existing ZIP code configurations work automatically
- Existing command-line arguments work as before
- All output formats remain compatible

### Optional: Switch to Coordinates
For slightly better performance, update your config:

```yaml
# Before (still works)
zipcode: "10001"

# After (optional, faster)
latitude: 40.7128
longitude: -74.0060
```

## 📚 Documentation

### Updated Documentation
- [README.md](README.md) - Complete usage guide
- [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) - Detailed migration steps
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues and solutions
- [CHANGELOG_V3.md](CHANGELOG_V3.md) - Complete list of changes

### New Documentation
- [VERSION.md](VERSION.md) - Version information and history
- [UPGRADE_SUMMARY.md](UPGRADE_SUMMARY.md) - Quick upgrade overview
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Command reference card

## 🧪 Testing

### Test Coverage
- All existing tests updated for API v3.0
- New tests added for geocoding functionality
- Mock responses updated to match One Call API structure

### Validation
```bash
# Run tests (if pytest installed)
pytest tests/

# Verify installation
python3 -c "import weather_formatter; print(weather_formatter.__version__)"
# Output: 2.0.0
```

## 🔮 Future Enhancements

Potential features for future releases:
- Cache geocoding results to reduce API calls
- Support for international postal codes
- City name-based location input
- Batch processing for multiple locations

## ⚠️ Known Issues

None at this time.

## 🆘 Support

### Getting Help
- **Migration Issues:** See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)
- **Troubleshooting:** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **API Questions:** Visit https://openweathermap.org/api

### Common Questions

**Q: Do I need to change my configuration?**
A: No, ZIP codes still work automatically.

**Q: Is the free tier still available?**
A: Yes, 1,000 API calls per day with One Call API 3.0.

**Q: Will my existing scripts break?**
A: No, all existing configurations and commands work as before.

**Q: How do I find coordinates for my location?**
A: Run once with `-v` flag and your ZIP code, or use https://www.latlong.net/

## 📝 Credits

Thanks to all contributors and users who provided feedback during development.

## 📄 License

This project maintains its existing license. See LICENSE file for details.

---

**Version:** 2.0.0  
**Release Date:** December 5, 2024  
**Previous Version:** 1.0.0  
**API Version:** OpenWeatherMap One Call API 3.0

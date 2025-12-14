# Release Notes - Version 2.1.0

**Release Date:** December 7, 2024

## Overview

Weather Formatter 2.1.0 is a minor release that adds new features, fixes bugs, and improves the development experience. This release maintains full backward compatibility with 2.0.0 while adding enhanced precipitation data and better local development tools.

## 🆕 New Features

### Enhanced Precipitation Data

#### Dual Precipitation Fields
- **New Field:** `precip_probability` - Precipitation probability (0-100%) for forecasts
- **Consistent Data:** `precip` field now uses mm/hour for both current weather and forecasts
- **Backward Compatible:** Existing configurations continue to work

**Usage Examples:**
```yaml
# Use precipitation amount (recommended)
output_fields: ["hour", "icon", "temp", "precip"]

# Use precipitation probability  
output_fields: ["hour", "icon", "temp", "precip_probability"]

# Use both
output_fields: ["hour", "icon", "temp", "precip", "precip_probability"]
```

### Improved Weather Icon Mappings

Enhanced icon mappings for better weather categorization:

| Condition | Old Icon | New Icon | Reason |
|-----------|----------|----------|---------|
| Light rain/drizzle | `2` | `7` | Better consistency with moderate rain |
| Sleet conditions | `8` | `3` | Distinguish from snow |
| Light snow showers | `8` | `2` | Distinguish from heavy snow |
| Tornado | `;` | `<` | More distinctive symbol |

### Local Development Tools

New tools for easier local setup and development:

1. **`install_and_run.sh`** - One-command setup script
2. **`run_weather.py`** - Python-based installer and runner  
3. **`check_requirements.py`** - System requirements checker
4. **`Makefile`** - Development commands (`make setup`, `make run`, etc.)
5. **`LOCAL_SETUP.md`** - Comprehensive setup guide
6. **`RUN_LOCALLY.md`** - Quick start reference

## 🐛 Bug Fixes

### Preamble Formatting Fix
- **Issue:** Double separator after preamble (`WEATHER:##76#`)
- **Fixed:** Single separator after preamble (`WEATHER:#76#`)
- **Impact:** Cleaner output formatting and easier parsing

### Precipitation Data Consistency
- **Issue:** Current weather used amounts, forecasts used probabilities
- **Fixed:** Both now use consistent precipitation amounts (mm/hour)
- **Added:** Separate probability field for those who need it

## 🔧 Improvements

### Documentation Enhancements
- Enhanced configuration documentation
- Better API v3.0 subscription guidance
- Improved troubleshooting sections
- Multiple installation method guides

### Developer Experience
- Multiple setup methods for different preferences
- Better error messages and validation
- Comprehensive local development tools
- Improved testing and validation scripts

## 📦 Installation & Upgrade

### New Installation (Multiple Options)

**Option 1: Automated Script**
```bash
./install_and_run.sh
```

**Option 2: Python Runner**
```bash
python3 run_weather.py
```

**Option 3: Make Commands**
```bash
make setup && make run
```

**Option 4: Traditional**
```bash
pip install weather-formatter
```

### Upgrade from 2.0.0

```bash
pip install --upgrade weather-formatter
```

No configuration changes required - fully backward compatible!

## 🔄 Migration Notes

### From 2.0.0 to 2.1.0
- **No breaking changes** - fully backward compatible
- **Optional:** Update icon mappings if you use custom ones
- **Optional:** Use new `precip_probability` field if needed

### Configuration Compatibility
All existing 2.0.0 configurations work without changes:
- ✅ All command-line arguments
- ✅ All configuration file formats  
- ✅ All output field names
- ✅ All icon mappings (with improvements)

## 📊 What's Changed

### Files Modified
- `weather_formatter/weather_client.py` - Added precipitation probability support
- `weather_formatter/formatter.py` - Fixed preamble formatting, added new field support
- `weather_formatter/icon_mapper.py` - Enhanced weather condition mappings
- `weather_formatter/config.py` - Improved documentation
- `tests/test_icon_mapper.py` - Updated for new icon mappings

### Files Added
- `install_and_run.sh` - Automated setup script
- `run_weather.py` - Python installer/runner
- `check_requirements.py` - Requirements checker
- `Makefile` - Development commands
- `LOCAL_SETUP.md` - Setup guide
- `RUN_LOCALLY.md` - Quick reference
- `RELEASE_NOTES_v2.1.0.md` - This file

## 🧪 Testing

### Validation
- ✅ All existing tests pass
- ✅ New precipitation fields work correctly
- ✅ Icon mappings function properly
- ✅ Preamble formatting fixed
- ✅ Local installation scripts tested

### Compatibility Testing
- ✅ Existing 2.0.0 configs work unchanged
- ✅ All command-line arguments compatible
- ✅ Output format maintains compatibility
- ✅ API integration unchanged

## 🔮 Looking Ahead

### Potential Future Features
- Geocoding result caching
- International postal code support
- City name-based location input
- Batch processing capabilities
- Configuration validation tools

## 📝 Technical Details

### API Compatibility
- **API Version:** OpenWeatherMap One Call API 3.0 (unchanged)
- **Python Requirements:** 3.8+ (unchanged)
- **Dependencies:** PyYAML, requests, python-dateutil (unchanged)

### Performance
- **No performance impact** from new features
- **Slightly faster** icon mapping with improved logic
- **Same API call efficiency** as 2.0.0

## 🆘 Support & Documentation

### Updated Documentation
- [README.md](README.md) - Complete usage guide
- [LOCAL_SETUP.md](LOCAL_SETUP.md) - Local development setup
- [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) - API v3 migration guide
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Command reference

### Getting Help
- **Setup Issues:** See LOCAL_SETUP.md
- **API Problems:** See TROUBLESHOOTING.md  
- **Feature Questions:** See README.md

## 🎉 Acknowledgments

Thanks to all users who provided feedback and helped improve the Weather Formatter!

---

**Version:** 2.1.0  
**Release Date:** December 7, 2024  
**Previous Version:** 2.0.0  
**Compatibility:** Fully backward compatible with 2.0.0
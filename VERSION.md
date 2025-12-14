# Version Information

## Current Version: 2.1.0

**Release Date:** December 5, 2024

## Version History

### 2.1.0 (Current) - December 7, 2024
**Minor Release - Enhanced Features and Bug Fixes**

#### New Features
- Added `precip_probability` field for precipitation probability data
- Enhanced icon mappings with better precipitation categorization
- Improved local setup scripts and installation methods

#### Bug Fixes
- Fixed preamble formatting (now single separator after preamble)
- Fixed precipitation data consistency (both current and forecast use mm/hour)

#### Improvements
- Better documentation and setup guides
- Enhanced error messages and troubleshooting
- Improved icon mappings for weather conditions

---

### 2.0.0 - December 5, 2024
**Major Release - API v3.0 Migration**

#### Breaking Changes
- Upgraded to OpenWeatherMap API v3.0 (One Call API)
- Requires One Call API 3.0 subscription (free tier available)
- Primary location input changed to latitude/longitude (ZIP codes auto-converted)

#### New Features
- Automatic ZIP code to coordinate geocoding
- Enhanced weather data (UV index, dew point)
- Hourly forecasts for 48 hours
- Command-line support for lat/lon coordinates (`--lat`, `--lon`)

#### Bug Fixes
- Added entry separator after preamble for consistent formatting

#### Migration Required
Users must subscribe to One Call API 3.0 to continue using this version.
See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for details.

---

### 1.0.0 - Previous Release
**Stable Release - API v2.5**

- Used OpenWeatherMap API v2.5
- ZIP code-based location input
- 5-day forecast with 3-hour intervals
- No subscription required for free tier

---

## Version Numbering

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR** version (2.x.x) - Incompatible API changes
- **MINOR** version (x.1.x) - Backwards-compatible functionality additions
- **PATCH** version (x.x.1) - Backwards-compatible bug fixes

## Checking Your Version

### Command Line
```bash
weather-formatter --version  # (if implemented)
```

### Python
```python
import weather_formatter
print(weather_formatter.__version__)
```

### Package Files
- `setup.py` - Line 11: `version="2.1.0"`
- `weather_formatter/__init__.py` - Line 28: `__version__ = "2.1.0"`

## Upgrade Path

### From 1.x to 2.0
1. Subscribe to One Call API 3.0
2. Update your installation: `pip install --upgrade weather-formatter`
3. No configuration changes required (ZIP codes still work)
4. See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for details

## Support

- **Version 2.1.0:** Actively supported
- **Version 1.0.0:** Legacy support (API v2.5 may be deprecated by OpenWeatherMap)

## Documentation

- [README.md](README.md) - Full documentation
- [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) - Upgrade instructions
- [CHANGELOG_V3.md](CHANGELOG_V3.md) - Detailed changes
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues

## Release Notes

For detailed release notes, see [CHANGELOG_V3.md](CHANGELOG_V3.md).

#!/bin/bash

# Weather Formatter - Local Installation and Run Script
# This script installs dependencies and runs the weather formatter locally

set -e  # Exit on any error

echo "🌤️  Weather Formatter v2.1.0 - Local Setup"
echo "=========================================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✅ Found Python $PYTHON_VERSION"

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip3 is not installed or not in PATH"
    echo "Please install pip3"
    exit 1
fi

echo "📦 Installing dependencies..."

# Install dependencies
pip3 install -r requirements.txt

echo "🔧 Installing weather-formatter package in development mode..."

# Install the package in editable mode
pip3 install -e .

echo "✅ Installation complete!"
echo ""
echo "🚀 Usage Examples:"
echo ""
echo "1. Create default config (first time only):"
echo "   weather-formatter"
echo ""
echo "2. Run with ZIP code:"
echo "   weather-formatter -z 10001 -k YOUR_API_KEY"
echo ""
echo "3. Run with coordinates:"
echo "   weather-formatter --lat 40.7128 --lon -74.0060 -k YOUR_API_KEY"
echo ""
echo "4. Run with config file:"
echo "   weather-formatter --config weather_config.yaml"
echo ""
echo "5. Verbose mode for debugging:"
echo "   weather-formatter -v"
echo ""
echo "📝 Next Steps:"
echo "1. Get an API key from: https://openweathermap.org/api/one-call-3"
echo "2. Subscribe to One Call API 3.0 (free tier available)"
echo "3. Edit weather_config.yaml with your API key and location"
echo "4. Run: weather-formatter"
echo ""
echo "📚 Documentation:"
echo "- README.md - Full documentation"
echo "- MIGRATION_GUIDE.md - API v3 upgrade guide"
echo "- TROUBLESHOOTING.md - Common issues"
echo ""
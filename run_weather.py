#!/usr/bin/env python3
"""
Weather Formatter - Simple Runner Script
This script provides an easy way to run the weather formatter locally.
"""

import sys
import subprocess
import os
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import yaml
        import requests
        return True
    except ImportError:
        return False

def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def install_package():
    """Install the weather formatter package in development mode."""
    print("🔧 Installing weather-formatter package...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."])
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install package")
        return False

def run_weather_formatter(args=None):
    """Run the weather formatter with optional arguments."""
    try:
        from weather_formatter.cli import main
        if args:
            sys.argv = ["weather-formatter"] + args
        return main()
    except ImportError:
        print("❌ Weather formatter not properly installed")
        return 1
    except Exception as e:
        print(f"❌ Error running weather formatter: {e}")
        return 1

def main():
    """Main function."""
    print("🌤️  Weather Formatter v2.1.1 - Python Runner")
    print("============================================")
    
    # Check if dependencies are installed
    if not check_dependencies():
        print("📦 Dependencies not found, installing...")
        if not install_dependencies():
            sys.exit(1)
    
    # Install package if needed
    try:
        import weather_formatter
    except ImportError:
        if not install_package():
            sys.exit(1)
    
    print("✅ Setup complete!")
    print()
    
    # Check if config file exists
    config_file = Path("weather_config.yaml")
    if not config_file.exists():
        print("📝 No config file found, creating default config...")
        result = run_weather_formatter([])
        if result == 0:
            print()
            print("✅ Default config created!")
            print("📝 Please edit weather_config.yaml with your API key and location")
            print("🔗 Get API key: https://openweathermap.org/api/one-call-3")
            print("⚠️  Remember to subscribe to One Call API 3.0 (free tier available)")
        return result
    
    # Run with existing config
    print("🚀 Running weather formatter...")
    if len(sys.argv) > 1:
        # Pass through command line arguments
        return run_weather_formatter(sys.argv[1:])
    else:
        # Run with default config
        return run_weather_formatter([])

if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
"""
Check system requirements for Weather Formatter
"""

import sys
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} (compatible)")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} (requires 3.8+)")
        return False

def check_pip():
    """Check if pip is available."""
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      capture_output=True, check=True)
        print("✅ pip is available")
        return True
    except subprocess.CalledProcessError:
        print("❌ pip is not available")
        return False

def check_dependency(name, package=None):
    """Check if a Python package is installed."""
    if package is None:
        package = name
    
    spec = importlib.util.find_spec(package)
    if spec is not None:
        print(f"✅ {name} is installed")
        return True
    else:
        print(f"❌ {name} is not installed")
        return False

def main():
    """Main function."""
    print("🌤️  Weather Formatter v2.1.0 - Requirements Check")
    print("=========================================")
    print()
    
    all_good = True
    
    # Check Python version
    if not check_python_version():
        all_good = False
    
    # Check pip
    if not check_pip():
        all_good = False
    
    print()
    print("📦 Checking dependencies:")
    
    # Check required dependencies
    dependencies = [
        ("PyYAML", "yaml"),
        ("requests", "requests"),
        ("python-dateutil", "dateutil")
    ]
    
    missing_deps = []
    for name, package in dependencies:
        if not check_dependency(name, package):
            missing_deps.append(name)
            all_good = False
    
    print()
    
    if all_good:
        print("🎉 All requirements satisfied!")
        print("✅ Ready to install Weather Formatter")
        print()
        print("Next steps:")
        print("1. Run: ./install_and_run.sh")
        print("2. Or: python3 run_weather.py")
        print("3. Or: make setup")
    else:
        print("⚠️  Some requirements are missing")
        print()
        if missing_deps:
            print("To install missing dependencies:")
            print(f"pip3 install {' '.join(missing_deps)}")
            print()
            print("Or install all at once:")
            print("pip3 install -r requirements.txt")
        
        if sys.version_info < (3, 8):
            print()
            print("❌ Python version too old")
            print("Please install Python 3.8 or higher")
            print("Visit: https://www.python.org/downloads/")
    
    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())
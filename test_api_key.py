#!/usr/bin/env python3
"""Diagnostic script to test OpenWeatherMap API key."""

import sys
import requests


def test_api_key(api_key, zipcode="10001"):
    """Test if an API key works with OpenWeatherMap API.
    
    Args:
        api_key: The API key to test
        zipcode: ZIP code to test with (default: 10001 - New York)
    """
    print("=" * 60)
    print("OpenWeatherMap API Key Diagnostic Tool")
    print("=" * 60)
    print()
    
    # Show API key info (masked for security)
    if len(api_key) > 8:
        masked_key = api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:]
    else:
        masked_key = "*" * len(api_key)
    
    print(f"Testing API key: {masked_key}")
    print(f"API key length: {len(api_key)} characters")
    print(f"Testing with zipcode: {zipcode}")
    print()
    
    # Check for common issues
    issues = []
    
    if api_key.startswith('"') or api_key.startswith("'"):
        issues.append("⚠️  API key starts with a quote character")
    
    if api_key.endswith('"') or api_key.endswith("'"):
        issues.append("⚠️  API key ends with a quote character")
    
    if ' ' in api_key:
        issues.append("⚠️  API key contains spaces")
    
    if '\n' in api_key or '\r' in api_key:
        issues.append("⚠️  API key contains newline characters")
    
    if len(api_key) != 32:
        issues.append(f"⚠️  API key length is {len(api_key)}, expected 32 characters")
    
    if issues:
        print("Potential issues detected:")
        for issue in issues:
            print(f"  {issue}")
        print()
    
    # Test the API
    print("Making test API request...")
    print()
    
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "zip": f"{zipcode},US",
        "appid": api_key,
        "units": "imperial"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        print(f"Response status code: {response.status_code}")
        print()
        
        if response.status_code == 200:
            print("✅ SUCCESS! Your API key is working correctly.")
            data = response.json()
            print()
            print("Sample data retrieved:")
            print(f"  Location: {data.get('name', 'Unknown')}")
            print(f"  Temperature: {data.get('main', {}).get('temp', 'N/A')}°F")
            print(f"  Condition: {data.get('weather', [{}])[0].get('description', 'N/A')}")
            return True
            
        elif response.status_code == 401:
            print("❌ FAILED: Invalid API key")
            print()
            print("Possible reasons:")
            print("  1. The API key is incorrect")
            print("  2. The API key hasn't been activated yet (can take 1-2 hours)")
            print("  3. The API key has been revoked or expired")
            print()
            print("Response from API:")
            print(f"  {response.text}")
            return False
            
        elif response.status_code == 404:
            print("❌ FAILED: Invalid zipcode")
            print(f"  The zipcode '{zipcode}' was not found")
            return False
            
        elif response.status_code == 429:
            print("❌ FAILED: Rate limit exceeded")
            print("  You've made too many requests. Wait a moment and try again.")
            return False
            
        else:
            print(f"❌ FAILED: Unexpected error (status {response.status_code})")
            print(f"  Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ FAILED: Request timed out")
        print("  Check your internet connection")
        return False
        
    except requests.exceptions.ConnectionError:
        print("❌ FAILED: Connection error")
        print("  Check your internet connection")
        return False
        
    except Exception as e:
        print(f"❌ FAILED: Unexpected error: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_api_key.py <your_api_key> [zipcode]")
        print()
        print("Example:")
        print("  python test_api_key.py abc123def456 10001")
        print()
        print("Or test with your config file:")
        print("  python test_api_key.py $(grep 'api_key:' weather_config.yaml | cut -d':' -f2 | tr -d ' \"')")
        sys.exit(1)
    
    api_key = sys.argv[1].strip().strip('"').strip("'")
    zipcode = sys.argv[2] if len(sys.argv) > 2 else "10001"
    
    success = test_api_key(api_key, zipcode)
    sys.exit(0 if success else 1)

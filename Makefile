# Weather Formatter - Makefile
# Simple commands for development and running

.PHONY: help install run test clean setup

help:
	@echo "🌤️  Weather Formatter v2.1.0 - Available Commands"
	@echo "================================================="
	@echo ""
	@echo "Setup Commands:"
	@echo "  make install    - Install dependencies and package"
	@echo "  make setup      - Full setup (install + create config)"
	@echo ""
	@echo "Run Commands:"
	@echo "  make run        - Run with existing config"
	@echo "  make run-demo   - Run with demo location (NYC)"
	@echo ""
	@echo "Development Commands:"
	@echo "  make test       - Run tests (if pytest available)"
	@echo "  make clean      - Clean build artifacts"
	@echo "  make check      - Check code syntax"
	@echo ""
	@echo "Help:"
	@echo "  make help       - Show this help message"

install:
	@echo "📦 Installing dependencies..."
	pip3 install -r requirements.txt
	@echo "🔧 Installing package in development mode..."
	pip3 install -e .
	@echo "✅ Installation complete!"

setup: install
	@echo "📝 Creating default config..."
	@python3 -c "from weather_formatter.cli import main; main()" || true
	@echo ""
	@echo "✅ Setup complete!"
	@echo "📝 Please edit weather_config.yaml with your API key"
	@echo "🔗 Get API key: https://openweathermap.org/api/one-call-3"

run:
	@echo "🚀 Running weather formatter..."
	weather-formatter

run-demo:
	@echo "🚀 Running weather formatter with NYC coordinates..."
	weather-formatter --lat 40.7128 --lon -74.0060 -k YOUR_API_KEY

test:
	@echo "🧪 Running tests..."
	@if command -v pytest >/dev/null 2>&1; then \
		pytest tests/ -v; \
	else \
		echo "⚠️  pytest not installed, running basic syntax check..."; \
		python3 -m py_compile weather_formatter/*.py tests/*.py; \
		echo "✅ Syntax check passed!"; \
	fi

check:
	@echo "🔍 Checking code syntax..."
	python3 -m py_compile weather_formatter/*.py tests/*.py setup.py
	@echo "✅ All files compile successfully!"

clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf __pycache__/
	rm -rf weather_formatter/__pycache__/
	rm -rf tests/__pycache__/
	find . -name "*.pyc" -delete
	@echo "✅ Clean complete!"

# Quick commands
.PHONY: quick-install quick-run
quick-install: install
quick-run: run
# YT Leechr Makefile

.PHONY: install test test-unit test-integration test-gui clean lint format run build release help

# Default target
help:
	@echo "YT Leechr Development Commands:"
	@echo ""
	@echo "  install     Install dependencies"
	@echo "  test        Run all tests"
	@echo "  test-unit   Run unit tests only"
	@echo "  test-gui    Run GUI tests only"
	@echo "  clean       Clean up generated files"
	@echo "  lint        Run code linting"
	@echo "  format      Format code"
	@echo "  run         Run the application"
	@echo "  build       Build standalone executable"
	@echo "  release     Create a new release (usage: make release BUMP=patch)"
	@echo "  help        Show this help message"

# Install dependencies
install:
	pip install -r requirements.txt

# Run all tests
test:
	python run_tests.py

# Run unit tests only
test-unit:
	python run_tests.py -m unit

# Run GUI tests only  
test-gui:
	python run_tests.py -m gui

# Run integration tests only
test-integration:
	python run_tests.py -m integration

# Clean up generated files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/

# Run code linting (if flake8 is available)
lint:
	@if command -v flake8 >/dev/null 2>&1; then \
		flake8 src/ tests/ --max-line-length=100 --ignore=E501,W503; \
	else \
		echo "flake8 not found. Install with: pip install flake8"; \
	fi

# Format code (if black is available)
format:
	@if command -v black >/dev/null 2>&1; then \
		black src/ tests/ --line-length=100; \
	else \
		echo "black not found. Install with: pip install black"; \
	fi

# Run the application
run:
	python main.py

# Development setup
dev-install: install
	pip install pytest-cov black flake8 mypy

# Create distribution
dist:
	python setup.py sdist bdist_wheel

# Install in development mode
dev:
	pip install -e .

# Build standalone executable
build:
	python build.py

# Create a new release
release:
	@if [ -z "$(BUMP)" ]; then \
		echo "Error: BUMP parameter required. Usage: make release BUMP=patch|minor|major"; \
		exit 1; \
	fi
	python scripts/release.py $(BUMP)
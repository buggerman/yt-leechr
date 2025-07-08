---
layout: default
title: Development
description: Development guide for contributing to YT Leechr
---

# Development Guide

Learn how to set up a development environment, contribute code, and build YT Leechr from source.

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- FFmpeg (for testing download functionality)

### Clone Repository

```bash
git clone https://github.com/buggerman/yt-leechr.git
cd yt-leechr
```

### Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Install Dependencies

```bash
# Install runtime dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

## Development Workflow

### Branch Strategy

- **main**: Stable release branch
- **dev**: Development branch for new features
- **feature/**: Feature branches

**Important**: Always work in dev branch and test thoroughly before merging to main.

### Making Changes

1. **Create feature branch** from dev:
```bash
git checkout dev
git checkout -b feature/your-feature-name
```

2. **Make your changes** with proper testing

3. **Run tests** to ensure nothing breaks:
```bash
make test
```

4. **Commit changes** with descriptive messages:
```bash
git add .
git commit -m "Add feature: description of changes"
```

5. **Push and create pull request** to dev branch

## Project Structure

```
yt-leechr/
├── src/                    # Application source code
│   ├── __init__.py        # Package initialization and version
│   ├── main_window.py     # Main application window
│   ├── download_manager.py # Download logic and threading
│   ├── download_item.py   # Download item model
│   ├── settings_widget.py # Settings UI and configuration
│   └── theme_manager.py   # Theme and styling management
├── tests/                  # Test suite
│   ├── test_*.py          # Test modules
│   └── conftest.py        # Test configuration and fixtures
├── assets/                 # Application assets
│   └── icon.*             # Application icons
├── docs/                   # Documentation
├── build.py               # Build script for executables
├── main.py                # Application entry point
├── requirements.txt       # Runtime dependencies
├── requirements-dev.txt   # Development dependencies
└── Makefile              # Development commands
```

## Architecture

### Application Design

YT Leechr follows a Model-View-Controller (MVC) pattern with Qt signals/slots:

**Models:**
- `DownloadItem`: Represents individual downloads
- Settings configuration classes

**Views:**
- `MainWindow`: Primary application interface
- `SettingsWidget`: Configuration panel
- Custom Qt widgets for UI components

**Controllers:**
- `DownloadManager`: Manages download queue and workers
- `ThemeManager`: Handles UI theming
- Event handlers and signal connections

### Threading Architecture

```python
# Main thread: UI and user interaction
MainWindow (QMainWindow)
├── Download queue management
├── Settings panel
└── Progress updates

# Worker threads: Download processing
DownloadManager (QObject)
├── DownloadWorker (QThread)
│   ├── yt-dlp integration
│   ├── Progress reporting
│   └── Error handling
└── Queue management
```

## Development Commands

### Using Makefile

```bash
# Show available commands
make help

# Install dependencies
make install

# Run application
make run

# Run tests
make test
make test-unit          # Unit tests only
make test-gui           # GUI tests only
make test-integration   # Integration tests only

# Code quality
make lint               # Run linting
make format             # Format code with black
make typecheck          # Run mypy type checking

# Build
make build              # Build executable
make clean              # Clean build artifacts
```

### Manual Commands

```bash
# Run application
python main.py

# Run tests with coverage
python -m pytest --cov=src --cov-report=html

# Build executable
python build.py

# Install as editable package
pip install -e .
```

## Testing

### Test Structure

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **GUI Tests**: Test user interface with pytest-qt

### Running Tests

```bash
# All tests
python -m pytest tests/ -v

# Specific test categories
python -m pytest tests/ -m "unit"
python -m pytest tests/ -m "gui" 
python -m pytest tests/ -m "integration"

# With coverage
python -m pytest tests/ --cov=src --cov-report=html

# Single test file
python -m pytest tests/test_download_manager.py -v
```

### Writing Tests

**Unit Test Example:**
```python
import pytest
from src.download_item import DownloadItem

@pytest.mark.unit
def test_download_item_creation():
    item = DownloadItem("https://example.com/video", "test_video")
    assert item.url == "https://example.com/video"
    assert item.title == "test_video"
    assert item.status == "pending"
```

**GUI Test Example:**
```python
import pytest
from PyQt6.QtCore import Qt
from src.main_window import MainWindow

@pytest.mark.gui
def test_add_download(qtbot, main_window):
    qtbot.addWidget(main_window)
    
    # Simulate adding a download
    main_window.url_input.setText("https://example.com/video")
    qtbot.keyClick(main_window.url_input, Qt.Key.Key_Return)
    
    # Verify download was added
    assert main_window.download_table.rowCount() == 1
```

### Test Coverage

Current test coverage: **68 tests** covering all major components

- `test_download_item.py`: 10 tests
- `test_download_manager.py`: 24 tests  
- `test_main_window.py`: 14 tests
- `test_settings_widget.py`: 16 tests
- `test_theme_manager.py`: 12 tests

## Building

### Create Executable

```bash
# Build for current platform
python build.py

# Manual build with PyInstaller
pyinstaller YT-Leechr.spec
```

**Build Outputs:**
- **Windows**: `YT-Leechr-windows-x64.exe`
- **macOS**: `YT Leechr.app` bundle
- **Linux**: `YT-Leechr-linux-x64`

### Cross-Platform Considerations

**Windows:**
- Use `.exe` extension
- Include icon in executable
- Handle Windows-specific paths

**macOS:**
- Create `.app` bundle
- Code signing (for distribution)
- Handle macOS security restrictions

**Linux:**
- Create portable executable
- Handle different distributions
- Flatpak packaging support

## Contributing

### Code Style

- **Python**: Follow PEP 8
- **Formatting**: Use Black formatter
- **Imports**: Use isort for import organization
- **Type Hints**: Add type hints for new code
- **Docstrings**: Document all public functions

### Code Quality Tools

```bash
# Format code
black src/ tests/

# Sort imports  
isort src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

### Pull Request Process

1. **Fork** the repository on GitHub
2. **Create feature branch** from dev
3. **Make changes** with tests
4. **Ensure all tests pass**
5. **Submit pull request** to dev branch
6. **Address review feedback**

### Commit Guidelines

**Format:**
```
<type>(<scope>): <description>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `build`: Build system changes

**Examples:**
```bash
feat(download): add playlist support for Vimeo

Add support for downloading Vimeo playlists with individual
video selection and batch processing capabilities.

Closes #123
```

## Release Process

### Version Management

Versions follow semantic versioning (SemVer):
- **Major** (1.0.0): Breaking changes
- **Minor** (0.1.0): New features, backwards compatible
- **Patch** (0.0.1): Bug fixes, backwards compatible

### Creating Releases

1. **Update version** in relevant files:
   - `src/__init__.py`
   - `setup.py`
   - `build.py`
   - `io.github.buggerman.yt-leechr.metainfo.xml`

2. **Update changelog** with new features and fixes

3. **Test thoroughly** in dev branch

4. **Merge dev to main** after all tests pass

5. **Create release tag**:
```bash
git tag v0.6.0
git push origin v0.6.0
```

6. **GitHub Actions** will automatically build and deploy

## Debugging

### Common Development Issues

**Import Errors:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements-dev.txt
```

**PyQt6 Issues:**
```bash
# Install specific version
pip install PyQt6==6.7.0

# Check Qt installation
python -c "from PyQt6.QtWidgets import QApplication; print('PyQt6 working')"
```

**Test Failures:**
```bash
# Run with verbose output
python -m pytest tests/ -v -s

# Run specific failing test
python -m pytest tests/test_specific.py::test_function -v
```

### Development Tools

**Recommended IDE Setup:**
- **VS Code** with Python extension
- **PyCharm** Community or Professional
- **Qt Designer** for UI design

**Useful Extensions:**
- Python
- PyQt6 support
- Black formatter
- GitLens
- Test Explorer

---

[← Configuration](configuration) | [Next: Testing →](testing)
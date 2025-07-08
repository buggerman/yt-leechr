---
layout: default
title: Testing
description: Testing guide and test suite information for YT Leechr
---

# Testing Guide

YT Leechr includes a comprehensive test suite with 68 tests covering all major components, ensuring reliability and code quality.

## Test Overview

### Test Statistics

- **Total Tests**: 68
- **Test Coverage**: All major components
- **Test Types**: Unit, Integration, GUI
- **Framework**: pytest with pytest-qt

### Test Distribution

| Module | Tests | Description |
|--------|-------|-------------|
| `test_download_item.py` | 10 | Download model testing |
| `test_download_manager.py` | 24 | Download worker and manager |
| `test_main_window.py` | 14 | GUI functionality |
| `test_settings_widget.py` | 16 | Settings and configuration |
| `test_theme_manager.py` | 12 | Theme management |

## Running Tests

### Quick Test Commands

```bash
# Run all tests
make test

# Run with verbose output
python -m pytest tests/ -v

# Run specific test categories
make test-unit          # Unit tests only
make test-gui           # GUI tests only  
make test-integration   # Integration tests only
```

### Detailed Test Commands

```bash
# Run all tests with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run specific test file
python -m pytest tests/test_download_manager.py -v

# Run specific test function
python -m pytest tests/test_main_window.py::TestMainWindow::test_add_download -v

# Run tests matching pattern
python -m pytest tests/ -k "download" -v

# Run tests with markers
python -m pytest tests/ -m "unit" -v
python -m pytest tests/ -m "gui" -v
python -m pytest tests/ -m "slow" -v
```

### Test Configuration

Tests are configured in `pytest.ini`:

```ini
[tool:pytest]
testpaths = tests
addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings
qt_api = pyqt6
markers =
    unit: Unit tests
    integration: Integration tests  
    gui: GUI tests
    slow: Slow tests (may take >1s)
```

## Test Categories

### Unit Tests

**Purpose**: Test individual components in isolation

**Characteristics:**
- Fast execution (< 100ms each)
- No external dependencies
- Mock external services
- Test single functions/methods

**Example:**
```python
@pytest.mark.unit
def test_download_item_creation():
    """Test creating a download item with basic properties."""
    item = DownloadItem("https://example.com", "Test Video")
    
    assert item.url == "https://example.com"
    assert item.title == "Test Video"
    assert item.status == "pending"
    assert item.progress == 0
```

### Integration Tests

**Purpose**: Test component interactions and workflows

**Characteristics:**
- Test multiple components together
- Verify data flow between modules
- Test realistic scenarios
- May use mocked external services

**Example:**
```python
@pytest.mark.integration
def test_download_manager_queue_processing():
    """Test download manager processes queue correctly."""
    manager = DownloadManager()
    
    # Add multiple downloads
    manager.add_download("https://example1.com", {"quality": "720p"})
    manager.add_download("https://example2.com", {"quality": "480p"})
    
    # Verify queue processing
    assert manager.queue_size() == 2
    assert manager.active_downloads() == 0
```

### GUI Tests

**Purpose**: Test user interface components and interactions

**Characteristics:**
- Use pytest-qt for Qt testing
- Simulate user interactions
- Test UI state changes
- Verify signal/slot connections

**Example:**
```python
@pytest.mark.gui
def test_paste_from_clipboard(qtbot, main_window):
    """Test pasting URL from clipboard."""
    qtbot.addWidget(main_window)
    
    # Set clipboard content
    clipboard = QApplication.clipboard()
    clipboard.setText("https://example.com/video")
    
    # Simulate paste action
    main_window.paste_from_clipboard()
    
    # Verify URL was pasted
    assert main_window.url_input.text() == "https://example.com/video"
```

## Test Environment

### Setup and Fixtures

Tests use `conftest.py` for shared fixtures:

```python
@pytest.fixture
def qapp():
    """Create QApplication instance for GUI tests."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    app.quit()

@pytest.fixture
def main_window(qapp):
    """Create MainWindow instance for testing."""
    window = MainWindow()
    yield window
    window.close()

@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    with patch('src.settings_widget.QSettings') as mock:
        yield mock
```

### Mocking Strategy

Tests extensively use mocking to isolate components:

**yt-dlp Integration:**
```python
@patch('src.download_manager.yt_dlp.YoutubeDL')
def test_download_worker_success(mock_ytdl):
    """Test successful download with mocked yt-dlp."""
    mock_instance = mock_ytdl.return_value
    mock_instance.download.return_value = None
    
    worker = DownloadWorker("https://example.com", {})
    worker.run()
    
    mock_ytdl.assert_called_once()
```

**Qt Components:**
```python
@patch('PyQt6.QtWidgets.QFileDialog.getExistingDirectory')
def test_browse_output_dir(mock_dialog, settings_widget):
    """Test directory selection dialog."""
    mock_dialog.return_value = "/selected/directory"
    
    settings_widget.browse_output_dir()
    
    assert settings_widget.output_dir_edit.text() == "/selected/directory"
```

## Test Data and Scenarios

### Test URLs

Tests use controlled URLs that don't require network access:

```python
TEST_URLS = {
    'youtube': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    'vimeo': 'https://vimeo.com/123456789',
    'invalid': 'https://invalid-url-for-testing.com',
    'playlist': 'https://www.youtube.com/playlist?list=PLtest'
}
```

### Mock Responses

Tests simulate various download scenarios:

```python
MOCK_DOWNLOAD_INFO = {
    'title': 'Test Video',
    'uploader': 'Test Channel',
    'duration': 180,
    'view_count': 1000,
    'upload_date': '20230101',
    'formats': [
        {'format_id': '720p', 'height': 720},
        {'format_id': '480p', 'height': 480}
    ]
}
```

## Continuous Integration

### GitHub Actions

Tests run automatically on:
- **Push to main/dev branches**
- **Pull requests**
- **Release tags**

**Test Matrix:**
- Python 3.8, 3.9, 3.10, 3.11, 3.12
- Ubuntu, Windows, macOS
- Different PyQt6 versions

### Test Workflow

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: [3.8, 3.9, 3.10, 3.11, 3.12]
    
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          pip install -r requirements-dev.txt
      - name: Run tests
        run: |
          python -m pytest tests/ -v
```

## Test Development

### Writing New Tests

**Test Structure:**
```python
import pytest
from unittest.mock import Mock, patch
from src.module_name import ClassToTest

@pytest.mark.unit  # or integration, gui
class TestClassName:
    """Test class with descriptive docstring."""
    
    def test_specific_functionality(self):
        """Test specific functionality with clear description."""
        # Arrange
        test_data = "test input"
        
        # Act
        result = function_to_test(test_data)
        
        # Assert
        assert result == expected_output
```

**Best Practices:**
1. **Clear test names** describing what is being tested
2. **Arrange-Act-Assert** pattern for test structure
3. **Mock external dependencies** to isolate components
4. **Test edge cases** and error conditions
5. **Use appropriate markers** for test categorization

### Test Debugging

**Running Single Tests:**
```bash
# Run specific test with detailed output
python -m pytest tests/test_main_window.py::TestMainWindow::test_add_download -v -s

# Run with debugger
python -m pytest tests/test_main_window.py::TestMainWindow::test_add_download --pdb
```

**GUI Test Debugging:**
```python
@pytest.mark.gui
def test_ui_interaction(qtbot, main_window):
    """Test UI interaction with debugging."""
    qtbot.addWidget(main_window)
    
    # Add delays for manual inspection
    qtbot.wait(1000)  # Wait 1 second
    
    # Take screenshot for debugging
    main_window.grab().save("debug_screenshot.png")
    
    # Your test assertions here
```

## Coverage Reports

### Generating Coverage

```bash
# Generate HTML coverage report
python -m pytest tests/ --cov=src --cov-report=html

# Open coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Coverage Goals

- **Target**: 90%+ code coverage
- **Critical paths**: 100% coverage for core functionality
- **UI components**: Focus on user interaction paths
- **Error handling**: Test all error conditions

## Performance Testing

### Slow Test Identification

```bash
# Run tests with duration reporting
python -m pytest tests/ --durations=10

# Run only fast tests (exclude slow marker)
python -m pytest tests/ -m "not slow"
```

### Memory and Resource Testing

```python
@pytest.mark.slow
def test_memory_usage_large_queue():
    """Test memory usage with large download queue."""
    manager = DownloadManager()
    
    # Add many downloads
    for i in range(1000):
        manager.add_download(f"https://example.com/video{i}", {})
    
    # Monitor memory usage
    import psutil
    process = psutil.Process()
    memory_mb = process.memory_info().rss / 1024 / 1024
    
    assert memory_mb < 100  # Less than 100MB
```

## Troubleshooting Tests

### Common Issues

**PyQt6 Display Issues:**
```bash
# Set display for headless environments
export QT_QPA_PLATFORM=offscreen
python -m pytest tests/ -m gui
```

**Import Errors:**
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Install in development mode
pip install -e .
```

**Slow GUI Tests:**
```bash
# Reduce test timeouts
python -m pytest tests/ -m gui --tb=short --maxfail=1
```

### Test Environment Issues

**Virtual Environment:**
```bash
# Ensure correct environment
which python
pip list | grep PyQt6

# Recreate if needed
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
```

---

[← Development](development) | [Next: Troubleshooting →](troubleshooting)
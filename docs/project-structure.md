# YT Leechr Project Structure

**Repository**: https://github.com/buggerman/yt-leechr

```
yt-leechr/
├── .github/                    # GitHub configuration
│   ├── workflows/              # CI/CD workflows
│   │   ├── test.yml           # Test automation
│   │   └── build.yml          # Build automation
│   ├── ISSUE_TEMPLATE/        # Issue templates
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── pull_request_template.md
├── assets/                     # Application assets
│   ├── icon.ico               # Windows icon (to be added)
│   ├── icon.icns              # macOS icon (to be added)
│   ├── icon.png               # General icon (to be added)
│   └── README.md              # Asset creation guide
├── docs/                      # Documentation
│   └── project-structure.md   # This file
├── scripts/                   # Build and utility scripts
│   ├── __init__.py
│   └── release.py             # Release automation
├── src/                       # Source code
│   ├── __init__.py            # Package metadata
│   ├── download_item.py       # Download item model
│   ├── download_manager.py    # Download management
│   ├── main_window.py         # Main application window
│   ├── settings_widget.py     # Settings panel
│   └── theme_manager.py       # Theme management
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── test_download_item.py  # Download item tests
│   ├── test_download_manager.py # Download manager tests
│   ├── test_main_window.py    # Main window tests
│   ├── test_settings_widget.py # Settings widget tests
│   └── test_theme_manager.py  # Theme manager tests
├── .gitignore                 # Git ignore rules
├── build.py                   # Build script
├── CHANGELOG.md               # Change log
├── conftest.py                # Pytest configuration
├── CONTRIBUTING.md            # Contribution guidelines
├── LICENSE                    # MIT license
├── main.py                    # Application entry point
├── Makefile                   # Development commands
├── pytest.ini                # Pytest configuration
├── README.md                  # Project documentation
├── requirements.txt           # Runtime dependencies
├── requirements-dev.txt       # Development dependencies
├── run_tests.py              # Test runner
├── setup.py                  # Package setup
└── YT-Leechr.spec            # PyInstaller specification
```

## Key Components

### Source Code (`src/`)
- **main_window.py**: Main application window with UI components
- **download_manager.py**: Handles download queue and yt-dlp integration
- **download_item.py**: Data model for individual downloads
- **settings_widget.py**: Configuration panel for user preferences
- **theme_manager.py**: Dark/light theme management

### Tests (`tests/`)
- Comprehensive test suite with 68 tests
- Unit tests for core functionality
- GUI tests for user interface
- Integration tests for component interaction
- All tests use pytest with mocking for external dependencies

### Build System
- **build.py**: Cross-platform executable builder
- **YT-Leechr.spec**: PyInstaller configuration
- **Makefile**: Development command shortcuts
- **scripts/release.py**: Automated release process

### CI/CD (`.github/`)
- **test.yml**: Automated testing on multiple platforms
- **build.yml**: Automated builds and releases
- Issue and PR templates for GitHub

### Documentation
- **README.md**: User documentation and setup guide
- **CONTRIBUTING.md**: Developer contribution guidelines
- **CHANGELOG.md**: Version history and changes
- **docs/**: Additional documentation files

## Development Workflow

1. **Setup**: `make install` or `pip install -r requirements-dev.txt`
2. **Development**: Edit source files in `src/`
3. **Testing**: `make test` to run test suite
4. **Building**: `make build` to create executables
5. **Release**: `make release BUMP=patch` for new versions

## Build Outputs

When building, outputs are created in `dist/`:
- Platform-specific executables
- Portable packages (ZIP/tar.gz)
- macOS app bundles (.app)

## Configuration Files

- **pytest.ini**: Test framework configuration
- **conftest.py**: Shared test fixtures
- **requirements.txt**: Runtime dependencies only
- **requirements-dev.txt**: All development dependencies
- **.gitignore**: Files to exclude from version control
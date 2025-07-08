# Credits and Acknowledgments

YT Leechr is built on the shoulders of giants. This document provides detailed attribution to all the open source projects, libraries, and communities that make this application possible.

## Core Application Framework

### yt-dlp
- **Project**: https://github.com/yt-dlp/yt-dlp
- **License**: Public Domain (Unlicense)
- **Role**: The core video downloading engine that powers YT Leechr
- **Description**: A feature-rich command-line audio/video downloader
- **Impact**: Without yt-dlp, this GUI application would not exist. It provides support for 1000+ websites, format selection, quality options, subtitle downloading, and all core functionality.

### PyQt6
- **Project**: https://pypi.org/project/PyQt6/
- **License**: GPL v3 / Commercial License
- **Developer**: Riverbank Computing Limited
- **Role**: GUI framework providing the entire user interface
- **Description**: Python bindings for Qt6 cross-platform application framework
- **Impact**: Enables native desktop application with professional appearance across Windows, macOS, and Linux

### Qt6 Framework
- **Project**: https://www.qt.io/
- **License**: GPL v3 / Commercial License  
- **Developer**: The Qt Company
- **Role**: Underlying GUI framework for PyQt6
- **Description**: Cross-platform software development framework
- **Impact**: Foundation for window management, widgets, theming, and OS integration

## Media Processing

### FFmpeg
- **Project**: https://ffmpeg.org/
- **License**: GNU Lesser General Public License (LGPL) v2.1+
- **Role**: Video/audio processing, format conversion, and stream merging
- **Description**: Complete, cross-platform solution to record, convert and stream audio and video
- **Impact**: Essential for merging separate video/audio streams, format conversion, and multimedia processing
- **Note**: Bundled binaries are GPL v3 licensed builds from https://github.com/BtbN/FFmpeg-Builds

## Python Ecosystem

### Python Standard Library
- **Project**: https://python.org/
- **License**: Python Software Foundation License
- **Role**: Core runtime and standard modules
- **Modules Used**: os, sys, threading, queue, subprocess, json, pathlib, typing, re, tempfile, shutil

### Python Package Index (PyPI) Dependencies

#### requests
- **Project**: https://github.com/psf/requests
- **License**: Apache 2.0
- **Role**: HTTP requests for downloads and API calls
- **Description**: Elegant and simple HTTP library for Python

#### urllib3
- **Project**: https://github.com/urllib3/urllib3  
- **License**: MIT
- **Role**: HTTP client library (dependency of requests)

#### certifi
- **Project**: https://github.com/certifi/python-certifi
- **License**: Mozilla Public License 2.0
- **Role**: SSL certificate bundle for secure connections

#### charset-normalizer
- **Project**: https://github.com/Ousret/charset_normalizer
- **License**: MIT
- **Role**: Character encoding detection (dependency of requests)

#### idna
- **Project**: https://github.com/kjd/idna
- **License**: BSD 3-Clause
- **Role**: Internationalized Domain Names support

## Development and Testing Tools

### pytest
- **Project**: https://github.com/pytest-dev/pytest
- **License**: MIT
- **Role**: Testing framework for comprehensive test suite
- **Description**: Makes it easy to write small tests, yet scales to support complex functional testing

### pytest-qt
- **Project**: https://github.com/pytest-dev/pytest-qt
- **License**: MIT
- **Role**: PyQt/Qt testing support for GUI tests
- **Description**: Provides fixtures and helpers for testing PyQt applications

### pytest-mock
- **Project**: https://github.com/pytest-dev/pytest-mock
- **License**: MIT
- **Role**: Mocking support for unit tests
- **Description**: Thin wrapper around unittest.mock for pytest

### pytest-asyncio
- **Project**: https://github.com/pytest-dev/pytest-asyncio
- **License**: Apache 2.0
- **Role**: Testing async code support
- **Description**: Pytest support for asyncio

## Build and Distribution Tools

### PyInstaller
- **Project**: https://github.com/pyinstaller/pyinstaller
- **License**: GPL v2 with runtime exception
- **Role**: Creates standalone executables from Python applications
- **Description**: Bundles Python applications into standalone executables
- **Impact**: Enables distribution of YT Leechr without requiring Python installation

### setuptools
- **Project**: https://github.com/pypa/setuptools
- **License**: MIT
- **Role**: Python packaging and distribution
- **Description**: Library for packaging Python projects

### pip
- **Project**: https://github.com/pypa/pip
- **License**: MIT
- **Role**: Python package installer
- **Description**: Package management system for Python

## Linux Distribution Infrastructure

### Flatpak
- **Project**: https://github.com/flatpak/flatpak
- **License**: LGPL v2.1+
- **Role**: Application sandboxing and distribution for Linux
- **Description**: Framework for distributing desktop applications on Linux
- **Impact**: Enables secure, universal Linux distribution with minimal permissions

### Flathub
- **Project**: https://flathub.org/
- **License**: Various (community-driven)
- **Role**: Central repository for Flatpak applications
- **Description**: App store and distribution platform for Linux applications
- **Impact**: Provides pathway for users to discover and install YT Leechr

### KDE Platform Runtime
- **Project**: https://kde.org/
- **License**: Various open source licenses
- **Role**: Qt6 runtime environment for Flatpak
- **Description**: Provides Qt6 libraries and KDE integration for Flatpak apps
- **Impact**: Enables professional desktop integration and reduces app bundle size

### org.freedesktop.Platform.ffmpeg-full
- **Project**: https://github.com/flathub/org.freedesktop.Platform.ffmpeg-full
- **License**: GPL v3
- **Role**: FFmpeg extension for Flatpak applications
- **Description**: Provides FFmpeg libraries in sandboxed environment

## Continuous Integration

### GitHub Actions
- **Service**: https://github.com/features/actions
- **License**: GitHub Terms of Service
- **Role**: Automated CI/CD pipeline
- **Description**: Workflow automation for testing, building, and releasing
- **Impact**: Enables automated multi-platform testing and building for Windows, macOS, and Linux

### Actions Used

#### actions/checkout
- **Project**: https://github.com/actions/checkout
- **License**: MIT
- **Role**: Repository checkout for CI workflows

#### actions/setup-python
- **Project**: https://github.com/actions/setup-python
- **License**: MIT
- **Role**: Python environment setup for CI

#### actions/upload-artifact
- **Project**: https://github.com/actions/upload-artifact
- **License**: MIT
- **Role**: Build artifact storage and sharing

#### actions/download-artifact
- **Project**: https://github.com/actions/download-artifact
- **License**: MIT
- **Role**: Artifact retrieval for release creation

#### softprops/action-gh-release
- **Project**: https://github.com/softprops/action-gh-release
- **License**: MIT
- **Role**: Automated GitHub release creation

## External Services and Resources

### BtbN FFmpeg Builds
- **Project**: https://github.com/BtbN/FFmpeg-Builds
- **License**: GPL v3
- **Role**: Pre-compiled FFmpeg binaries for Windows and Linux
- **Description**: Automated FFmpeg builds with consistent configuration
- **Impact**: Provides reliable FFmpeg binaries for bundling with releases

### Python Package Index (PyPI)
- **Service**: https://pypi.org/
- **Role**: Python package distribution
- **Impact**: Hosts all Python dependencies used by YT Leechr

## Documentation and Communication

### Markdown
- **Standard**: CommonMark specification
- **Role**: Documentation format for README, CHANGELOG, and project docs
- **Description**: Lightweight markup language for readable documentation

### GitHub
- **Service**: https://github.com/
- **Role**: Code hosting, issue tracking, and project management
- **Impact**: Provides collaboration platform and version control

## Special Recognition

### Open Source Community
The broader open source community deserves recognition for:
- Creating and maintaining these essential tools
- Providing documentation, examples, and support
- Contributing bug reports, feature requests, and improvements
- Building a collaborative ecosystem that makes projects like YT Leechr possible

### Individual Contributors
While YT Leechr itself may have specific contributors, it builds upon the work of thousands of developers who have contributed to the underlying projects, libraries, and tools.

## License Compliance Statement

YT Leechr is committed to full compliance with all upstream project licenses:

1. **MIT License (YT Leechr)**: Chosen for maximum compatibility and permissive use
2. **GPL v3 Compliance**: FFmpeg binaries and PyQt6 usage fully comply with GPL v3 terms
3. **LGPL Compliance**: FFmpeg libraries used in accordance with LGPL requirements
4. **Attribution Requirements**: All projects properly attributed in documentation and code
5. **License Preservation**: Original license files maintained for bundled components

## Contributing to Upstream Projects

Users of YT Leechr are encouraged to contribute back to the projects that make it possible:
- Report bugs and feature requests to upstream projects
- Contribute code improvements and documentation
- Support maintainers through donations or sponsorship
- Share knowledge and help other users in community forums

## Updates and Maintenance

This credits file is maintained alongside YT Leechr development:
- New dependencies are promptly added with proper attribution
- License changes in upstream projects are tracked and updated
- Community contributions to YT Leechr itself are recognized

---

**Last Updated**: July 2025
**YT Leechr Version**: 0.6.0+

For the most current information, see individual project websites and repositories linked above.
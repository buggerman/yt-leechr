# Changelog

All notable changes to YT Leechr will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of YT Leechr
- Modern PyQt6-based GUI for yt-dlp
- GitHub repository: https://github.com/buggerman/yt-leechr
- Download queue management with progress tracking
- Format selection and quality options
- Subtitle download support with multiple languages
- Dark mode and light mode themes
- Batch download support for multiple URLs
- Context menus for download management
- Settings persistence across sessions
- Cross-platform support (Windows, macOS, Linux)
- Comprehensive test suite with 68 tests
- Standalone executable builds with PyInstaller
- Documentation and contribution guidelines

### Features
- **Queue Management**: Add, pause, resume, retry, and remove downloads
- **Format Selection**: Choose video quality, audio-only extraction, custom formats
- **Subtitle Support**: Download and embed subtitles in multiple languages
- **Batch Downloads**: Process multiple URLs simultaneously
- **Theme Support**: Dark, light, and system theme modes
- **Settings Panel**: Comprehensive configuration options
- **Progress Tracking**: Real-time download progress and speed
- **Error Handling**: Clear error messages and retry functionality
- **Cross-Platform**: Native look and feel on all platforms

### Technical Details
- **Architecture**: Model-View-Controller pattern with Qt signals/slots
- **Threading**: Multi-threaded downloads with proper UI responsiveness
- **Testing**: Unit, integration, and GUI tests with pytest
- **Build System**: Automated builds for multiple platforms
- **Dependencies**: PyQt6, yt-dlp, minimal external dependencies

## [1.0.0] - 2024-XX-XX

### Added
- Initial public release

---

## Release Notes Template

For future releases, use this template:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New features

### Changed
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Security improvements
```
# YT Leechr - A Feature-Rich GUI for yt-dlp

<div align="center">

![YT Leechr Logo](assets/icon.png)

**A modern, cross-platform graphical user interface for [yt-dlp](https://github.com/yt-dlp/yt-dlp)**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green.svg)](https://pypi.org/project/PyQt6/)
[![Tests](https://img.shields.io/badge/tests-68%20passed-brightgreen.svg)](#testing)
[![GitHub release](https://img.shields.io/github/v/release/buggerman/yt-leechr.svg)](https://github.com/buggerman/yt-leechr/releases)
[![Build Status](https://github.com/buggerman/yt-leechr/workflows/Tests/badge.svg)](https://github.com/buggerman/yt-leechr/actions)
[![Downloads](https://img.shields.io/github/downloads/buggerman/yt-leechr/total.svg)](https://github.com/buggerman/yt-leechr/releases)

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Building](#building) • [Contributing](#contributing)

</div>

---

YT Leechr provides an intuitive interface for downloading videos and audio from hundreds of websites, with advanced features like queue management, format selection, and batch downloads.

## 🚀 Quick Start

**Ready to use? Download the latest release for your platform:**

- **📥 [Download for Windows](https://github.com/buggerman/yt-leechr/releases/latest)** - Standalone `.exe` executable
- **📥 [Download for macOS](https://github.com/buggerman/yt-leechr/releases/latest)** - Native `.app` bundle
- **📥 [Download for Linux](https://github.com/buggerman/yt-leechr/releases/latest)** - Portable executable
- **📦 [Install via Flatpak](#flatpak)** - Universal Linux package with sandboxing

*No installation required! Just download and run.*

## ✨ Features

### 🎯 Core Features
- **🖥️ Intuitive Interface**: Clean, modern GUI with drag-and-drop support
- **📋 Queue Management**: Download multiple videos with real-time progress tracking
- **🎞️ Format Selection**: Choose video quality, extract audio, and customize output formats
- **🎬 Playlist Support**: Download entire playlists or select specific videos
- **📑 Subtitle Support**: Download and embed subtitles in multiple languages
- **🌍 Cross-Platform**: Native builds for Windows, macOS, and Linux

### 🎨 User Experience
- **🌙 Dark Mode**: Supports light, dark, and system themes
- **⚡ High-Quality Icons**: Custom-designed icons for crisp display on all platforms
- **🖱️ Context Menus**: Right-click for advanced options like retry, pause, and folder access
- **⌨️ Keyboard Shortcuts**: Quick access to common functions
- **📱 Responsive Design**: Scales beautifully on different screen sizes

### 🔧 Advanced Features
- **🔀 Batch Downloads**: Paste multiple URLs for simultaneous downloads
- **📁 Custom File Naming**: Flexible templates with variables like title, uploader, date
- **⚙️ Advanced Settings**: Full access to yt-dlp options for power users
- **🔄 Retry Logic**: Automatic retry on failed downloads with exponential backoff
- **📊 Progress Analytics**: Detailed download statistics and speed monitoring

## Installation

### Prerequisites

- Python 3.8 or higher
- FFmpeg (for audio extraction and video conversion)

### Install Dependencies

1. Clone or download this repository
2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

### Install FFmpeg

**Windows:**
- Download from [FFmpeg website](https://ffmpeg.org/download.html)
- Add to your system PATH

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

### Flatpak

YT Leechr is available as a Flatpak for universal Linux distribution support with enhanced security through sandboxing.

**Install from Flathub (Coming Soon):**
```bash
flatpak install flathub com.github.buggerman.yt-leechr
```

**Build from Source:**
```bash
# Install flatpak-builder
sudo apt install flatpak flatpak-builder  # Ubuntu/Debian
sudo dnf install flatpak flatpak-builder  # Fedora

# Add Flathub repository
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

# Build and install
./build-flatpak.sh
```

**Features:**
- 🔒 **Sandboxed Security**: Runs in isolated environment with limited system access
- 🎯 **Minimal Permissions**: Only accesses Downloads, Videos, and Music directories
- 🌐 **Universal**: Works on any Linux distribution with Flatpak support
- 🔄 **Auto-Updates**: Seamless updates through Flatpak system

For detailed Flatpak instructions, see [FLATPAK.md](FLATPAK.md).

## Usage

### Running the Application

```bash
python main.py
```

### Basic Usage

1. **Add Downloads**: Paste video URLs in the input field and click "Download"
2. **Configure Settings**: Use the settings panel to customize output directory, format, and quality
3. **Manage Queue**: Use the queue controls to pause, resume, or clear downloads
4. **Monitor Progress**: Watch real-time download progress in the main table

### Advanced Features

- **Context Menu**: Right-click on downloads for options like retry, copy URL, or open folder
- **Custom Formats**: Use yt-dlp format selectors for advanced quality control
- **Themes**: Switch between light, dark, and system themes via View menu
- **Batch Downloads**: Paste multiple URLs (one per line) for batch downloading

## Configuration

### Settings Options

- **Output Directory**: Choose where downloads are saved
- **File Naming**: Customize filename templates with variables like `%(title)s`, `%(uploader)s`
- **Quality**: Select video/audio quality or extract audio only
- **Subtitles**: Enable subtitle downloads and specify languages
- **Advanced**: Add custom yt-dlp arguments for power users

### Format Examples

- `%(title)s.%(ext)s` - Simple title with extension
- `%(uploader)s - %(title)s.%(ext)s` - Include uploader name
- `%(upload_date)s - %(title)s.%(ext)s` - Include upload date

## Supported Sites

YT Leechr supports the same sites as yt-dlp, including:
- YouTube
- Vimeo
- Dailymotion
- Twitch
- And [many more](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)

## Keyboard Shortcuts

- `Ctrl+V` / `Cmd+V`: Paste clipboard content to URL field
- `Enter`: Add current URL to download queue
- `Delete`: Remove selected downloads from queue

## Troubleshooting

### Common Issues

1. **FFmpeg not found**: Install FFmpeg and ensure it's in your system PATH
2. **Download errors**: Check if the URL is valid and the video is accessible
3. **Slow downloads**: Try reducing concurrent downloads in Advanced settings

### Log Files

Application logs are saved to your system's application data directory for debugging.

## Building

### Development Setup

1. **Clone the repository**
```bash
git clone https://github.com/buggerman/yt-leechr.git
cd yt-leechr
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
# Runtime dependencies
pip install -r requirements.txt

# Development dependencies (optional)
pip install -r requirements-dev.txt
```

### Creating Standalone Executables

YT Leechr includes a comprehensive build system for creating standalone executables:

```bash
# Install build dependencies
pip install pyinstaller

# Build for your platform
python build.py
```

**Build outputs:**
- **Windows**: `YT-Leechr-windows-x64.exe` + portable ZIP package
- **macOS**: `YT Leechr.app` bundle + portable tar.gz package  
- **Linux**: `YT-Leechr-linux-x64` + portable tar.gz package

### Manual Build with PyInstaller

For custom builds, use the included spec file:

```bash
pyinstaller YT-Leechr.spec
```

### Development Commands

Use the included Makefile for common tasks:

```bash
make help          # Show available commands
make install       # Install dependencies
make test          # Run all tests
make test-unit     # Run unit tests only
make clean         # Clean build artifacts
make lint          # Run code linting
make format        # Format code with black
make run           # Run the application
```

## Testing

YT Leechr includes comprehensive test coverage with 68 tests across all modules:

```bash
# Run all tests
make test

# Run specific test categories
make test-unit          # Unit tests only
make test-gui           # GUI tests only  
make test-integration   # Integration tests only

# Run with coverage
python -m pytest --cov=src --cov-report=html
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Start for Contributors

1. Fork the repository on GitHub
2. Clone your fork: `git clone https://github.com/YOUR-USERNAME/yt-leechr.git`
3. Create a feature branch: `git checkout -b feature-name`
4. Make your changes with tests
5. Run the test suite: `make test`
6. Push to your fork and submit a pull request

### Code Quality

- Follow PEP 8 style guidelines
- Add tests for new features
- Ensure all tests pass
- Use type hints where appropriate

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The powerful video downloader that powers this GUI
- [PyQt6](https://pypi.org/project/PyQt6/) - The GUI framework
- [FFmpeg](https://ffmpeg.org/) - Video and audio processing

## Support

- 📖 [Documentation](https://github.com/buggerman/yt-leechr#readme)
- 🐛 [Report Issues](https://github.com/buggerman/yt-leechr/issues)
- 💬 [Discussions](https://github.com/buggerman/yt-leechr/discussions)
- ⭐ Star this repo if you find it useful!

---

<div align="center">
<strong>Made with ❤️ for the open source community</strong>
</div>
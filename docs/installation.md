---
layout: default
title: Installation Guide
description: Complete installation instructions for YT Leechr on all platforms
---

# Installation Guide

YT Leechr offers multiple installation methods to suit different needs and platforms.

## Quick Installation (Recommended)

### Standalone Executables

**No installation required** - just download and run:

- **📥 Windows**: Download `YT-Leechr-windows-x64.exe` from [releases](https://github.com/buggerman/yt-leechr/releases/latest)
- **📥 macOS**: Download `YT Leechr.app` bundle from [releases](https://github.com/buggerman/yt-leechr/releases/latest)
- **📥 Linux**: Download `YT-Leechr-linux-x64` from [releases](https://github.com/buggerman/yt-leechr/releases/latest)

### Flatpak (Linux)

**Universal Linux package with enhanced security:**

```bash
# Install from Flathub (coming soon)
flatpak install flathub io.github.buggerman.yt-leechr

# Run the application
flatpak run io.github.buggerman.yt-leechr
```

**Benefits:**
- 🔒 **Sandboxed Security**: Runs in isolated environment
- 🎯 **Minimal Permissions**: Only accesses Downloads, Videos, and Music directories
- 🌐 **Universal**: Works on any Linux distribution with Flatpak support
- 🔄 **Auto-Updates**: Seamless updates through Flatpak system

## Install from Source

### Prerequisites

- Python 3.8 or higher
- FFmpeg (for audio extraction and video conversion)

### Step 1: Clone Repository

```bash
git clone https://github.com/buggerman/yt-leechr.git
cd yt-leechr
```

### Step 2: Install Python Dependencies

```bash
# Install runtime dependencies
pip install -r requirements.txt

# For development (optional)
pip install -r requirements-dev.txt
```

### Step 3: Install FFmpeg

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

**Linux (Fedora):**
```bash
sudo dnf install ffmpeg
```

**Linux (Arch):**
```bash
sudo pacman -S ffmpeg
```

### Step 4: Run Application

```bash
python main.py
```

## Build from Source

### Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt
```

### Create Standalone Executable

```bash
# Install build dependencies
pip install pyinstaller

# Build for your platform
python build.py
```

**Build outputs:**
- **Windows**: `YT-Leechr-windows-x64.exe` + portable ZIP
- **macOS**: `YT Leechr.app` bundle + portable tar.gz  
- **Linux**: `YT-Leechr-linux-x64` + portable tar.gz

## Flatpak from Source

### Prerequisites

```bash
# Install flatpak-builder
sudo apt install flatpak flatpak-builder  # Ubuntu/Debian
sudo dnf install flatpak flatpak-builder  # Fedora

# Add Flathub repository
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
```

### Build and Install

```bash
# Build flatpak
./build-flatpak.sh

# Or manually:
flatpak run org.flatpak.Builder --force-clean --user --install builddir io.github.buggerman.yt-leechr.json
```

## Verification

After installation, verify YT Leechr is working:

1. **Launch the application**
2. **Check version**: Help → About should show version 0.6.0
3. **Test download**: Try downloading a test video from YouTube
4. **Check FFmpeg**: Advanced settings should detect FFmpeg installation

## Troubleshooting

### Common Issues

**FFmpeg not found:**
- Ensure FFmpeg is installed and in your system PATH
- Restart the application after installing FFmpeg

**PyQt6 installation issues:**
```bash
# Try installing with specific version
pip install PyQt6==6.7.0
```

**Permission denied (Linux):**
```bash
chmod +x YT-Leechr-linux-x64
```

**macOS security warning:**
- Right-click the app → Open → Confirm opening

### Getting Help

- 📖 [User Guide](user-guide) for usage instructions
- 🐛 [Report Issues](https://github.com/buggerman/yt-leechr/issues) for bugs
- 💬 [Discussions](https://github.com/buggerman/yt-leechr/discussions) for questions

---

[← Back to Home](index) | [Next: User Guide →](user-guide)
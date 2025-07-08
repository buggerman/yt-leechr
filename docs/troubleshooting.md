---
layout: default
title: Troubleshooting
description: Common issues and solutions for YT Leechr
---

# Troubleshooting

Common issues and their solutions to help you get YT Leechr working smoothly.

## Installation Issues

### FFmpeg Not Found

**Symptoms:**
- Error: "FFmpeg not found"
- Audio extraction fails
- Video conversion errors

**Solutions:**

**Windows:**
1. Download FFmpeg from [official website](https://ffmpeg.org/download.html)
2. Extract to `C:\ffmpeg\`
3. Add `C:\ffmpeg\bin` to system PATH
4. Restart YT Leechr

**macOS:**
```bash
# Install with Homebrew
brew install ffmpeg

# Or download binary and add to PATH
export PATH="/path/to/ffmpeg:$PATH"
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# Fedora
sudo dnf install ffmpeg

# Arch Linux
sudo pacman -S ffmpeg
```

**Verify Installation:**
```bash
ffmpeg -version
```

### PyQt6 Installation Problems

**Symptoms:**
- Import errors on startup
- "No module named PyQt6"
- GUI not displaying

**Solutions:**

```bash
# Reinstall PyQt6
pip uninstall PyQt6
pip install PyQt6==6.7.0

# For older systems, try PyQt5
pip install PyQt5

# Check installation
python -c "from PyQt6.QtWidgets import QApplication; print('PyQt6 working')"
```

**System-specific Issues:**

**Linux (Ubuntu/Debian):**
```bash
# Install system dependencies
sudo apt install python3-pyqt6 python3-pyqt6.qtmultimedia

# Or build dependencies
sudo apt install build-essential python3-dev
```

**macOS:**
```bash
# Install with Homebrew if pip fails
brew install pyqt6
```

### Python Version Compatibility

**Requirements:**
- Python 3.8 or higher
- 64-bit Python recommended

**Check Python Version:**
```bash
python --version
python -c "import sys; print(sys.version_info)"
```

**Upgrade Python:**
- Download from [python.org](https://python.org)
- Use system package manager
- Consider using pyenv for version management

## Download Issues

### Download Failures

**Common Symptoms:**
- "Video unavailable" errors
- Network timeout errors
- Authentication errors
- Format not available

**Solutions:**

**1. Check Video Availability:**
- Verify URL is correct and accessible
- Check if video is private/restricted
- Try accessing in web browser

**2. Update yt-dlp:**
```bash
pip install --upgrade yt-dlp
```

**3. Clear Browser Cache:**
- Some sites require fresh cookies
- Try incognito/private browsing mode

**4. Retry with Different Settings:**
- Lower quality setting
- Different video format
- Audio-only download

**5. Check Network Connection:**
```bash
# Test connectivity
ping google.com

# Test with simple download
yt-dlp --list-formats https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### Slow Download Speeds

**Causes:**
- Network limitations
- Server throttling
- Too many concurrent downloads

**Solutions:**

**1. Reduce Concurrent Downloads:**
- Set to 1-2 simultaneous downloads
- Monitor network usage

**2. Rate Limiting:**
```bash
# Add to custom arguments
--limit-rate 1M
```

**3. Different Download Times:**
- Try downloading during off-peak hours
- Some sites throttle during busy periods

**4. Network Optimization:**
- Use wired connection instead of WiFi
- Close other bandwidth-heavy applications
- Check with ISP about throttling

### Playlist Download Issues

**Symptoms:**
- Only first video downloads
- Playlist not recognized
- Incomplete playlist downloads

**Solutions:**

**1. Verify Playlist URL:**
- Ensure URL contains playlist ID
- Try copying playlist URL from web browser

**2. Playlist Settings:**
```bash
# Custom arguments for playlists
--yes-playlist --playlist-start 1 --playlist-end 50
```

**3. Handle Unavailable Videos:**
```bash
# Skip unavailable videos
--ignore-errors
```

## Application Issues

### Application Won't Start

**Symptoms:**
- No window appears
- Crashes immediately
- Error messages on startup

**Diagnostic Steps:**

**1. Run from Terminal:**
```bash
# Windows
YT-Leechr-windows-x64.exe

# macOS
./YT\ Leechr.app/Contents/MacOS/YT\ Leechr

# Linux
./YT-Leechr-linux-x64

# Or from source
python main.py
```

**2. Check Error Messages:**
- Look for specific error details
- Note any missing dependencies

**3. Delete Settings:**
```bash
# Windows
del "%APPDATA%\YT-Leechr\settings.ini"

# macOS
rm "~/Library/Application Support/YT-Leechr/settings.ini"

# Linux
rm "~/.config/YT-Leechr/settings.ini"
```

### macOS Security Issues

**Symptoms:**
- "YT Leechr.app is damaged and can't be opened"
- "Cannot verify the developer" warning
- Application blocked by Gatekeeper
- "App can't be opened because it is from an unidentified developer"

**Solutions:**

**1. Remove Quarantine Attributes:**
```bash
# Navigate to the app location and run:
xattr -cr /path/to/YT\ Leechr.app

# Example for Downloads folder:
xattr -cr ~/Downloads/YT\ Leechr.app
```

**2. Allow in Security Settings:**
1. Try to open the app (it will fail)
2. Go to **System Preferences → Security & Privacy → General**
3. Click **"Open Anyway"** next to the blocked app message
4. Confirm by clicking **"Open"** in the dialog

**3. Right-Click Method:**
1. Right-click on **YT Leechr.app**
2. Select **"Open"** from context menu
3. Click **"Open"** in the security dialog

**4. Disable Gatekeeper (Advanced):**
```bash
# Temporarily disable (not recommended)
sudo spctl --master-disable

# Re-enable after installation
sudo spctl --master-enable
```

**Note:** These security warnings appear because the app is not code-signed with an Apple Developer certificate. The `xattr -cr` command removes the quarantine flag that macOS applies to downloaded files.

### GUI Display Issues

**Symptoms:**
- Blank window
- Missing interface elements
- Scaling problems

**Solutions:**

**1. Display Settings:**
```bash
# Force specific display scaling
export QT_SCALE_FACTOR=1.0
python main.py
```

**2. Graphics Driver Issues:**
```bash
# Use software rendering
export QT_QUICK_BACKEND=software
python main.py
```

**3. High DPI Displays:**
```bash
# Enable high DPI scaling
export QT_ENABLE_HIGHDPI_SCALING=1
python main.py
```

### Performance Issues

**Symptoms:**
- Slow UI response
- High CPU/memory usage
- Application freezing

**Solutions:**

**1. Reduce Concurrent Downloads:**
- Limit to 1-2 downloads simultaneously
- Monitor system resources

**2. Clear Download History:**
- Remove completed downloads from queue
- Clear application cache

**3. Check System Resources:**
```bash
# Monitor resource usage
top    # Linux/macOS
taskmgr    # Windows
```

**4. Update Graphics Drivers:**
- Ensure latest graphics drivers installed
- Restart after driver updates

## File and Permission Issues

### Permission Denied Errors

**Symptoms:**
- Cannot save to download directory
- Settings not saving
- File access errors

**Solutions:**

**1. Check Directory Permissions:**
```bash
# Linux/macOS
ls -la ~/Downloads/
chmod 755 ~/Downloads/

# Windows: Run as administrator
```

**2. Change Download Directory:**
- Select different folder with write permissions
- Create new folder in user directory

**3. Antivirus Interference:**
- Add YT Leechr to antivirus exclusions
- Temporarily disable real-time scanning

### File Already Exists

**Symptoms:**
- Download fails with "file exists" error
- Duplicate files created

**Solutions:**

**1. Enable Overwrite:**
```bash
# Custom argument
--force-overwrites
```

**2. Use Archive Feature:**
```bash
# Skip already downloaded
--download-archive downloaded.txt
```

**3. Unique Naming:**
- Include date/time in filename template
- Use `%(autonumber)s` for unique numbers

## Network and Connectivity

### Proxy Issues

**Symptoms:**
- Connection timeout in corporate networks
- "Network unreachable" errors

**Solutions:**

**1. Configure Proxy:**
```bash
# HTTP proxy
--proxy http://proxy.company.com:8080

# SOCKS proxy  
--proxy socks5://proxy.company.com:1080

# With authentication
--proxy http://username:password@proxy.company.com:8080
```

**2. System Proxy Settings:**
- Use system proxy configuration
- Check corporate firewall settings

### DNS Issues

**Symptoms:**
- Cannot resolve domain names
- Intermittent connectivity

**Solutions:**

**1. Change DNS Servers:**
- Use Google DNS: 8.8.8.8, 8.8.4.4
- Use Cloudflare DNS: 1.1.1.1, 1.0.0.1

**2. Flush DNS Cache:**
```bash
# Windows
ipconfig /flushdns

# macOS
sudo dscacheutil -flushcache

# Linux
sudo systemctl restart systemd-resolved
```

## Site-Specific Issues

### YouTube Issues

**Common Problems:**
- "Video unavailable" for available videos
- Throttling or slow downloads
- Age-restricted content

**Solutions:**

**1. Cookie Authentication:**
```bash
# Export cookies from browser
--cookies-from-browser chrome
```

**2. Account Login:**
```bash
# Use YouTube account
--username your_username --password your_password
```

**3. Different User Agent:**
```bash
# Mimic different browser
--user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
```

### Instagram/TikTok Issues

**Problems:**
- Private content access
- Session management
- Rate limiting

**Solutions:**

**1. Browser Cookies:**
- Export cookies from logged-in session
- Use cookies for authentication

**2. Rate Limiting:**
```bash
# Slow down requests
--sleep-interval 1 --max-sleep-interval 5
```

## Advanced Troubleshooting

### Debug Mode

**Enable Verbose Logging:**
```bash
# Run with debug output
python main.py --debug

# Or add to custom arguments
--verbose --print-traffic
```

### Log Files

**Location:**
```bash
# Windows
%APPDATA%\YT-Leechr\logs\

# macOS
~/Library/Logs/YT-Leechr/

# Linux
~/.local/share/YT-Leechr/logs/
```

**Analyzing Logs:**
- Look for error patterns
- Check timestamp correlation
- Note repeated failures

### Clean Reinstallation

**Complete Removal:**
```bash
# Remove application
rm -rf /path/to/yt-leechr

# Remove settings and cache
# Windows
rmdir /s "%APPDATA%\YT-Leechr"

# macOS  
rm -rf "~/Library/Application Support/YT-Leechr"
rm -rf "~/Library/Caches/YT-Leechr"

# Linux
rm -rf "~/.config/YT-Leechr"
rm -rf "~/.cache/YT-Leechr"
```

**Fresh Installation:**
1. Download latest release
2. Install dependencies
3. Configure settings fresh

## Getting Help

### Before Reporting Issues

**Gather Information:**
- YT Leechr version
- Operating system and version
- Python version
- Error messages and logs
- Steps to reproduce

**Check Existing Issues:**
- Search [GitHub issues](https://github.com/buggerman/yt-leechr/issues)
- Look for similar problems
- Check if issue is already reported

### Reporting Bugs

**Include in Bug Report:**
```
- YT Leechr version: 0.6.0
- OS: Windows 11 / macOS 13 / Ubuntu 22.04
- Python: 3.10.8
- PyQt6: 6.7.0
- Error message: [full error text]
- Steps to reproduce: [detailed steps]
- Expected behavior: [what should happen]
- Actual behavior: [what actually happens]
```

### Community Support

- 🐛 [GitHub Issues](https://github.com/buggerman/yt-leechr/issues) - Bug reports
- 💬 [GitHub Discussions](https://github.com/buggerman/yt-leechr/discussions) - Questions and support
- 📖 [Documentation](https://buggerman.github.io/yt-leechr/) - Comprehensive guides

---

[← Testing](testing) | [Back to Home](index)
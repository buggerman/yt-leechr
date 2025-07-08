---
layout: default
title: Configuration
description: Detailed configuration options and customization for YT Leechr
---

# Configuration

Customize YT Leechr to fit your workflow with comprehensive settings and advanced options.

## Settings Panel

Access settings by clicking the gear icon (⚙️) in the main window toolbar.

## Basic Settings

### Output Directory

**Purpose**: Choose where downloaded files are saved

**Options:**
- **Default**: Downloads folder in your home directory
- **Custom**: Browse to select any folder
- **Per-format**: Use different folders for video/audio

**Examples:**
```
~/Downloads/YT-Leechr/          # Organized subfolder
~/Videos/Downloaded/            # Video-specific location
/media/storage/downloads/       # External storage
```

### File Naming Templates

**Purpose**: Customize how downloaded files are named using variables

**Common Variables:**
- `%(title)s` - Video title
- `%(uploader)s` - Channel/uploader name
- `%(upload_date)s` - Upload date (YYYYMMDD)
- `%(duration)s` - Video duration
- `%(view_count)s` - View count
- `%(ext)s` - File extension

**Template Examples:**

```bash
# Simple title with extension
%(title)s.%(ext)s

# Include uploader name
%(uploader)s - %(title)s.%(ext)s

# Organized by date
%(upload_date)s - %(title)s.%(ext)s

# Full organization
%(uploader)s/%(upload_date>%Y-%m-%d)s - %(title)s.%(ext)s

# With view count
%(title)s [%(view_count)s views].%(ext)s
```

**Advanced Templates:**
```bash
# Create folders by uploader
%(uploader)s/%(title)s.%(ext)s

# Organize by year and month
%(upload_date>%Y)s/%(upload_date>%m)s/%(title)s.%(ext)s

# Include quality in filename
%(title)s [%(height)sp].%(ext)s
```

## Quality and Format Settings

### Video Quality

**Best Available (Default):**
- Downloads highest quality available
- Balances file size and quality
- Recommended for most users

**Specific Resolution:**
- 2160p (4K)
- 1440p (2K)
- 1080p (Full HD)
- 720p (HD)
- 480p (Standard)
- 360p (Low)

**Audio Only:**
- Extract audio track only
- Ideal for music, podcasts, lectures
- Smaller file sizes

### Video Formats

**MP4 (Recommended):**
- Best compatibility
- Plays on all devices
- Good compression

**MKV:**
- Supports multiple audio tracks
- Better for archival
- May need specific players

**WebM:**
- Open source format
- Good compression
- Web-optimized

**Original:**
- No conversion
- Fastest download
- Format depends on source

### Audio Formats

**MP3:**
- Universal compatibility
- Good compression
- Most popular format

**M4A:**
- Better quality than MP3
- Smaller file sizes
- Apple ecosystem friendly

**OGG:**
- Open source
- Excellent compression
- Linux/Android friendly

**FLAC:**
- Lossless compression
- Largest file sizes
- Audiophile quality

### Audio Quality

**Best Available:**
- Highest bitrate available
- Best quality

**High (320 kbps):**
- Excellent quality
- Larger files

**Medium (192 kbps):**
- Good quality
- Balanced file size

**Low (128 kbps):**
- Acceptable quality
- Smallest files

## Advanced Settings

### Download Behavior

**Maximum Concurrent Downloads:**
- Range: 1-5 simultaneous downloads
- Lower = more stable, higher = faster (if bandwidth allows)
- Consider your internet speed and CPU

**Retry Attempts:**
- Number of retry attempts for failed downloads
- Automatic exponential backoff between retries
- Range: 1-10 attempts

**Download Timeout:**
- Maximum time to wait for download start
- Prevents hanging on slow/unavailable content
- Range: 30-300 seconds

### Subtitle Settings

**Download Subtitles:**
- Enable automatic subtitle download
- Available languages depend on source

**Subtitle Languages:**
- Primary: Preferred language (e.g., 'en' for English)
- Secondary: Fallback language
- 'all': Download all available languages

**Subtitle Format:**
- SRT: Most compatible
- VTT: Web standard
- ASS: Advanced styling

**Embed Subtitles:**
- Include subtitles in video file
- Only works with MP4/MKV formats
- Convenient but increases file size

### Network Settings

**Proxy Configuration:**
- HTTP/HTTPS proxy support
- SOCKS proxy support
- Authentication support

**User Agent:**
- Custom browser user agent
- Helps bypass some restrictions
- Use for compatibility issues

**Rate Limiting:**
- Limit download speed
- Useful for shared connections
- Format: "50K" (50 KB/s), "1M" (1 MB/s)

## Custom yt-dlp Arguments

**Purpose**: Add any yt-dlp command-line options for advanced users

**Common Examples:**

```bash
# Download age-restricted content (requires login)
--username YOUR_USERNAME --password YOUR_PASSWORD

# Download private/unlisted videos (requires cookies)
--cookies-from-browser chrome

# Extract additional metadata
--write-info-json --write-thumbnail

# Download specific playlist range
--playlist-start 5 --playlist-end 10

# Skip unavailable videos in playlists
--ignore-errors

# Download with specific format preference
--format "best[height<=720]"

# Archive downloaded videos (skip already downloaded)
--download-archive archive.txt

# Add video description to filename
--output "%(title)s - %(description)s.%(ext)s"
```

**Security Note**: Never share configurations containing passwords or cookies.

## Presets and Profiles

### Quick Presets

**Music Downloads:**
- Audio only: MP3
- Quality: High (320 kbps)
- Template: `%(uploader)s - %(title)s.%(ext)s`

**Video Archive:**
- Format: MKV
- Quality: Best available
- Subtitles: All languages
- Template: `%(upload_date)s - %(uploader)s - %(title)s.%(ext)s`

**Quick Watch:**
- Format: MP4
- Quality: 720p
- Template: `%(title)s.%(ext)s`

**Podcast Downloads:**
- Audio only: MP3
- Quality: Medium (192 kbps)
- Template: `%(uploader)s/%(title)s.%(ext)s`

## Configuration Files

### Settings Location

**Windows:**
```
%APPDATA%/YT-Leechr/settings.ini
```

**macOS:**
```
~/Library/Application Support/YT-Leechr/settings.ini
```

**Linux:**
```
~/.config/YT-Leechr/settings.ini
```

### Backup and Restore

**Export Settings:**
1. Copy settings.ini file
2. Save to backup location
3. Include in your backup routine

**Import Settings:**
1. Close YT Leechr
2. Replace settings.ini with backup
3. Restart application

### Reset to Defaults

1. Close YT Leechr
2. Delete settings.ini file
3. Restart application
4. Reconfigure preferred settings

## Troubleshooting Configuration

### Common Issues

**Settings not saving:**
- Check file permissions
- Ensure application has write access
- Try running as administrator (Windows)

**Invalid templates:**
- Test templates with simple downloads
- Check variable spelling
- Avoid special characters in paths

**Download failures with custom args:**
- Test arguments with yt-dlp directly
- Remove arguments one by one to isolate issues
- Check yt-dlp documentation for syntax

### Performance Optimization

**For fast connections:**
- Increase concurrent downloads (3-5)
- Use best quality settings
- Enable parallel downloads in advanced args

**For slow connections:**
- Limit to 1-2 concurrent downloads
- Use lower quality settings
- Enable rate limiting if needed

**For limited storage:**
- Use audio-only for non-video content
- Use lower quality settings
- Enable automatic cleanup options

---

[← User Guide](user-guide) | [Next: Development →](development)
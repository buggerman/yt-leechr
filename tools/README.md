# Bundled Tools Directory

This directory is for bundling external tools with YT Leechr executables.

## Muxing Tools

YT Leechr can automatically mux separate video and audio files into single containers. To enable this functionality, you can bundle muxing tools:

### FFmpeg (Recommended)
1. Download ffmpeg binary for your platform from https://ffmpeg.org/download.html
2. Place the executable in this directory as:
   - `ffmpeg` (Linux/macOS)
   - `ffmpeg.exe` (Windows)

### MKVToolNix (Alternative)
1. Download mkvtoolnix from https://mkvtoolnix.download/
2. Extract and place the `mkvmerge` executable in this directory as:
   - `mkvmerge` (Linux/macOS) 
   - `mkvmerge.exe` (Windows)

## Build Integration

The build script will automatically include any executables in this directory with the final application bundle.

## Licensing Note

When bundling external tools, ensure you comply with their respective licenses:
- FFmpeg: LGPL/GPL (depending on build configuration)
- MKVToolNix: GPL v2

For distribution, consider:
1. Documenting bundled tools and their licenses
2. Including license files
3. Providing source code links as required by GPL

## Fallback Behavior

If no bundled tools are found, YT Leechr will:
1. Try to use system-installed ffmpeg/mkvmerge
2. Fall back to downloading separate video/audio files
3. Display helpful messages to users about installing tools
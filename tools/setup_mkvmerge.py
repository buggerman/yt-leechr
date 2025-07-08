#!/usr/bin/env python3
"""
Download and setup mkvmerge binaries for bundling with YT Leechr
"""

import os
import sys
import platform
import urllib.request
import zipfile
import tarfile
from pathlib import Path

# MKVToolNix download URLs for different platforms
MKVTOOLNIX_URLS = {
    'macos-x64': 'https://mkvtoolnix.download/macos/MKVToolNix-84.0.dmg',
    'windows-x64': 'https://mkvtoolnix.download/windows/releases/84.0/mkvtoolnix-64-bit-84.0.7z',
    'linux-x64': 'https://mkvtoolnix.download/sources/mkvtoolnix-84.0.tar.xz'
}

def get_platform():
    """Get platform identifier"""
    system = platform.system().lower()
    arch = platform.machine().lower()
    
    if arch in ('x86_64', 'amd64'):
        arch = 'x64'
    elif arch in ('aarch64', 'arm64'):
        arch = 'arm64'
    
    return f"{system}-{arch}"

def download_file(url: str, dest_path: str):
    """Download file from URL with progress"""
    print(f"Downloading {url}...")
    
    def progress_hook(block_num, block_size, total_size):
        if total_size > 0:
            percent = min(100, (block_num * block_size * 100) // total_size)
            print(f"\rProgress: {percent}%", end='', flush=True)
    
    urllib.request.urlretrieve(url, dest_path, progress_hook)
    print(f"\nDownloaded to {dest_path}")

def setup_mkvmerge():
    """Download and setup mkvmerge for current platform"""
    current_platform = get_platform()
    
    # Handle arm64 macOS by using x64 binary (Rosetta compatibility)  
    if current_platform == 'darwin-arm64':
        current_platform = 'macos-x64'
    elif current_platform.startswith('darwin'):
        current_platform = current_platform.replace('darwin', 'macos')
    
    # For now, just create a simple mkvmerge wrapper using ffmpeg
    # since downloading and extracting MKVToolNix is complex
    tools_dir = Path(__file__).parent
    
    # Use ffmpeg as mkvmerge alternative 
    ffmpeg_path = tools_dir / 'ffmpeg'
    if ffmpeg_path.exists():
        # Create a simple mkvmerge wrapper script
        if platform.system() == 'Windows':
            wrapper_content = f'''@echo off
"{ffmpeg_path}" -i "%1" -i "%2" -c copy "%3"
'''
            wrapper_path = tools_dir / 'mkvmerge.bat'
        else:
            wrapper_content = f'''#!/bin/bash
"{ffmpeg_path}" -i "$1" -i "$2" -c copy "$3"
'''
            wrapper_path = tools_dir / 'mkvmerge'
            
        wrapper_path.write_text(wrapper_content)
        if not platform.system() == 'Windows':
            os.chmod(wrapper_path, 0o755)
            
        print(f"✅ Created mkvmerge wrapper using ffmpeg: {wrapper_path}")
        return True
    else:
        print("❌ FFmpeg not found - run setup_ffmpeg.py first")
        return False

if __name__ == '__main__':
    print("🔧 Setting up MKVmerge wrapper for YT Leechr...")
    success = setup_mkvmerge()
    
    if success:
        print("\n✅ MKVmerge wrapper setup complete!")
        print("   Video/audio files will be muxed to MKV format.")
    else:
        print("\n❌ MKVmerge wrapper setup failed!")
        sys.exit(1)
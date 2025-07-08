#!/usr/bin/env python3
"""
Download and setup ffmpeg binaries for bundling with YT Leechr
"""

import os
import sys
import platform
import urllib.request
import tarfile
import zipfile
import shutil
from pathlib import Path

# FFmpeg download URLs for different platforms
FFMPEG_URLS = {
    'linux-x64': 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.tar.xz',
    'windows-x64': 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip',
    'macos-x64': 'https://evermeet.cx/ffmpeg/getrelease/zip',  # Universal binary
}

def get_platform():
    """Get platform identifier"""
    system = platform.system().lower()
    arch = platform.machine().lower()
    
    if arch in ('x86_64', 'amd64'):
        arch = 'x64'
    elif arch in ('i386', 'i686'):
        arch = 'x86'
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

def extract_ffmpeg_linux(tar_path: str, dest_dir: str) -> bool:
    """Extract ffmpeg from Linux tar.xz archive"""
    try:
        with tarfile.open(tar_path, 'r:xz') as tar:
            # Find the ffmpeg binary in the archive
            for member in tar.getmembers():
                if member.name.endswith('/bin/ffmpeg'):
                    # Extract just the ffmpeg binary
                    member.name = 'ffmpeg'  # Rename to simple name
                    tar.extract(member, dest_dir)
                    # Make executable
                    ffmpeg_path = os.path.join(dest_dir, 'ffmpeg')
                    os.chmod(ffmpeg_path, 0o755)
                    print(f"Extracted ffmpeg to {ffmpeg_path}")
                    return True
        return False
    except Exception as e:
        print(f"Failed to extract Linux ffmpeg: {e}")
        return False

def extract_ffmpeg_windows(zip_path: str, dest_dir: str) -> bool:
    """Extract ffmpeg from Windows zip archive"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            # Find the ffmpeg.exe binary in the archive
            for file_info in zip_file.filelist:
                if file_info.filename.endswith('/bin/ffmpeg.exe'):
                    # Extract just the ffmpeg.exe binary
                    file_info.filename = 'ffmpeg.exe'  # Rename to simple name
                    zip_file.extract(file_info, dest_dir)
                    ffmpeg_path = os.path.join(dest_dir, 'ffmpeg.exe')
                    print(f"Extracted ffmpeg.exe to {ffmpeg_path}")
                    return True
        return False
    except Exception as e:
        print(f"Failed to extract Windows ffmpeg: {e}")
        return False

def extract_ffmpeg_macos(zip_path: str, dest_dir: str) -> bool:
    """Extract ffmpeg from macOS zip archive"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            # Extract ffmpeg binary
            zip_file.extract('ffmpeg', dest_dir)
            ffmpeg_path = os.path.join(dest_dir, 'ffmpeg')
            # Make executable
            os.chmod(ffmpeg_path, 0o755)
            print(f"Extracted ffmpeg to {ffmpeg_path}")
            return True
    except Exception as e:
        print(f"Failed to extract macOS ffmpeg: {e}")
        return False

def setup_ffmpeg():
    """Download and setup ffmpeg for current platform"""
    current_platform = get_platform()
    
    # Handle arm64 macOS by using x64 binary (Rosetta compatibility)
    if current_platform == 'darwin-arm64':
        current_platform = 'macos-x64'
    elif current_platform.startswith('darwin'):
        current_platform = current_platform.replace('darwin', 'macos')
    
    if current_platform not in FFMPEG_URLS:
        print(f"Platform {current_platform} not supported")
        return False
    
    # Create tools directory
    tools_dir = Path(__file__).parent
    tools_dir.mkdir(exist_ok=True)
    
    url = FFMPEG_URLS[current_platform]
    filename = f"ffmpeg-{current_platform}.{'zip' if 'zip' in url else 'tar.xz'}"
    download_path = tools_dir / filename
    
    try:
        # Download ffmpeg
        download_file(url, str(download_path))
        
        # Extract based on platform
        success = False
        if current_platform.startswith('linux'):
            success = extract_ffmpeg_linux(str(download_path), str(tools_dir))
        elif current_platform.startswith('windows'):
            success = extract_ffmpeg_windows(str(download_path), str(tools_dir))
        elif current_platform.startswith('macos'):
            success = extract_ffmpeg_macos(str(download_path), str(tools_dir))
        
        # Clean up downloaded archive
        try:
            os.remove(download_path)
        except OSError:
            pass
        
        if success:
            print(f"✅ FFmpeg successfully set up for {current_platform}")
            
            # Create license compliance file
            license_file = tools_dir / 'FFMPEG_LICENSE.txt'
            license_file.write_text('''FFmpeg License Information

This application bundles FFmpeg, which is licensed under the GPL v3.

FFmpeg is free software; you can redistribute it and/or modify it under the 
terms of the GNU General Public License as published by the Free Software 
Foundation; either version 3 of the License, or (at your option) any later version.

Source code for FFmpeg is available at: https://github.com/FFmpeg/FFmpeg
Pre-compiled builds from: https://github.com/BtbN/FFmpeg-Builds

For complete license text, see: https://www.gnu.org/licenses/gpl-3.0.html
''')
            print(f"📄 Created license compliance file: {license_file}")
            return True
        else:
            print(f"❌ Failed to extract ffmpeg")
            return False
            
    except Exception as e:
        print(f"❌ Failed to setup ffmpeg: {e}")
        return False

if __name__ == '__main__':
    print("🔧 Setting up FFmpeg for YT Leechr...")
    success = setup_ffmpeg()
    
    if success:
        print("\n✅ FFmpeg setup complete!")
        print("   The next build will include ffmpeg for automatic video/audio muxing.")
    else:
        print("\n❌ FFmpeg setup failed!")
        print("   Builds will fall back to system-installed ffmpeg or separate files.")
        sys.exit(1)
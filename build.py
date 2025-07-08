#!/usr/bin/env python3
"""
Build script for YT Leechr standalone executables
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path

def get_platform_name():
    """Get platform-specific name for builds"""
    system = platform.system().lower()
    arch = platform.machine().lower()
    
    if arch in ('x86_64', 'amd64'):
        arch = 'x64'
    elif arch in ('aarch64', 'arm64'):
        arch = 'arm64'
    elif arch.startswith('arm'):
        arch = 'arm'
    
    return f"{system}-{arch}"

def clean_build():
    """Clean previous build artifacts"""
    print("🧹 Cleaning previous builds...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   Removed {dir_name}/")
    
    # Clean .pyc files
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                os.remove(os.path.join(root, file))

def build_executable():
    """Build standalone executable with PyInstaller"""
    print("🔨 Building standalone executable...")
    
    platform_name = get_platform_name()
    
    # PyInstaller command
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name', f'YT-Leechr-{platform_name}',
        '--icon', 'assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
        '--add-data', 'src:src',
        '--hidden-import', 'PyQt6.QtCore',
        '--hidden-import', 'PyQt6.QtGui',
        '--hidden-import', 'PyQt6.QtWidgets',
        '--hidden-import', 'yt_dlp',
        '--collect-all', 'yt_dlp',
        'main.py'
    ]
    
    # Remove None values
    cmd = [arg for arg in cmd if arg is not None]
    
    print(f"   Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("   ✅ Build successful!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Build failed: {e}")
        print(f"   stdout: {e.stdout}")
        print(f"   stderr: {e.stderr}")
        return False

def create_app_bundle_macos():
    """Create macOS app bundle"""
    if platform.system() != 'Darwin':
        return
        
    print("🍎 Creating macOS app bundle...")
    
    app_name = "YT Leechr.app"
    app_path = f"dist/{app_name}"
    
    # Create app bundle structure
    os.makedirs(f"{app_path}/Contents/MacOS", exist_ok=True)
    os.makedirs(f"{app_path}/Contents/Resources", exist_ok=True)
    
    # Move executable
    executable_name = f"YT-Leechr-{get_platform_name()}"
    if os.path.exists(f"dist/{executable_name}"):
        shutil.move(f"dist/{executable_name}", f"{app_path}/Contents/MacOS/YT-Leechr")
        os.chmod(f"{app_path}/Contents/MacOS/YT-Leechr", 0o755)
    
    # Create Info.plist
    info_plist = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>YT-Leechr</string>
    <key>CFBundleIdentifier</key>
    <string>com.github.buggerman.yt-leechr</string>
    <key>CFBundleName</key>
    <string>YT Leechr</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.14</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSHumanReadableCopyright</key>
    <string>© 2024 buggerman. Licensed under MIT License.</string>
</dict>
</plist>"""
    
    with open(f"{app_path}/Contents/Info.plist", 'w') as f:
        f.write(info_plist)
    
    print(f"   ✅ Created {app_name}")

def create_portable_package():
    """Create portable package with all dependencies"""
    print("📦 Creating portable package...")
    
    platform_name = get_platform_name()
    package_name = f"YT-Leechr-{platform_name}-portable"
    package_dir = f"dist/{package_name}"
    
    os.makedirs(package_dir, exist_ok=True)
    
    # Copy executable
    executable_name = f"YT-Leechr-{platform_name}"
    if os.path.exists(f"dist/{executable_name}"):
        shutil.copy2(f"dist/{executable_name}", package_dir)
    
    # Copy documentation
    docs_to_copy = ['README.md', 'LICENSE']
    for doc in docs_to_copy:
        if os.path.exists(doc):
            shutil.copy2(doc, package_dir)
    
    # Create run script
    if platform.system() == 'Windows':
        run_script = f"@echo off\n{executable_name}.exe %*\n"
        with open(f"{package_dir}/run.bat", 'w') as f:
            f.write(run_script)
    else:
        run_script = f"#!/bin/bash\n./{executable_name} \"$@\"\n"
        with open(f"{package_dir}/run.sh", 'w') as f:
            f.write(run_script)
        os.chmod(f"{package_dir}/run.sh", 0o755)
    
    # Create archive
    archive_name = f"dist/{package_name}"
    if platform.system() == 'Windows':
        shutil.make_archive(archive_name, 'zip', 'dist', package_name)
        print(f"   ✅ Created {package_name}.zip")
    else:
        shutil.make_archive(archive_name, 'gztar', 'dist', package_name)
        print(f"   ✅ Created {package_name}.tar.gz")

def main():
    """Main build process"""
    print("🚀 YT Leechr Build Script")
    print(f"   Platform: {get_platform_name()}")
    print()
    
    # Check if PyInstaller is available
    try:
        subprocess.run(['pyinstaller', '--version'], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ PyInstaller not found. Install with: pip install pyinstaller")
        return 1
    
    # Build process
    clean_build()
    
    if not build_executable():
        return 1
    
    if platform.system() == 'Darwin':
        create_app_bundle_macos()
    
    create_portable_package()
    
    print()
    print("✅ Build completed successfully!")
    print(f"   Check the dist/ directory for your builds")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
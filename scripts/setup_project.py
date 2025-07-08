#!/usr/bin/env python3
"""
Project setup and validation script for YT Leechr
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is supported"""
    version = sys.version_info
    if version < (3, 8):
        print(f"❌ Python 3.8+ required, found {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """Check if required dependencies are available"""
    required_packages = [
        'PyQt6',
        'yt_dlp',
        'pytest'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_').lower())
            print(f"✅ {package}")
        except ImportError:
            missing.append(package)
            print(f"❌ {package}")
    
    if missing:
        print(f"\nMissing packages: {', '.join(missing)}")
        print("Install with: pip install -r requirements-dev.txt")
        return False
    
    return True

def check_project_structure():
    """Validate project structure"""
    required_dirs = [
        'src',
        'tests',
        'scripts',
        'assets',
        'docs',
        '.github/workflows'
    ]
    
    required_files = [
        'main.py',
        'setup.py',
        'requirements.txt',
        'requirements-dev.txt',
        'README.md',
        'LICENSE',
        'CONTRIBUTING.md',
        'CHANGELOG.md',
        'Makefile',
        'build.py',
        'YT-Leechr.spec'
    ]
    
    print("📁 Checking project structure...")
    
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✅ {directory}/")
        else:
            print(f"❌ {directory}/")
            return False
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            return False
    
    return True

def run_tests():
    """Run the test suite"""
    print("🧪 Running tests...")
    
    try:
        result = subprocess.run(
            ['python', '-m', 'pytest', 'tests/', '-v', '--tb=short'],
            capture_output=True,
            text=True,
            env={**os.environ, 'QT_QPA_PLATFORM': 'offscreen'}
        )
        
        if result.returncode == 0:
            print("✅ All tests passed!")
            return True
        else:
            print("❌ Tests failed!")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def check_build_system():
    """Check if build system works"""
    print("🔨 Checking build system...")
    
    try:
        # Try importing PyInstaller
        import PyInstaller
        print("✅ PyInstaller available")
        
        # Check if build script exists and is executable
        if os.path.exists('build.py') and os.access('build.py', os.X_OK):
            print("✅ Build script executable")
        else:
            print("❌ Build script not executable")
            return False
        
        return True
    except ImportError:
        print("❌ PyInstaller not available")
        print("Install with: pip install pyinstaller")
        return False

def create_sample_icon():
    """Create a simple placeholder icon if none exists"""
    icon_path = 'assets/icon.png'
    
    if not os.path.exists(icon_path):
        print("💡 Creating placeholder icon...")
        
        # Create a simple SVG icon as placeholder
        svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="256" height="256" viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg">
    <rect width="256" height="256" fill="#2196F3"/>
    <circle cx="128" cy="128" r="80" fill="white"/>
    <polygon points="110,90 110,166 170,128" fill="#2196F3"/>
</svg>'''
        
        svg_path = 'assets/icon.svg'
        with open(svg_path, 'w') as f:
            f.write(svg_content)
        
        print(f"✅ Created placeholder icon: {svg_path}")
        print("   Replace with your own icon for production builds")

def cleanup_project():
    """Clean up any temporary files"""
    print("🧹 Cleaning up...")
    
    patterns_to_clean = [
        '**/__pycache__',
        '**/*.pyc',
        '**/*.pyo',
        '.pytest_cache',
        'htmlcov',
        '.coverage',
        'dist',
        'build',
        '*.egg-info'
    ]
    
    for pattern in patterns_to_clean:
        for path in Path('.').glob(pattern):
            if path.exists():
                if path.is_dir():
                    shutil.rmtree(path)
                    print(f"   Removed directory: {path}")
                else:
                    path.unlink()
                    print(f"   Removed file: {path}")

def main():
    """Main setup and validation process"""
    print("🚀 YT Leechr Project Setup & Validation")
    print("=" * 50)
    
    all_checks_passed = True
    
    # Check Python version
    if not check_python_version():
        all_checks_passed = False
    
    print()
    
    # Check dependencies
    print("📦 Checking dependencies...")
    if not check_dependencies():
        all_checks_passed = False
    
    print()
    
    # Check project structure
    if not check_project_structure():
        all_checks_passed = False
    
    print()
    
    # Clean up first
    cleanup_project()
    
    print()
    
    # Run tests
    if check_dependencies():  # Only run tests if dependencies are available
        if not run_tests():
            all_checks_passed = False
    
    print()
    
    # Check build system
    if not check_build_system():
        all_checks_passed = False
    
    print()
    
    # Create sample assets if needed
    create_sample_icon()
    
    print()
    print("=" * 50)
    
    if all_checks_passed:
        print("✅ Project setup complete! YT Leechr is ready for development.")
        print()
        print("Next steps:")
        print("  1. Run the app: python main.py")
        print("  2. Run tests: make test")
        print("  3. Build executable: make build")
        print("  4. See Makefile for more commands: make help")
        return 0
    else:
        print("❌ Setup incomplete. Please fix the issues above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
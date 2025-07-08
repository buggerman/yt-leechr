#!/usr/bin/env python3
"""
Release automation script for YT Leechr
"""

import os
import sys
import subprocess
import json
import re
from pathlib import Path
from datetime import datetime

def get_version():
    """Get current version from setup.py"""
    with open('setup.py', 'r') as f:
        content = f.read()
        match = re.search(r'version="([^"]+)"', content)
        if match:
            return match.group(1)
    return None

def bump_version(current_version, bump_type):
    """Bump version number"""
    major, minor, patch = map(int, current_version.split('.'))
    
    if bump_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif bump_type == 'minor':
        minor += 1
        patch = 0
    elif bump_type == 'patch':
        patch += 1
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")
    
    return f"{major}.{minor}.{patch}"

def update_version_files(new_version):
    """Update version in all relevant files"""
    files_to_update = [
        ('setup.py', r'version="[^"]+"', f'version="{new_version}"'),
        ('src/__init__.py', r'__version__ = "[^"]+"', f'__version__ = "{new_version}"'),
    ]
    
    for file_path, pattern, replacement in files_to_update:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
            
            content = re.sub(pattern, replacement, content)
            
            with open(file_path, 'w') as f:
                f.write(content)
            
            print(f"Updated {file_path}")

def update_changelog(version):
    """Update CHANGELOG.md with new version"""
    changelog_path = 'CHANGELOG.md'
    
    if not os.path.exists(changelog_path):
        return
    
    with open(changelog_path, 'r') as f:
        content = f.read()
    
    # Replace [Unreleased] with version and date
    today = datetime.now().strftime('%Y-%m-%d')
    content = content.replace(
        '## [Unreleased]',
        f'## [{version}] - {today}'
    )
    
    # Add new Unreleased section
    content = content.replace(
        f'## [{version}] - {today}',
        f'## [Unreleased]\n\n### Added\n### Changed\n### Fixed\n\n## [{version}] - {today}'
    )
    
    with open(changelog_path, 'w') as f:
        f.write(content)
    
    print(f"Updated {changelog_path}")

def run_tests():
    """Run the test suite"""
    print("Running tests...")
    result = subprocess.run(['python', '-m', 'pytest', 'tests/', '-v'], 
                          capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Tests failed!")
        print(result.stdout)
        print(result.stderr)
        return False
    
    print("All tests passed!")
    return True

def build_executables():
    """Build standalone executables"""
    print("Building executables...")
    result = subprocess.run(['python', 'build.py'], capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Build failed!")
        print(result.stdout)
        print(result.stderr)
        return False
    
    print("Build completed successfully!")
    return True

def git_operations(version):
    """Perform git operations for release"""
    commands = [
        ['git', 'add', '.'],
        ['git', 'commit', '-m', f'chore: release v{version}'],
        ['git', 'tag', '-a', f'v{version}', '-m', f'Release v{version}'],
    ]
    
    for cmd in commands:
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Command failed: {' '.join(cmd)}")
            print(result.stderr)
            return False
    
    print("Git operations completed successfully!")
    return True

def create_github_release(version):
    """Create GitHub release (requires gh CLI)"""
    try:
        # Check if gh CLI is available
        subprocess.run(['gh', '--version'], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("GitHub CLI not found. Skipping GitHub release creation.")
        print("You can create a release manually or install gh CLI.")
        return True
    
    # Generate release notes from changelog
    release_notes = f"Release v{version}\n\nSee CHANGELOG.md for detailed changes."
    
    cmd = [
        'gh', 'release', 'create', f'v{version}',
        '--title', f'v{version}',
        '--notes', release_notes,
        '--draft'
    ]
    
    # Add build artifacts if they exist
    dist_files = []
    if os.path.exists('dist'):
        for file in os.listdir('dist'):
            if file.endswith(('.exe', '.app', '.zip', '.tar.gz')):
                dist_files.append(os.path.join('dist', file))
    
    cmd.extend(dist_files)
    
    print(f"Creating GitHub release: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("GitHub release creation failed!")
        print(result.stderr)
        return False
    
    print("GitHub release created successfully!")
    return True

def main():
    """Main release process"""
    if len(sys.argv) != 2:
        print("Usage: python release.py <bump_type>")
        print("bump_type: major, minor, patch")
        sys.exit(1)
    
    bump_type = sys.argv[1]
    if bump_type not in ['major', 'minor', 'patch']:
        print("Error: bump_type must be major, minor, or patch")
        sys.exit(1)
    
    # Get current version
    current_version = get_version()
    if not current_version:
        print("Error: Could not determine current version")
        sys.exit(1)
    
    # Calculate new version
    new_version = bump_version(current_version, bump_type)
    
    print(f"🚀 Releasing YT Leechr")
    print(f"   Current version: {current_version}")
    print(f"   New version: {new_version}")
    print(f"   Bump type: {bump_type}")
    print()
    
    # Confirm release
    response = input("Continue with release? (y/N): ")
    if response.lower() != 'y':
        print("Release cancelled.")
        sys.exit(0)
    
    # Run tests
    if not run_tests():
        print("❌ Tests failed. Aborting release.")
        sys.exit(1)
    
    # Update version files
    print("📝 Updating version files...")
    update_version_files(new_version)
    update_changelog(new_version)
    
    # Build executables
    if not build_executables():
        print("❌ Build failed. Aborting release.")
        sys.exit(1)
    
    # Git operations
    if not git_operations(new_version):
        print("❌ Git operations failed. Aborting release.")
        sys.exit(1)
    
    # Create GitHub release
    if not create_github_release(new_version):
        print("❌ GitHub release creation failed.")
        # Don't abort here as the local release is complete
    
    print()
    print("✅ Release completed successfully!")
    print(f"   Version {new_version} has been released")
    print(f"   Next steps:")
    print(f"   1. Push changes: git push origin main")
    print(f"   2. Push tags: git push origin v{new_version}")
    print(f"   3. Check GitHub Actions for automated builds")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
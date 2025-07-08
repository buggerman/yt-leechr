#!/bin/bash
# Generate Flatpak Python dependency manifests

set -e

echo "Generating Flatpak Python dependency manifests..."

# Check if flatpak-pip-generator is available
if ! command -v flatpak-pip-generator &> /dev/null; then
    echo "flatpak-pip-generator not found. Installing..."
    pip3 install --user flatpak-pip-generator
    export PATH="$HOME/.local/bin:$PATH"
fi

# Generate yt-dlp dependencies
echo "Generating yt-dlp dependencies..."
flatpak-pip-generator --output python3-yt-dlp yt-dlp

# Generate requests dependencies  
echo "Generating requests dependencies..."
flatpak-pip-generator --output python3-requests requests

echo "Dependency manifests generated successfully!"
echo "Files created:"
echo "  - python3-yt-dlp.json"
echo "  - python3-requests.json"
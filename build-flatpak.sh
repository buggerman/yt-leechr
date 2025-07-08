#!/bin/bash
# Build YT Leechr Flatpak package

set -e

APP_ID="io.github.buggerman.yt-leechr"
MANIFEST="${APP_ID}.json"
BUILD_DIR="build-dir"
REPO_DIR="repo"

echo "🏗️  Building YT Leechr Flatpak..."

# Check prerequisites
echo "🔍 Checking prerequisites..."

if ! command -v flatpak-builder &> /dev/null; then
    echo "❌ flatpak-builder not found. Please install it:"
    echo "   sudo apt install flatpak-builder  # Debian/Ubuntu"
    echo "   sudo dnf install flatpak-builder  # Fedora"
    exit 1
fi

if ! flatpak list --runtime | grep -q "org.kde.Platform.*6.7"; then
    echo "❌ KDE Platform 6.7 runtime not found. Installing..."
    flatpak install -y flathub org.kde.Platform//6.7 org.kde.Sdk//6.7 com.riverbankcomputing.PyQt.BaseApp//6.7
fi

# Generate dependencies if they don't exist
if [[ ! -f python3-yt-dlp.json ]] || [[ ! -f python3-requests.json ]]; then
    echo "🔧 Generating Python dependencies..."
    chmod +x generate-flatpak-deps.sh
    ./generate-flatpak-deps.sh
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf "$BUILD_DIR" "$REPO_DIR"

# Build the Flatpak
echo "🔨 Building Flatpak package..."
flatpak-builder --force-clean --repo="$REPO_DIR" "$BUILD_DIR" "$MANIFEST"

# Install locally
echo "📦 Installing Flatpak locally..."
flatpak --user remote-add --no-gpg-verify --if-not-exists yt-leechr-repo "$REPO_DIR"
flatpak --user install -y yt-leechr-repo "$APP_ID"

echo "✅ Build completed successfully!"
echo ""
echo "🚀 To run the application:"
echo "   flatpak run $APP_ID"
echo ""
echo "🗑️  To uninstall:"
echo "   flatpak --user uninstall $APP_ID"
echo ""
echo "📁 To create a .flatpak bundle:"
echo "   flatpak build-bundle $REPO_DIR yt-leechr.flatpak $APP_ID"
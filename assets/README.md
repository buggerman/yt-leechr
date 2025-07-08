# Assets Directory

This directory contains application assets such as icons and images.

## Icon Files

To add application icons:

- `icon.ico` - Windows icon (256x256 px recommended)
- `icon.icns` - macOS icon bundle
- `icon.png` - General purpose icon (256x256 px recommended)

## Creating Icons

You can create icons from a high-quality PNG image using:

### Windows (.ico)
```bash
# Using ImageMagick
magick convert icon.png -define icon:auto-resize=256,128,64,48,32,16 icon.ico
```

### macOS (.icns)
```bash
# Using iconutil (macOS only)
mkdir icon.iconset
sips -z 16 16 icon.png --out icon.iconset/icon_16x16.png
sips -z 32 32 icon.png --out icon.iconset/icon_16x16@2x.png
sips -z 32 32 icon.png --out icon.iconset/icon_32x32.png
sips -z 64 64 icon.png --out icon.iconset/icon_32x32@2x.png
sips -z 128 128 icon.png --out icon.iconset/icon_128x128.png
sips -z 256 256 icon.png --out icon.iconset/icon_128x128@2x.png
sips -z 256 256 icon.png --out icon.iconset/icon_256x256.png
sips -z 512 512 icon.png --out icon.iconset/icon_256x256@2x.png
iconutil -c icns icon.iconset
```
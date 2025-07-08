# YT Leechr Flatpak

This document covers building, installing, and distributing YT Leechr as a Flatpak package.

## Quick Installation

### From Release (Recommended)

1. Download the latest `.flatpak` bundle from [GitHub Releases](https://github.com/buggerman/yt-leechr/releases)
2. Install the bundle:
   ```bash
   flatpak install --user yt-leechr.flatpak
   ```
3. Run the application:
   ```bash
   flatpak run io.github.buggerman.yt-leechr
   ```

### From Flathub (Future)

*Note: Submission to Flathub is planned for future releases.*

```bash
flatpak install flathub io.github.buggerman.yt-leechr
```

## Building from Source

### Prerequisites

1. **Install Flatpak and flatpak-builder**:
   ```bash
   # Debian/Ubuntu
   sudo apt install flatpak flatpak-builder
   
   # Fedora
   sudo dnf install flatpak flatpak-builder
   
   # Arch Linux
   sudo pacman -S flatpak flatpak-builder
   ```

2. **Add Flathub repository**:
   ```bash
   flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
   ```

3. **Install required runtimes**:
   ```bash
   flatpak install flathub org.kde.Platform//6.7 org.kde.Sdk//6.7 com.riverbankcomputing.PyQt.BaseApp//6.7
   ```

### Build Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/buggerman/yt-leechr.git
   cd yt-leechr
   ```

2. **Build the Flatpak**:
   ```bash
   ./build-flatpak.sh
   ```

The script will:
- Generate Python dependency manifests
- Build the Flatpak package
- Install it locally for testing
- Provide instructions for running and uninstalling

### Manual Build

If you prefer manual control:

1. **Generate dependencies**:
   ```bash
   ./generate-flatpak-deps.sh
   ```

2. **Build manually**:
   ```bash
   flatpak-builder --force-clean --repo=repo build-dir io.github.buggerman.yt-leechr.json
   flatpak --user remote-add --no-gpg-verify --if-not-exists yt-leechr-repo repo
   flatpak --user install yt-leechr-repo io.github.buggerman.yt-leechr
   ```

3. **Create bundle**:
   ```bash
   flatpak build-bundle repo yt-leechr.flatpak io.github.buggerman.yt-leechr
   ```

## Usage

### Running the Application

```bash
# Via flatpak command
flatpak run io.github.buggerman.yt-leechr

# Via desktop launcher (after installation)
# Look for "YT Leechr" in your application menu
```

### Permissions

YT Leechr requests these permissions for proper functionality:

- **Network access**: Download videos from online sources
- **XDG directories**: Access to Downloads, Videos, and Music folders
- **Display/Audio**: GUI display and audio playback
- **File manager integration**: Open download folders
- **Notifications**: Download completion alerts

### File Access

Downloads are saved to these sandboxed locations:
- `~/Downloads/` - Default download location
- `~/Videos/` - Alternative for video files
- `~/Music/` - For audio-only downloads

## Troubleshooting

### Common Issues

1. **"App not found" error**:
   ```bash
   # Refresh Flatpak
   flatpak update
   flatpak --user list | grep yt-leechr
   ```

2. **Permission denied downloading**:
   ```bash
   # Check folder permissions
   ls -la ~/Downloads ~/Videos ~/Music
   ```

3. **Network connection issues**:
   ```bash
   # Test network access
   flatpak run --devel io.github.buggerman.yt-leechr
   ```

4. **GUI not starting**:
   ```bash
   # Run with debug output
   flatpak run --verbose io.github.buggerman.yt-leechr
   ```

### Logs and Debugging

View application logs:
```bash
journalctl --user -f | grep yt-leechr
```

Debug the Flatpak sandbox:
```bash
flatpak run --devel --command=bash io.github.buggerman.yt-leechr
```

## Development

### Testing Changes

1. Make changes to the source code
2. Update the Git tag in the manifest if needed
3. Rebuild: `./build-flatpak.sh`
4. Test: `flatpak run io.github.buggerman.yt-leechr`

### Updating Dependencies

When adding new Python packages:

1. Update `requirements.txt`
2. Regenerate dependencies: `./generate-flatpak-deps.sh`
3. Add new dependency JSON to the manifest's modules section

### Manifest Structure

The `io.github.buggerman.yt-leechr.json` manifest contains:

- **Runtime**: KDE Platform 6.7 (provides Qt6 and system libraries)
- **Base**: PyQt BaseApp 6.7 (provides PyQt6 and Python)
- **Modules**: Python dependencies (yt-dlp, requests) + application source
- **Permissions**: Minimal required permissions for functionality
- **Desktop Integration**: `.desktop` file, icons, and AppStream metadata

### CI/CD Integration

GitHub Actions automatically:
- Builds Flatpak on new tags
- Generates dependency manifests
- Uploads `.flatpak` bundles to releases
- Validates the manifest

## Distribution

### Release Process

1. Tag a new release: `git tag v0.x.x && git push origin v0.x.x`
2. GitHub Actions builds the Flatpak automatically
3. Download `.flatpak` bundle from release artifacts
4. Test the bundle before publishing

### Flathub Submission

For Flathub distribution:

1. Fork the [Flathub repository](https://github.com/flathub/flathub)
2. Add the manifest to `io.github.buggerman.yt-leechr` directory
3. Submit pull request following [Flathub guidelines](https://docs.flathub.org/)

### Bundle Distribution

Share the `.flatpak` bundle file for offline installation:
```bash
flatpak install --user yt-leechr.flatpak
```

## Security

### Sandbox Restrictions

YT Leechr runs in a secure sandbox with:
- No access to system files outside XDG directories
- No access to other applications' data
- Network access limited to HTTPS/HTTP downloads
- No access to sensitive system APIs

### Permissions Rationale

- **Network**: Required for downloading videos
- **XDG Downloads/Videos/Music**: User's expected download locations
- **File Manager**: Open download folders for user convenience
- **Notifications**: Inform user of download completion

## Support

- **Issues**: [GitHub Issues](https://github.com/buggerman/yt-leechr/issues)
- **Documentation**: [README](https://github.com/buggerman/yt-leechr#readme)
- **Flatpak Guide**: This document

---

*For more information about Flatpak, visit [flatpak.org](https://flatpak.org)*
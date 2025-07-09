# YT Leechr Release Guide

This guide explains how to create and publish a new release of YT Leechr when there are new changes merged to the main branch.

## 📋 Prerequisites

- Push access to the repository
- GitHub CLI (`gh`) installed and authenticated
- Git configured with your credentials

## 🚀 Release Process

### 1. Ensure Main Branch is Up-to-Date

```bash
git checkout main
git pull origin main
```

### 2. Create and Push New Release Tag

Replace `vX.X.X` with your desired version number (e.g., `v1.0.2`, `v1.1.0`):

```bash
# Create tag locally
git tag vX.X.X

# Push tag to GitHub (this triggers the build workflows)
git push origin vX.X.X
```

### 3. Monitor Build Progress

After pushing the tag, two workflows will automatically start:

```bash
# Check build status
gh run list --limit 5

# Watch specific build run
gh run watch <run-id>
```

**Expected workflows:**
- `Build Executables` - Builds all platform binaries
- `Build Flatpak` - Builds the universal Linux package

### 4. Wait for Builds to Complete

Builds typically take 5-10 minutes. Monitor until both workflows show "completed success":

```bash
# Check status until both complete
gh run list --limit 2
```

### 5. Review Draft Release

Once builds complete, a draft release is automatically created:

```bash
# View the draft release
gh release view vX.X.X
```

**Expected artifacts:**
- `YT-Leechr-linux-x64` + `YT-Leechr-linux-x64-portable.tar.gz`
- `YT-Leechr-linux-aarch64` + `YT-Leechr-linux-aarch64-portable.tar.gz`
- `YT-Leechr-windows-x64.exe` + `YT-Leechr-windows-x64-portable.zip`
- `YT-Leechr-darwin-arm64-portable.tar.gz` (macOS Apple Silicon)
- `yt-leechr.flatpak` (Universal Linux)

### 6. Customize Release Notes (Optional)

If you want to customize the release notes:

```bash
# Edit release notes interactively
gh release edit vX.X.X --notes-file -

# Or edit with a prepared file
gh release edit vX.X.X --notes-file release-notes.md
```

### 7. Publish the Release

Remove the draft status to make it public:

```bash
# Publish the release
gh release edit vX.X.X --draft=false
```

## 📝 Release Notes Template

Create a file called `release-notes.md` if you want custom release notes:

```markdown
# YT Leechr vX.X.X - Release Title

Brief description of what's new or changed.

## 🆕 What's New

- Feature 1
- Feature 2
- Bug fix 1

## 📦 Available Downloads

### Windows
- **x64**: `YT-Leechr-windows-x64.exe` + portable ZIP

### Linux  
- **x64**: `YT-Leechr-linux-x64` + portable tar.gz
- **aarch64**: `YT-Leechr-linux-aarch64` + portable tar.gz

### macOS
- **Apple Silicon only**: `YT-Leechr-darwin-arm64-portable.tar.gz`
- **⚠️ Intel Mac users**: Not supported - builds are ARM64 only

### Universal Linux
- **Flatpak**: Works on x86_64 Linux distributions with Flatpak support
- **⚠️ ARM64 Linux users**: Use native `linux-aarch64` builds instead

## ⚠️ Platform Status

### Current Limitations
- **Flatpak**: Quality selection may default to 360p instead of best quality (x86_64 only)
- **Windows**: Video/audio files may download separately instead of merged MKV
- **Intel Macs**: **NOT SUPPORTED** - ARM64 builds only work on Apple Silicon

### Working Perfectly
- ✅ **Apple Silicon macOS**: Full functionality with automatic MKV merging
- ✅ **Linux Standalone**: Complete feature support (both x64 and aarch64)

---

**Full Changelog**: [vX.X.X-1...vX.X.X](https://github.com/buggerman/yt-leechr/compare/vX.X.X-1...vX.X.X)
```

## 🔧 Troubleshooting

### Builds Fail

If builds fail:

```bash
# Check build logs
gh run view <run-id> --log

# For specific job
gh run view --job=<job-id>
```

Common issues:
- **Tests fail**: Check if code changes broke existing functionality
- **Build errors**: Usually dependency or compilation issues
- **Release upload fails**: Check if artifacts were generated correctly

### Missing Artifacts

If some artifacts are missing from the release:

```bash
# Check what artifacts were uploaded
gh run view <run-id>

# Look for artifact upload issues in logs
gh run view <run-id> --log | grep -i "upload"
```

### Wrong Architecture Names

If architecture names are incorrect (e.g., `x64` instead of `arm64` for macOS):

1. Check the build matrix in `.github/workflows/build.yml`
2. Verify the architecture detection in `build.py`
3. Delete the tag and recreate after fixing

```bash
# Delete tag and recreate
git tag -d vX.X.X
git push origin :refs/tags/vX.X.X

# Fix the issue, then recreate
git tag vX.X.X
git push origin vX.X.X
```

## 🎯 Quick Reference

```bash
# Complete release process (one-liner)
git checkout main && git pull origin main && git tag vX.X.X && git push origin vX.X.X

# Then wait for builds and publish
gh run watch && gh release edit vX.X.X --draft=false
```

## 📊 Platform Support Matrix

| Platform | Architecture | Status | Filename Pattern |
|----------|-------------|--------|------------------|
| Linux | x64 | ✅ Full Support | `YT-Leechr-linux-x64` |
| Linux | aarch64 | ✅ Full Support | `YT-Leechr-linux-aarch64` |
| Windows | x64 | ⚠️ Minor Issues | `YT-Leechr-windows-x64.exe` |
| macOS | ARM64 | ✅ Full Support | `YT-Leechr-darwin-arm64-portable.tar.gz` |
| macOS | Intel x64 | ❌ Not Supported | N/A |
| Universal Linux | x86_64 | ⚠️ Minor Issues | `yt-leechr.flatpak` |

## 🔄 Automation Details

The release process is automated through GitHub Actions:

1. **Tag Push** triggers both `Build Executables` and `Build Flatpak` workflows
2. **Build Executables** creates platform-specific binaries and portable packages
3. **Build Flatpak** creates universal Linux distribution package
4. **Release Job** automatically creates draft release with all artifacts
5. **Manual Step** is required to publish the release (remove draft status)

This ensures consistent releases with all expected artifacts and proper architecture labeling.
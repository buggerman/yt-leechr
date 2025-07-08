#!/bin/bash
# Flatpak launcher script for YT Leechr

# Set up environment
export QT_QPA_PLATFORM_PLUGIN_PATH=/app/lib/plugins/platforms
export QT_PLUGIN_PATH=/app/lib/plugins

# Set Python path to include the application
export PYTHONPATH="/app/share/yt-leechr:$PYTHONPATH"

# Ensure ffmpeg extension is available
export PATH="/app/lib/ffmpeg:$PATH"
export LD_LIBRARY_PATH="/app/lib/ffmpeg:$LD_LIBRARY_PATH"

# Change to home directory for proper file dialogs
cd "$HOME"

# Launch the application - run main.py directly
exec python3 /app/share/yt-leechr/main.py "$@"
#!/bin/bash
# Flatpak launcher script for YT Leechr

# Set up environment
export QT_QPA_PLATFORM_PLUGIN_PATH=/app/lib/plugins/platforms
export QT_PLUGIN_PATH=/app/lib/plugins

# Change to home directory for proper file dialogs
cd "$HOME"

# Launch the application
exec python3 -m main "$@"
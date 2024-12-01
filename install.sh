# install.sh
#!/bin/bash

# Exit on error
set -e

echo "Setting up Audio Recorder..."

# Get project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create symbolic links
echo "Creating symbolic links..."
sudo ln -sf "${PROJECT_DIR}/bin/audio-recorder-toggle" /usr/local/bin/audio-recorder-toggle
mkdir -p ~/.config/systemd/user
ln -sf "${PROJECT_DIR}/config/audio-recorder.service" ~/.config/systemd/user/audio-recorder.service
mkdir -p ~/.local/share/applications
ln -sf "${PROJECT_DIR}/config/audio-recorder.desktop" ~/.local/share/applications/audio-recorder.desktop

# Reload systemd and start service
echo "Starting service..."
systemctl --user daemon-reload
systemctl --user enable audio-recorder
systemctl --user restart audio-recorder

echo "Setup complete!"
echo "Use Ctrl+Alt+R to toggle recording"
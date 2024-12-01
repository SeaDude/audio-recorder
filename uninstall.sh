#!/bin/bash

echo "Removing Audio Recorder system integration..."

# Stop and disable service
systemctl --user stop audio-recorder 2>/dev/null || true
systemctl --user disable audio-recorder 2>/dev/null || true

# Remove symbolic links
sudo rm -f /usr/local/bin/audio-recorder-toggle
rm -f ~/.config/systemd/user/audio-recorder.service
rm -f ~/.local/share/applications/audio-recorder.desktop

# Reload systemd
systemctl --user daemon-reload

echo "Removal complete!"
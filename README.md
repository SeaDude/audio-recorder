# System Audio Recorder

A lightweight system audio recorder for Ubuntu Linux that captures system audio (not microphone) with a simple keyboard shortcut (Ctrl+Alt+R).

## Features

- Record system audio with a keyboard shortcut (Ctrl+Alt+R)
- Desktop notifications for recording status
- Optimized for speech recording (using Opus codec)
- Small file sizes without compromising speech quality

## Prerequisites

- Ubuntu Linux (tested on 22.04 LTS)
- Python 3.8+
- FFmpeg
- PulseAudio
- Required packages:
  ```bash
  sudo apt-get install ffmpeg python3-notify2 netcat-openbsd
  ```

## Quick Start

1. Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/audio-recorder.git
cd audio-recorder
```

2. Run the installer:

```bash
chmod +x install.sh
./install.sh
```

3. Use Ctrl+Alt+R to start/stop recording
4. Recordings are saved in `~/projects/audio-recorder/recordings`

## Project Structure
This project intentionally deviates from the Filesystem Hierarchy Standard (FHS) to maintain a more maintainable and portable structure:
```bash
/projects/audio-recorder/
├── bin/                    # Executable scripts
│   └── audio-recorder-toggle
├── src/                    # Python source files
│   ├── recorder.py         # Core recording functionality
│   └── recorder_service.py # System service implementation
├── config/                 # Configuration files
│   └── audio-recorder.service
├── logs/                   # Log files
│   ├── debug.log
│   └── service.log
├── recordings/            # Recorded audio files
└── install.sh            # Installation script
```

## System Integration
Instead of spreading files across the system, this project:

- Keeps all files in one project directory
- Uses symbolic links to integrate with the system:
    ```bash
    /usr/local/bin/audio-recorder-toggle → bin/audio-recorder-toggle
    ~/.config/systemd/user/audio-recorder.service → config/audio-recorder.service
    ```

## Technical Details

- Uses FFmpeg with PulseAudio for recording
- Implements a systemd user service for background operation
- Uses Unix domain sockets for inter-process communication
- Optimized for speech recording using the Opus codec
- Default recording settings:

    - Codec: Opus
    - Bitrate: 32k
    - Channels: Mono
    - Sample Rate: 16kHz
    - Filters: Speech-optimized bandpass

## Uninstallation

```bash
chmod +x uninstall.sh
./uninstall.sh
```
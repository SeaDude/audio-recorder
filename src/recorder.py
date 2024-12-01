import subprocess
import os
import time
import signal
import sys
from datetime import datetime
import logging

# Get project directory (relative to this file)
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Set up logging
os.makedirs(os.path.join(PROJECT_DIR, 'logs'), exist_ok=True)
logging.basicConfig(
    filename=os.path.join(PROJECT_DIR, 'logs/debug.log'),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class AudioRecorder:
    def __init__(self, quality_preset='speech'):
        self.process = None
        self.filename = None
        self.is_recording = False
        self.quality_preset = quality_preset
        self.recordings_dir = os.path.join(PROJECT_DIR, 'recordings')
        
        # Create recordings directory if it doesn't exist
        os.makedirs(self.recordings_dir, exist_ok=True)
        
        self.presets = {
            'speech': {
                'codec': 'libopus',
                'bitrate': '32k',
                'channels': '1',
                'sample_rate': '16000',
                'filters': 'highpass=f=200,lowpass=f=3000',
                'extension': 'opus',
                'extra_args': ['-application', 'voip']
            }
        }

    def get_default_sink_monitor(self):
        try:
            sink = subprocess.check_output(
                "pactl get-default-sink",
                shell=True
            ).decode().strip()
            monitor = f"{sink}.monitor"
            return monitor
        except Exception as e:
            logging.error(f"Error getting default sink monitor: {str(e)}")
            return None

    def start_recording(self):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            preset = self.presets[self.quality_preset]
            self.filename = os.path.join(
                self.recordings_dir, 
                f"system_audio_{timestamp}.{preset['extension']}"
            )
            
            logging.info(f"Will save recording to: {self.filename}")
            
            monitor_source = self.get_default_sink_monitor()
            if not monitor_source:
                logging.error("Could not find audio monitor source")
                return False

            command = [
                'ffmpeg',
                '-f', 'pulse',
                '-i', monitor_source,
                '-c:a', preset['codec'],
                '-b:a', preset['bitrate'],
                '-ac', preset['channels'],
                '-ar', preset['sample_rate']
            ]
            
            if preset['filters']:
                command.extend(['-af', preset['filters']])
            
            if 'extra_args' in preset:
                command.extend(preset['extra_args'])
            
            command.extend(['-y', self.filename])
            
            logging.info(f"Executing command: {' '.join(command)}")

            self.process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            time.sleep(1)
            if self.process.poll() is not None:
                error_output = self.process.stderr.read().decode()
                logging.error(f"FFmpeg process failed to start: {error_output}")
                return False
            
            self.is_recording = True
            logging.info("Recording started successfully")
            return True

        except Exception as e:
            logging.error(f"Error starting recording: {str(e)}")
            return False

    def stop_recording(self):
        if self.process and self.is_recording:
            try:
                logging.info("Stopping recording...")
                self.process.terminate()
                self.process.wait(timeout=5)
                self.is_recording = False
                
                if os.path.exists(self.filename):
                    file_size = os.path.getsize(self.filename)
                    logging.info(f"Recording saved: {self.filename} (size: {file_size} bytes)")
                else:
                    logging.error(f"Recording file not found: {self.filename}")
                    
            except Exception as e:
                logging.error(f"Error stopping recording: {str(e)}")
                try:
                    self.process.kill()
                except:
                    pass

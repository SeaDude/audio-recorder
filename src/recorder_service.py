import os
import sys
import socket
import notify2
from recorder import AudioRecorder
import logging

# Get project directory
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Set up logging
os.makedirs(os.path.join(PROJECT_DIR, 'logs'), exist_ok=True)
logging.basicConfig(
    filename=os.path.join(PROJECT_DIR, 'logs/service.log'),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

SOCKET_PATH = "/tmp/audio_recorder.sock"

class RecorderService:
    def __init__(self):
        self.recorder = AudioRecorder(quality_preset='speech')
        self.server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        notify2.init("Audio Recorder")
        logging.info("Recorder service initialized")
        
    def notify(self, message):
        try:
            notification = notify2.Notification("Audio Recorder", message)
            notification.show()
            logging.info(f"Notification sent: {message}")
        except Exception as e:
            logging.error(f"Failed to send notification: {e}")
        
    def start_service(self):
        if os.path.exists(SOCKET_PATH):
            os.remove(SOCKET_PATH)
            
        try:
            self.server.bind(SOCKET_PATH)
            self.server.listen(1)
            logging.info(f"Service started, listening on {SOCKET_PATH}")
            
            while True:
                logging.debug("Waiting for connection...")
                conn, addr = self.server.accept()
                command = conn.recv(1024).decode().strip()
                logging.info(f"Received command: {command}")
                
                if command == "TOGGLE":
                    if self.recorder.is_recording:
                        logging.info("Stopping recording")
                        self.recorder.stop_recording()
                        self.notify("Recording stopped")
                        conn.send(b"Recording stopped")
                    else:
                        logging.info("Starting recording")
                        if self.recorder.start_recording():
                            self.notify("Recording started")
                            conn.send(b"Recording started")
                        else:
                            self.notify("Failed to start recording")
                            conn.send(b"Failed to start recording")
                            
                conn.close()
        except Exception as e:
            logging.error(f"Service error: {e}")
            self.notify(f"Service error: {e}")

if __name__ == "__main__":
    service = RecorderService()
    service.start_service()

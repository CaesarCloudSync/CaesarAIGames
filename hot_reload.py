from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import time
import os

class RestartOnChangeHandler(FileSystemEventHandler):
    def __init__(self, command):
        self.command = command
        self.process = None
        self.start_process()

    def start_process(self):
        print("🔁 Starting PyQt5 app...")
        self.process = subprocess.Popen(self.command)

    def kill_process(self):
        if self.process:
            print("🛑 Stopping PyQt5 app...")
            self.process.kill()
            self.process.wait()

    def on_any_event(self, event):
        if event.src_path.endswith(".py"):
            self.kill_process()
            self.start_process()

    def stop(self):
        self.kill_process()

if __name__ == "__main__":
    path = "."  # Watch current directory
    command = ["venv/Scripts/python.exe", "main.py"]  # Replace with your script name
    event_handler = RestartOnChangeHandler(command)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        event_handler.stop()
        observer.stop()
    observer.join()

import os
import time
import psutil
from models import PID
class TaskManager:
    def __init__(self):
        pass
    def run_game(self,exe_path):
        # Check if running as admin (UAC check)
        os.startfile(exe_path)
        #self.find_process_by_filename(os.path.basename(exe_path))

    def list_processes():
        # Iterate over all processes
        for process in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
            try:
                # Process info: PID, Name, User, CPU Usage, Memory Usage
                print(f"PID: {process.info['pid']}, "
                    f"Name: {process.info['name']}, "
                    f"User: {process.info['username']}, "
                    f"CPU: {process.info['cpu_percent']}%, "
                    f"Memory: {process.info['memory_percent']}%")
                
                #{'username': 'AMARI\\amari', 'cpu_percent': 0.0, 'pid': 25692, 'memory_percent': 0.5098751875168762, 'exe': 'D:\\Games\\Vampyr\\AVGame\\Binaries\\Win64\\AVGame-Win64-Shipping.exe', 'name': 'AVGame-Win64-Shipping.exe'}
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # Handle processes that end or don't have permission
                pass
    def kill_process(self, pid):
        try:
            process = psutil.Process(pid)
            process.terminate()  # Attempt to terminate the process
            process.wait(timeout=3)  # Wait for the process to terminate
            print(f"Process {pid} terminated successfully.")
        except psutil.NoSuchProcess:
            print(f"Process {pid} does not exist.")
        except psutil.AccessDenied:
            print(f"Access denied to terminate process {pid}.")
        except psutil.TimeoutExpired:
            print(f"Process {pid} did not terminate in time.")
    def check_process_running(self, pid):
        try:
            process = psutil.Process(pid)
            return process.is_running()
        except psutil.NoSuchProcess:
            return False
        except psutil.AccessDenied:
            print(f"Access denied to check process {pid}.")
            return False
    def find_process_by_filename(self,filename):
        # Iterate over all running processes
        for process in psutil.process_iter(['pid', 'name', 'exe', 'username', 'cpu_percent', 'memory_percent']):
            try:\
                # Check if the executable name matches the given filename
                if filename.lower() in process.info['name'].lower():  # Compare in a case-insensitive manner
                    return PID.model_validate(process.info)

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # Handle processes that end or don't have permission
                pass
    def find_process_by_pid(self, pid):
        try:
            process = psutil.Process(pid)
            return PID.model_validate(process.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return None
    # Function to monitor the process
    def monitor_process(self,pid):
        try:
            # Create a process object using the PID
            process = psutil.Process(pid)

            # Continuously check if the process is still running
            while True:
                # Check if the process is still running
                if not process.is_running():
                    print(f"Process {pid} has terminated.")
                    # Call a random function when the process stops
                    print("Backing up data...")
                    print("Data backup complete.")
                    break  # Exit the loop after triggering the event
                else:
                    print(f"Process {pid} is still running.")
                
                time.sleep(1)  # Wait for 1 second before checking again
        except psutil.NoSuchProcess:
            print(f"No process with PID {pid} found.")
        except psutil.AccessDenied:
            print(f"Access denied to process {pid}. You might need higher privileges.")

if __name__ == "__main__":
    tm = TaskManager()
    exe_path = r"E:\steamunlockedgames\Baldur-Gate-three-SteamRIP.com\Baldurs Gate 3\bin\bg3.exe" #"D:\\Games\\Vampyr\\AVGame\\Binaries\\Win64\\AVGame-Win64-Shipping.exe"

    tm.run_game(exe_path)
    processinfo: PID = tm.find_process_by_filename(os.path.basename(exe_path))
    tm.monitor_process(processinfo.pid)

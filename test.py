import time
import requests

# File not found error - {'error': "<class 'TypeError'>,Object of type FileNotFoundError is not JSON serializable"}
time.sleep(3)
response2 = requests.get("http://127.0.0.1:8082/get_all_tasks")
print(response2.json())


#/media/amari/SSD T7
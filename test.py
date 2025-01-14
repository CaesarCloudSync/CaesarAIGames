import time
import requests
url = "https://download161.uploadhaven.com/1/application/zip/15motqeYKVmHrpmxBwhoaTzJid9vmP6WbEioUwBn.zip?key=I7SoiWn6uxwKmmH4LvBSGg&expire=1736947939&filename=Shadow.Tactics.Blades.of.the.Shogun.v2.2.10.f.zip"
#response = requests.post("http://127.0.0.1:8082/api/v1/downloadgame",json={"url":url})

#print(response.json())
#time.sleep(3)
#response2 = requests.get("http://127.0.0.1:8082/tasks",params={"task_id":response.json()["task_id"],"filename":response.json()["filename"]})
#print(response2.json())
# File not found error - {'error': "<class 'TypeError'>,Object of type FileNotFoundError is not JSON serializable"}
time.sleep(3)
response2 = requests.get("http://127.0.0.1:8082/get_all_tasks")
print(response2.json())

time.sleep(3)
#response2 = requests.get("http://127.0.0.1:8082/cancel_task",params={"filename":"Shadow.Tactics.Blades.of.the.Shogun.v2.2.10.f.zip"})
#print(response2.json())


#/media/amari/SSD T7
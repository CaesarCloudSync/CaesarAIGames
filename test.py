import time
import requests
url = "https://download161.uploadhaven.com/1/application/zip/15motqeYKVmHrpmxBwhoaTzJid9vmP6WbEioUwBn.zip?key=GVSVJZlYfVAPbmetSc_eqg&expire=1736807935&filename=Shadow.Tactics.Blades.of.the.Shogun.v2.2.10.f.zip"
response = requests.get("http://127.0.0.1:8082/api/v1/downloadgame",params={"url":url})

print(response.json())
time.sleep(3)
response2 = requests.get("http://127.0.0.1:8082/get_all_tasks")
print(response2.json())
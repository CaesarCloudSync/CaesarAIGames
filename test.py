import requests
url = "https://download191.uploadhaven.com/1/application/zip/PwqHm6HPNS7o78bdbqtyTRqYXL9h8eBNHO1aXfVc.zip?key=F6EqOfzkS_2mVEQ5akRB2g&expire=1719016771&filename=Shadow.Tactics.Aikos.Choice.v3.2.25.F.zip"
#response = requests.get('http://127.0.0.1:8080/api/v1/downloadgame',params={"url":url})
#print(response.json()["task_id"])
responsestatus = requests.get(f"http://127.0.0.1:8080/tasks",params={"task_id":"0d2b066c-37f9-4406-b98c-9d225b5db59e","url":url})
print(responsestatus.json())


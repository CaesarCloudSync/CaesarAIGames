import requests
import json
import time
class AmariGames:
    def __init__(self,server_uri,game_url) -> None:
        self.server_uri = server_uri
        self.current_task_id = ""
    def create_download_task(self):
        response = requests.post(f'{uri}:8080/api/v1/downloadgame',json={"url":url})
        task_id = response.json()["task_id"]
        print(task_id)
        with open("task_id.json","w+") as f:
            json.dump({"task_id":task_id},f)
    def get_task_progress(self):
        with open("task_id.json") as f:
            task_json = json.load(f)
        print(task_json)
        responsestatus = requests.post(f"{uri}:8080/tasks",json={"task_id":task_json["task_id"],"filename":"Lies.of.P"})
        print(responsestatus.json())
    def cancel_task(self):
        with open("task_id.json") as f:
            task_json = json.load(f)
        responsestatus = requests.get(f"{uri}:8080/cancel_task",params={"task_id":task_json["task_id"]})
        print(responsestatus.json())

if __name__ == "__main__":
    uri = "http://localhost"
    url ="https://download167.uploadhaven.com/1/application/zip/E0JERlmVtKgW7hWIs4ktacrDGNHacMKfjVmMrQYu.zip?key=Yujw_v9QTVEii4gPsT3eIQ&expire=1721077463&filename=Lies.of.P.zip"
    amg = AmariGames(uri,url)
    amg.create_download_task()
    #amg.get_task_progress()
    #time.sleep(40)
    #amg.cancel_task()

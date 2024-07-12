import requests
import json
import time
class AmariGames:
    def __init__(self,server_uri,game_url) -> None:
        self.server_uri = server_uri
        self.current_task_id = ""
    def create_download_task(self):
        response = requests.get(f'{uri}:8080/api/v1/downloadgame',params={"url":url})
        task_id = response.json()["task_id"]
        print(task_id)
        with open("task_id.json","w+") as f:
            json.dump({"task_id":task_id},f)
    def get_task_progress(self):
        with open("task_id.json") as f:
            task_json = json.load(f)
        print(task_json)
        responsestatus = requests.get(f"{uri}:8080/tasks",params={"task_id":task_json["task_id"],"url":url})
        print(responsestatus.json())
    def cancel_task(self):
        with open("task_id.json") as f:
            task_json = json.load(f)
        responsestatus = requests.get(f"{uri}:8080/cancel_task",params={"task_id":task_json["task_id"]})
        print(responsestatus.json())

if __name__ == "__main__":
    uri = "http://localhost"
    url ="https://download192.uploadhaven.com/1/application/zip/h9lvRwo7BjGgxutkfDMGTNBs1zj5diyAXKho8I2S.zip?key=fCcoN4Gp0CxETfgpM68QFg&expire=1721078861&filename=Dishonored2ALLDLCs.zip"
    amg = AmariGames(uri,url)
    amg.create_download_task()
    amg.get_task_progress()
    time.sleep(40)
    amg.cancel_task()

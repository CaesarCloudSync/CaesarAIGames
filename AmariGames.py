import requests
import json
class AmariGames:
    def __init__(self,server_uri,game_url) -> None:
        self.server_uri = server_uri
        self.current_task_id = ""
    def create_download_task(self):
        response = requests.get(f'{uri}:8080/api/v1/downloadgame',params={"url":url})
        task_id = response.json()["task_id"]
        with open("task_id.json","w+") as f:
            json.dump({"task_id":task_id},f)
    def get_task_progress(self):
        with open("task_id.json") as f:
            task_json = json.load(f)
        print(task_json)
        responsestatus = requests.get(f"{uri}:8080/tasks",params={"task_id":task_json["task_id"],"url":url})
        print(responsestatus.json())
if __name__ == "__main__":
    uri = "http://192.168.0.10"
    url = "https://download193.uploadhaven.com/1/application/zip/TRJWz7uRtqF7BCq57qXLQKQ8VPASg5dneCSnapIb.zip?key=7Bb9TSvdszCTsnV56vGUfw&expire=1719144349&filename=Kingdom.Come.Deliverance.v1.9.6.Incl.ALL.DLC.zip"
    amg = AmariGames(uri,url)
    #amg.create_download_task()
import uvicorn

from fastapi import FastAPI, Header,Request,File, UploadFile,status,Form
from fastapi.responses import StreamingResponse,FileResponse,Response
from typing import Dict,List,Any,Union
from fastapi.responses import StreamingResponse,JSONResponse
from fastapi import WebSocket,WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from worker import create_task
from celery.result import AsyncResult
import redis
from GamesModel.GamesModel import GameModel,ProgressModel
from CaesarAIEmail.CaesarAIEmail import CaesarAIEmail
from CaesarAIGames.CaesarAIGames import CaesarAIGamesTools
from urllib.parse import unquote
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

r = redis.Redis(host="redis")
@app.get('/')# GET # allow all origins all methods.
async def index():
    return "Welcome to CaesarAIGames Template. Hello"
@app.get('/api/v1/steamunlockeddownloadgame')# GET # allow all origins all methods.
async def steamunlockeddownloadgame(url:str):
    try:
        url = unquote(url)
        #if "uploadhaven" in url:
        filename = CaesarAIGamesTools.extract_filename_steamunlocked(url)
        
        print(filename,"Lesy")
        task = create_task.delay(url,filename)
        r.hset(f"current-download-task-id:",filename,task.id)
        r.hset(f"current-download-url:",filename,url)
        return JSONResponse({"task_id": task.id,"filename":filename})
    except Exception as ex:
        CaesarAIEmail.send(**{"email":"amari.lawal@gmail.com","subject":f"CaesarAI Games Download {filename} Raspberry Pi Error - {filename}","message":f"{filename} Error: {type(ex)},{ex}"})
        return {"error":f"{type(ex)},{ex}"}

@app.get("/tasks")
def get_status(task_id:str,filename:str):
    try:

        task_result = AsyncResult(task_id)
        print(filename,"lester")
        progress = r.hget(f"current-download:",filename)
    
        progress = progress.decode("utf-8") if progress else "0"
        print(progress,"progress")
        result = {
            "task_id": task_id,
            "task_status": task_result.status,
            "task_result": task_result.result,
            "progress":progress
        }
        return JSONResponse(result)
    except Exception as ex:
        CaesarAIEmail.send(**{"email":"amari.lawal@gmail.com","subject":f"CaesarAI Games Tasks Progress {filename} Raspberry Pi Error - {progress}%","message":f"{filename} Error: {type(ex)},{ex} - Progress: {progress}%"})
        return {"error":f"{type(ex)},{ex}"}
@app.get("/get_all_tasks")
async def get_all_tasks():
    data = r.hgetall("current-download:")
    print(data)
    current_downloads = []
    for key,value in data.items():
        filename = key.decode("utf-8")
        task_id = r.hget(f"current-download-task-id:",filename)
        paused = "paused" if not task_id else "unpaused"
        current_downloads.append({filename:value,"paused":paused})

    return {"downloads":current_downloads}

@app.get("/pause_download")
async def pause_download(filename:str):
    try:
        task_id = r.hget(f"current-download-task-id:",filename)
        if task_id:
            task_id = task_id.decode("utf-8")
            task_result = AsyncResult(task_id)
            task_result.revoke(terminate=True)
        r.hdel(f"current-download-task-id:",filename)
        return {"message":f"{task_id} was paused."}
    except Exception as ex:
        CaesarAIEmail.send(**{"email":"amari.lawal@gmail.com","subject":f"CaesarAI Games Cancel {task_id} Raspberry Pi Error ","message":f" Error: {type(ex)},{ex}, Task ID: {task_id}"})
        return {"error":f"{type(ex)},{ex}"}
@app.get("/continue_download")
async def continue_download(filename:str):
    try:
        url = r.hget(f"current-download-url:",filename)
        if url:
            filename = CaesarAIGamesTools.extract_filename_steamunlocked(url.decode("utf-8"))
            
            print(filename,"Lesy")
            task = create_task.delay(url,filename)
            r.hset(f"current-download-task-id:",filename,task.id)
            return JSONResponse({"task_id": task.id,"filename":filename})
        else:
            return {"message":"download does not exist cancel your download."}
    except Exception as ex:
        CaesarAIEmail.send(**{"email":"amari.lawal@gmail.com","subject":f"CaesarAI Games Cancel {task_id} Raspberry Pi Error ","message":f" Error: {type(ex)},{ex}, Task ID: {task_id}"})
        return {"error":f"{type(ex)},{ex}"}

@app.get("/cancel_download")
async def cancel_download(filename:str):
    try:
        task_id = r.hget(f"current-download-task-id:",filename)
        if task_id:
            task_result = AsyncResult(task_id.decode("utf-8"))
            task_result.revoke(terminate=True)
        r.hdel(f"current-download-task-id:",filename)
        r.hdel(f"current-download:",filename)
        r.hdel(f"current-download-url:",filename)
        #print("final", r.hgetall("current-download:"))
        return {"message":f"{task_id} was cancelled."}
    except Exception as ex:
        CaesarAIEmail.send(**{"email":"amari.lawal@gmail.com","subject":f"CaesarAI Games Cancel {task_id} Raspberry Pi Error ","message":f" Error: {type(ex)},{ex}, Task ID: {task_id}"})
        return {"error":f"{type(ex)},{ex}"}

if __name__ == "__main__":
    uvicorn.run("main:app",port=8082,log_level="info")

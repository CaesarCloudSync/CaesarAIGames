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
@app.post('/api/v1/downloadgame')# GET # allow all origins all methods.
async def downloadgame(gamesmodel: GameModel):
    try:
        gamesmodel = gamesmodel.model_dump()
        url = gamesmodel["url"]
        #if "uploadhaven" in url:
        filename = CaesarAIGamesTools.extract_filename_steamunlocked(url)
        
        print(filename,"Lesy")
        task = create_task.delay(url,filename)
        return JSONResponse({"task_id": task.id,"filename":filename})
    except Exception as ex:
        CaesarAIEmail.send(**{"email":"amari.lawal@gmail.com","subject":f"CaesarAI Games Download {filename} Raspberry Pi Error - {filename}","message":f"{filename} Error: {type(ex)},{ex}"})
        return {"error":f"{type(ex)},{ex}"}

@app.post("/tasks")
def get_status(progressmodel:ProgressModel):
    try:
        progressmodel = progressmodel.model_dump()
        task_id = progressmodel["task_id"]
        filename = progressmodel["filename"]

        task_result = AsyncResult(task_id)

        filename = f"/media/amari/SSD T7/steamunlockedgames/{filename}"
        print(filename,"lester")
        progress = r.get(f"{filename}-progress")
    
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
@app.get("/cancel_task")
async def cancel_task(task_id:str):
    try:
        task_result = AsyncResult(task_id)
        task_result.revoke(terminate=True)
        return {"message":f"{task_id} was cancelled."}
    except Exception as ex:
        CaesarAIEmail.send(**{"email":"amari.lawal@gmail.com","subject":f"CaesarAI Games Cancel {task_id} Raspberry Pi Error ","message":f" Error: {type(ex)},{ex}, Task ID: {task_id}"})
        return {"error":f"{type(ex)},{ex}"}

if __name__ == "__main__":
    uvicorn.run("main:app",port=8082,log_level="info")

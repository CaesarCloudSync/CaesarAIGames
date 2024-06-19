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
@app.get('/api/v1/downloadgame')# GET # allow all origins all methods.
async def downloadgame(url:str):
    try:
        task = create_task.delay(url)
        return JSONResponse({"task_id": task.id})
    except Exception as ex:
        return {"error":f"{type(ex)},{ex}"}

@app.get("/tasks")
def get_status(task_id:str,url:str):
    task_result = AsyncResult(task_id)
  
    filename = f"/media/amari/SSD T7/steamunlockedgames/{url.split('&')[-1].split('=')[-1]}"
    print(filename)
    progress = r.get(f"{filename}-progress")
 
    progress = progress.decode("utf-8") if progress else "0"
    print(progress)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result,
        "filename":filename,
        "progress":progress
    }
    return JSONResponse(result)

if __name__ == "__main__":
    uvicorn.run("main:app",port=8080,log_level="info")

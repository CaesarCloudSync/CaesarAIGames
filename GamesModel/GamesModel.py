from pydantic import BaseModel

class GameModel(BaseModel):
    url:str
class ProgressModel(BaseModel):
    task_id:str
    filename:str
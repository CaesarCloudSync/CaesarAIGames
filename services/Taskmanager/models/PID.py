from pydantic import BaseModel
class PID(BaseModel):
    pid: int
    name: str
    username: str
    cpu_percent: float
    memory_percent: float
    exe: str

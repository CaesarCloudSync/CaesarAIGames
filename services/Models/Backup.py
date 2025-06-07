from pydantic import BaseModel, computed_field, Field,field_validator
import re
from datetime import datetime
import uuid
from typing import Optional
import hashlib
from typing import ClassVar,Literal,Union
class Backup(BaseModel):
    BACKUPTABLENAME: ClassVar[str] = "backup"
    backup_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    game_name :str
    status:str
    BACKUPDATATYPES: ClassVar[tuple] = (
            "TEXT PRIMARY KEY",      # Backup_id as UUID (TEXT NOT NULL format)
            "TEXT NOT NULL",   
            "TEXT NOT NULL"
        )
    
    @classmethod
    def fields_to_tuple(cls) -> tuple:
        return tuple(cls.model_fields)
    
    def values_to_tuple(self) -> tuple:
        return tuple(self.model_dump().values())
    @classmethod
    def get_field_name(cls,value) -> Union[str,None]:
        keys = list(cls.model_fields)
        if value in keys:
            return value
        else:
            raise ValueError(value)

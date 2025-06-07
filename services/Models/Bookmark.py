from pydantic import BaseModel, computed_field, Field,field_validator
import re
import json
from datetime import datetime
import uuid
from typing import Optional
import hashlib
from typing import ClassVar,Literal,Union
from services.Models import Game
class Library(BaseModel):
    LIBRARYTABLENAME: ClassVar[str] = "library"
    library_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    game_name :str
    game_data: Game
    LIBRARYDATATYPES: ClassVar[tuple] = (
            "TEXT PRIMARY KEY",      # Library_id as UUID (TEXT NOT NULL format)
            "TEXT NOT NULL",                  # first_name as TEXT NOT NULL
            "TEXT NOT NULL",                  # last_name as TEXT NOT NULL
        )
    
    @classmethod
    def fields_to_tuple(cls) -> tuple:
        return tuple(cls.model_fields)
    
    def values_to_tuple(self) -> tuple:
        values = []
        for value in self.model_dump().values():
            if isinstance(value,Game):
                values.append(json.dumps(value))
            else:
                values.append(value)
        return tuple(values)
    @classmethod
    def get_field_name(cls,value) -> Union[str,None]:
        keys = list(cls.model_fields)
        if value in keys:
            return value
        else:
            raise ValueError(value)

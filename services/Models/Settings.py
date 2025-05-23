from pydantic import BaseModel, computed_field, Field,field_validator
import re
from datetime import datetime
import uuid
from typing import Optional
import hashlib
from typing import ClassVar,Literal,Union
class Settings(BaseModel):
    SETTINGSTABLENAME: ClassVar[str] = "settings"
    settings_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    install_folder: str
    saved_games_folder:str
    SETTINGSDATATYPES: ClassVar[tuple] = (
            "TEXT PRIMARY KEY",      # settings_id as UUID (TEXT NOT NULL format)
            "TEXT NOT NULL",                  # first_name as TEXT NOT NULL
            "TEXT NOT NULL",                  # last_name as TEXT NOT NULL
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

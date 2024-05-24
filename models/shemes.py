from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy import Identity
from enum import Enum

class Main_User(BaseModel):
    id: Annotated[int | None, Identity(start=10)] = None
    name: str | None = None
    age: int

class Main_Level(BaseModel):
    id: Annotated[int | None, Identity(start=1)] = None
    size: int
    body: str | None = None

class Tags(Enum):
    user = "users"
    level = "level"
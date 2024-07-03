from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy import Identity
from enum import Enum


class Main_Data(BaseModel):
    id: Annotated[int | None, Identity(start=10)] = None
    size: int = Field(default=2, ge=1, lt=20)
    body: str | None = Field(default="0000")
    start_x: int = Field(ge=0, lt=20)
    start_y: int = Field(ge=0, lt=20)
    end_x: int = Field(ge=0, lt=20)
    end_y: int = Field(ge=0, lt=20)

class Tags(Enum):
    user = "users"
    level = "level"

class Main_User(BaseModel):
    id: Annotated[int | None, Identity(start=10)] = None
    name: str | None = None
    age: int

class Main_Start_Point(Main_Data):
    start_x: int
    start_y: int

class Main_End_Point(Main_Data):
    end_x: int
    end_y: int

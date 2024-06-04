from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy import Identity
from enum import Enum

class Main_User(BaseModel):
    id: Annotated[int | None, Identity(start=10)] = None
    name: str | None = None
    age: int

# class Main_Level(BaseModel):
#     id: Annotated[int | None, Identity(start=1)] = None
#     size: int
#     body: str | None = None
#     start_x: int
#     start_y: int
#     end_x: int
#     end_y: int

class Main_Data(BaseModel):
    id: Annotated[int | None, Identity(start=1)] = None
    size: int = Field(ge=1)
    body: str | None = None
    start_x: int
    start_y: int
    end_x: int
    end_y: int

class Main_Start_Point(Main_Data):
    start_x: int
    start_y: int

class Main_End_Point(Main_Data):
    end_x: int
    end_y: int

class Tags(Enum):
    user = "users"
    level = "level"
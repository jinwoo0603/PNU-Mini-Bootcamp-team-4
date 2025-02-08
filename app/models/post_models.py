from enum import Enum
from time import time
from pydantic import BaseModel
from typing import Optional, Literal
from dataclasses import dataclass
from sqlmodel import Field, SQLModel, Session

class RESULT_CODE(Enum):
    SUCCESS = 1
    NOT_FOUND = -2
    FAILED = -3

class Post(SQLModel, table=True):
    post_id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    title: str
    body: str
    created_at: int | None = Field(index=True)
    published: bool = Field(index=True)

@dataclass
class CreatePostReq:
    user_id: int
    title: str
    body: str
    published: bool = False

@dataclass
class UpdatePostReq:
    title: Optional[str] = None
    body: Optional[str] = None
    published: Optional[bool] = False
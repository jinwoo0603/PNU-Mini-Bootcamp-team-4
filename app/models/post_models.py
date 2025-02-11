from enum import IntEnum
from typing import Optional
from dataclasses import dataclass
from pydantic import BaseModel
from sqlmodel import Field, SQLModel

class LikeOp(IntEnum):
    LIKE = 1
    DISLIKE = -1

class Post(SQLModel, table=True):
    post_id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    title: str
    body: str
    created_at: int | None = Field(index=True)
    published: bool = Field(index=True)
    likes: int

@dataclass
class CreatePostReq:
    user_id: int
    title: str
    body: str
    published: bool = False

class UpdatePostReq(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    published: Optional[bool] = None
from enum import Enum
from typing import Optional
from dataclasses import dataclass
from sqlmodel import Field, SQLModel

class LIKE_OPTION(Enum):
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

@dataclass
class UpdatePostReq:
    title: Optional[str] = None
    body: Optional[str] = None
    published: Optional[bool] = False
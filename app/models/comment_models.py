from enum import Enum
from typing import Optional
from dataclasses import dataclass
from sqlmodel import Field, SQLModel

class Comment(SQLModel, table=True):
    comment_id: int | None = Field(default=None, primary_key=True)
    post_id: int = Field(index=True)
    user_id: int
    body: str
    created_at: int | None = Field(index=True)
    published: bool = Field(index=True)

@dataclass
class CreateCommReq:
    comment_id: int
    post_id: int
    user_id: int
    body: str
    published: bool = False

@dataclass
class UpdateCommReq:
    body: Optional[str] = None
    published: Optional[bool] = False
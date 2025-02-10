from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import BaseModel

#친구 아이디, 닉네임, (프사?), 프로필 떠야함, from->to 형태로 db 작성
class Follow(SQLModel):
    from_user_id: int = Field(primary_key=True)
    to_user_id: int = Field(primary_key=True)
from sqlmodel import SQLModel, Field
from pydantic import BaseModel

class FollowReq(BaseModel):
    user_id: int
    friend_id: int

#친구 아이디, 닉네임, (프사?), 프로필 떠야함, from->to 형태로 db 작성
class Follow(SQLModel, table = True):
    user_id: int = Field(primary_key=True)
    friend_id: int = Field(primary_key=True)
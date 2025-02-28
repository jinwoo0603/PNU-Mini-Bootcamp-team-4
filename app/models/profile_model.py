
#로그인이 이미 되었다 가정하고 메인화면에서 구현되어야 할 기능을 구현하기
#프로필의 구성요소: 프로필 사진, 아이디(닉네임), 팔로잉, 팔로워, 바이오
#디비에서 아이디를 가져와야 될듯
from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import BaseModel

#Profile Request(input)
class CreateProfileReq(BaseModel):
    user_id: int
    username: str
    bio: Optional[str] = None
    published: bool

class UpdateProfileReq(BaseModel):
    username: Optional[str] = None
    bio: Optional[str] = None
    published: Optional[bool] = None

class Profile(SQLModel, table = True):
    user_id: int | None = Field(default=None, primary_key=True)
    username: str
    profile_pic_path: Optional[str] = None
    bio: Optional[str] = None
    published: bool = Field(index=True)
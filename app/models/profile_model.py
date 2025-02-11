
#로그인이 이미 되었다 가정하고 메인화면에서 구현되어야 할 기능을 구현하기
#프로필의 구성요소: 프로필 사진, 아이디(닉네임), 팔로잉, 팔로워, 바이오
#디비에서 아이디를 가져와야 될듯
from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import BaseModel

#Profile Request(input)
class CreateProfileReq(BaseModel):
    username: str
    bio: Optional[str] = None
    published: bool = Field(index=True)

# class ProfileResp(BaseModel):
#     pass

class Profile(SQLModel, table = True):
    user_id: int = Field(primary_key=True)
    username: str
    profile_pic_path: str
    bio: Optional[str] = None
    published: bool = Field(index=True)


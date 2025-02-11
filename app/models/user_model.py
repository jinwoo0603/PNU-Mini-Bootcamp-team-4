from sqlmodel import SQLModel, Field
from datetime import datetime

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    created_at: int | None = Field(index=True)

    login_id: str = Field(index=True)
    pwd: str = Field(default=None, exclude=True)

    name: str

    access_token: str | None = None

#from sqlmodel import SQLModel, Field
#from typing import Optional
#from datetime import datetime
#
#class User(SQLModel, table=True):
#    id: Optional[int] = Field(default=None, primary_key=True)
#    
#    login_id: str = Field(index=True, unique=True)
#    pwd: str  # 비밀번호는 응답 모델에서 제외하는 방식 사용
#
#    name: str
#    created_at: datetime = Field(default_factory=datetime.utcnow)  # 자동 생성
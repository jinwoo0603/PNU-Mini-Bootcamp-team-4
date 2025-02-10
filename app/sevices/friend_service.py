from sqlmodel import Session, select
from fastapi import HTTPException
from app.models.friend_models import *

class FriendService():
    def __init__(self, db: Session):
        self.db = db

    def follow(self, user_id: int):
        #TODO: user가 팔로우를 하면-from_user_id에 user_id, to_user_id에 freind_id를 넣고 table에 add
        pass
    
    def get_followers(self, user_id: int, page: int = 1, limit: int = 10):
        #나를 팔로우하는 사람의 프로필을 보이기
        if limit > 10:
            limit = 10
        nOffset = (page-1) * limit
        followers = self.db.exec(select(Follow).where(Follow.to_user_id == user_id).offset(nOffset)
            .limit(limit)).all()
        if not followers:
            raise HTTPException(status_code=404, detail="Followers not found")
        #to_user_id 들의 프로필을 get
        return followers

    def get_followings(self, user_id: int, page: int = 1, limit: int = 10):
        if limit > 10:
            limit = 10
        nOffset = (page-1) * limit
        followings = self.db.exec(select(Follow).where(Follow.from_user_id == user_id).offset(nOffset)
            .limit(limit)).all()
        if not followings:
            raise HTTPException(status_code=404, detail="Followers not found")
        #from_user_id 들의 프로필을 get
        return followings
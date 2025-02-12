from sqlmodel import Session, select
from fastapi import HTTPException
from app.models.friend_model import *
from app.sevices.profile_service import ProfileService

class FriendService():
    def __init__(self, db: Session):
        self.db = db

    def follow(self, req: FollowReq):
        #user가 팔로우를 하면- user_id(from), freind_id(to)를 넣고 table에 add
        friendModel = Follow()
        friendModel.user_id = req.user_id
        friendModel.friend_id = req.friend_id
        self.db.add(friendModel)
        self.db.commit()
        self.db.refresh(friendModel)
        return friendModel
    
    def get_followers(self, user_id: int, page: int = 1, limit: int = 10):
        #나를 팔로우하는 사람의 프로필을 보이기
        if limit > 10:
            limit = 10
        nOffset = (page-1) * limit
        followers = self.db.exec(select(Follow.user_id).where(Follow.friend_id == user_id).offset(nOffset)
            .limit(limit)).all()
        if not followers:
            raise HTTPException(status_code=404, detail="Followers not found")
        #to_user_id 들의 프로필을 get
        return ProfileService.get_profiles(self, followers, page, limit)

    def get_followings(self, user_id: int, page: int = 1, limit: int = 10):
        if limit > 10:
            limit = 10
        nOffset = (page-1) * limit
        followings = self.db.exec(select(Follow.friend_id).where(Follow.user_id == user_id).offset(nOffset)
            .limit(limit)).all()
        if not followings:
            raise HTTPException(status_code=404, detail="Followers not found")
        #from_user_id 들의 프로필을 get
        return ProfileService.get_profiles(self, followings, page, limit)
    
    def delete_follow(self, req: FollowReq):
        #TODO: delete from table
        follow = self.db.exec(select(Follow)
                     .where(Follow.user_id == req.user_id
                            and Follow.friend_id == req.friend_id)
                            ).first()
        if not follow:
            raise HTTPException(status_code=404, detail="Follow not found")
        self.db.delete(follow)
        self.db.commit()
        return {"message": "Follow deleted successfully"}

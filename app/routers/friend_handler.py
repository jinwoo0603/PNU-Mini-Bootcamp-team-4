from fastapi import APIRouter,Depends
from app.sevices.friend_service import *
from app.dependencies.db import get_db_session

router = APIRouter(prefix='/v1/friend')

#명세서랑 달라진 점: 팔로우 팔로워 분리

@router.post('')
def follow(req:FollowReq, db:Session = Depends(get_db_session)):
    friendService = FriendService(db)
    return friendService.follow(req)

# @router.get('/{user_id}/followers')
# def get_followers(user_id:str, db:Session = Depends(get_db_session)):
#     friendService = FriendService(db)
#     return friendService.get_followers(user_id)

@router.get('/{user_id}/followings')
def get_friends(user_id:str, db:Session = Depends(get_db_session)):
    friendService = FriendService(db)
    return friendService.get_friends(user_id)

@router.delete('/{profile_id}')
def delete_follow(req:FollowReq, db:Session = Depends(get_db_session)):
    friendService = FriendService(db)
    return friendService.delete_follow(req)
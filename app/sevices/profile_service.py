from sqlmodel import Session, select
from fastapi import HTTPException
from app.models.profile_model import *
import os
from app.models.utils import RESULT_CODE

class ProfileService():
    def __init__(self, db: Session):
        self.db = db

    def get_profile(self, user_id: int):
        profile = self.db.exec(select(Profile).where(Profile.user_id == user_id)).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        return profile
    
    def get_profiles(self, users: list, page: int = 1, limit: int = 10):
        #팔로우/팔로워 테이블에서 팔로워 리스트(users)를 추출했을 때, 해당하는 프로필들을 가져오기
        if limit > 10:
            limit = 10
        nOffset = (page-1) * limit
        profiles = self.db.exec(select(Profile).where(Profile.id.in_(users))
                                .offset(nOffset).limit(limit)).all()
        return profiles
    
    def get_profiles_test(self, page: int = 1, limit: int = 10):
        if limit > 10:
            limit = 10
        nOffset = (page-1) * limit
        profiles = self.db.exec(select(Profile).offset(nOffset).limit(limit)).all()
        return profiles

    def create_profile(self, profile_data:CreateProfileReq):
        db_profile = Profile(**profile_data.model_dump())
        self.db.add(db_profile)
        self.db.commit()
        self.db.refresh(db_profile)
        return db_profile
    
    def update_profile(self, user_id:int, req: UpdateProfileReq):
        oldProfile = self.db.exec(select(Profile).where(Profile.user_id == user_id)).first()
        if not oldProfile:
            raise HTTPException(status_code=404, detail="Profile not found")
        dictToUpdate = req.model_dump(exclude_unset=True)
        oldProfile.sqlmodel_update(dictToUpdate)
        try:
            self.db.add(oldProfile)
            self.db.commit()
            self.db.refresh(oldProfile)
        except Exception as e:
            print(e)
            return (None, RESULT_CODE.FAILED)
        return (oldProfile, RESULT_CODE.SUCCESS)

    def delete_profile(self, user_id:int):
        profile = self.db.exec(select(Profile).where(Profile.user_id == user_id)).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        if profile.profile_pic_path:
            os.remove(profile.profile_pic_path)
        self.db.delete(profile)
        self.db.commit()
        return {"message": "Profile deleted successfully"}
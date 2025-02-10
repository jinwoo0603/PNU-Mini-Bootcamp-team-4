from sqlmodel import Session, select
from fastapi import HTTPException
from app.models.profile_model import *

class ProfileService():
    def __init__(self, db: Session):
        self.db = db

    def get_profile(self, user_id: int):
        profile = self.db.exec(select(Profile).where(Profile.user_id == user_id)).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        return profile

    def create_profile(self, profile_data:CreateProfileReq):
        db_profile = Profile(**profile_data.model_dump())
        self.db.add(db_profile)
        self.db.commit()
        self.db.refresh(db_profile)
        return db_profile
    
    def update_profile(self, user_id:int, profile_data: CreateProfileReq):
        profile = self.db.exec(select(Profile).where(Profile.user_id == user_id)).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        for key, value in profile_data.model_dump().items():
            setattr(profile, key, value)
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def delete_profile(self, user_id:int):
        profile = self.db.exec(select(Profile).where(Profile.user_id == user_id)).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        self.db.delete(profile)
        self.db.commit()
        return {"message": "Profile deleted successfully"}
from fastapi import APIRouter,Depends
from app.sevices.profile_service import *
from app.dependencies.db import get_db_session

router = APIRouter(prefix='/v1/profile')

@router.get('/{user_id}')
def get_profiles(user_id:str, db:Session = Depends(get_db_session)):
    profileService = ProfileService(db)
    return profileService.get_profile(user_id)

@router.post('')
def create_profile(profile:CreateProfileReq, db:Session = Depends(get_db_session)):
    profileService = ProfileService(db)
    return profileService.create_profile(profile)

@router.patch('/{profile_id}')
def update_profile(user_id:int, profile:CreateProfileReq, db:Session = Depends(get_db_session)):
    profileService = ProfileService(db)
    return profileService.update_profile(user_id, profile, profileService)

@router.delete('/{profile_id}')
def delete_profile(user_id:int, db:Session = Depends(get_db_session)):
    profileService = ProfileService(db)
    return profileService.delete_profile(user_id)
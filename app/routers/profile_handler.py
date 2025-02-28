from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import FileResponse
from app.sevices.profile_service import *
from app.dependencies.db import get_db_session
import shutil
import os

PROFILE_PIC_DIR = "profile_pics"
os.makedirs(PROFILE_PIC_DIR, exist_ok=True)

router = APIRouter(prefix='/v1/profile')

@router.get('/')
def get_profiles(user_id: int = None, db:Session = Depends(get_db_session)):
    profileService = ProfileService(db)
    if not user_id:
        return profileService.get_profiles_test()
    return profileService.get_profile(user_id)

@router.post('')
def create_profile(profile:CreateProfileReq, db:Session = Depends(get_db_session)):
    profileService = ProfileService(db)
    return profileService.create_profile(profile)

@router.patch('/{profile_id}')
def update_profile(user_id:int, profile:UpdateProfileReq, db:Session = Depends(get_db_session)):
    profileService = ProfileService(db)
    return profileService.update_profile(user_id, profile)

@router.delete('/{profile_id}')
def delete_profile(user_id:int, db:Session = Depends(get_db_session)):
    profileService = ProfileService(db)
    return profileService.delete_profile(user_id)

@router.post("/{user_id}/upload-profile-pic")
def upload_profile_pic(user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db_session)):
    profile = db.exec(select(Profile).where(Profile.user_id == user_id)).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    file_path = os.path.join(PROFILE_PIC_DIR, f"profile_{user_id}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    profile.profile_pic_path = file_path
    db.commit()
    db.refresh(profile)
    return {"message": "Profile picture uploaded successfully", "profile_pic_path": file_path}

@router.get("/{user_id}/profile-pic")
def get_profile_pic(user_id: int, db: Session = Depends(get_db_session)):
    profile = db.exec(select(Profile).where(Profile.user_id == user_id)).first()
    if not profile or not profile.profile_pic_path:
        raise HTTPException(status_code=404, detail="Profile picture not found")
    return FileResponse(profile.profile_pic_path)
from sqlmodel import (
    Session, select
)
import time
import os
from app.models.post_models import *
from app.models.utils import RESULT_CODE

class FileService():
    def save_file(self, post_id: int, file_db: Session, file_name: str, file_data: bytes):
        strPath = os.path.join('app', 'files', f"{post_id}_{file_name}")
        
        try:
            with open(strPath, 'wb') as f:
                f.write(file_data)
        except Exception as e:
            print(e)
            return None
        
        fileModel = Files()
        fileModel.post_id = post_id
        fileModel.url = strPath
        fileModel.created_at = int(time.time())
        
        file_db.add(fileModel)
        file_db.commit()
        file_db.refresh(fileModel)
        
        return fileModel
    
    def get_file(self,
                  post_id: int,
                  file_db: Session):
        file = file_db.exec(
            select(Files)
            .filter(Files.post_id == post_id)
        ).first()

        # NOTE: 배포시 클라이언트가 접근 가능한 경로로 전처리하도록 수정
        return file.url
    
    def delete_files(self,
                     post_id: int,
                     file_db: Session):
        files = file_db.exec(
            select(Files)
            .filter(Files.post_id == post_id)
        ).all()
        for file in files:
            filePath = file.url
            try:
                file_db.delete(file)
                file_db.commit()
                if os.path.exists(filePath):
                    os.remove(filePath)
            except Exception as e:
                return RESULT_CODE.FAILED
        return RESULT_CODE.SUCCESS
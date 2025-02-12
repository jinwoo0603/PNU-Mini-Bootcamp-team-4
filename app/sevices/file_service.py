from sqlmodel import (
    Session, select
)
import time
import os
from app.models.post_models import *
from app.models.utils import RESULT_CODE

class FileService():
    def save_files(self,
                   post_id: int,
                   file_db: Session,
                   files: dict[str, bytes]):
        fileModels = []

        for filename in files:
            fileData = files[filename]
            
            strPath = os.path.join('app\\files', str(post_id) + "_" + filename)
            try:
                with open(strPath, 'wb') as f:
                    f.write(fileData)
            except Exception as e:
                print(e)
                continue
            fileModel = Files()
            fileModel.post_id = post_id
            fileModel.url = strPath
            fileModel.created_at = int(time.time())
            file_db.add(fileModel)  
            fileModels.append(fileModel)
            file_db.commit()
            file_db.refresh(fileModel)
        
        return fileModels
    
    def get_files(self,
                  post_id: int,
                  file_db: Session):
        files = file_db.exec(
            select(Files)
            .filter(Files.post_id == post_id)
        ).all()

        # NOTE: 배포시 클라이언트가 접근 가능한 경로로 전처리하도록 수정
        return [file.url for file in files]
    
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
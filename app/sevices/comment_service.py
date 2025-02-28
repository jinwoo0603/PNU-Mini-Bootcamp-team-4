from dataclasses import asdict
from sqlmodel import (
    Session, select
)
import time
from app.models.comment_models import *
from app.models.utils import RESULT_CODE

class CommentService:
    def get_comment(self,
                    db: Session,
                    post_id: int):
        comments = db.exec(
            select(Comment)
            .filter(Comment.post_id == post_id)
        ).all()
        return comments
    
    def create_comment(self,
                    post_id:int,
                    db:Session,
                    req: CreateCommReq):
        commModel = Comment()
        commModel.post_id = post_id
        commModel.user_id = req.user_id
        commModel.body = req.body
        commModel.created_at = int(time.time())
        commModel.published = req.published
        db.add(commModel)
        db.commit()
        db.refresh(commModel)
        return commModel

    def update_comment(self,
                    db:Session, 
                    comment_id: int,
                    req: UpdateCommReq) -> tuple[Comment|None,RESULT_CODE]:
        oldComm = db.get(Comment, comment_id)
        oldComm = db.exec(
            select(Comment)
            .where(Comment.comment_id == comment_id)
        ).first()
        if not oldComm:
            return (None, RESULT_CODE.NOT_FOUND)
        
        dictToUpdate = asdict(req)
        oldComm.sqlmodel_update(dictToUpdate)
        try:
            db.add(oldComm)
            db.commit()
            db.refresh(oldComm)
        except:
            return (None, RESULT_CODE.FAILED)
        return (oldComm, RESULT_CODE.SUCCESS)

    def delete_comment(self,
                    db: Session,
                    comment_id: int) -> RESULT_CODE:
        comment = db.exec(
            select(Comment)
            .where(Comment.comment_id == comment_id)
        ).first()
        if not comment:
            return RESULT_CODE.NOT_FOUND 
        try:
            db.delete(comment)
            db.commit()
        except:
            return RESULT_CODE.FAILED
        return RESULT_CODE.SUCCESS

from fastapi import APIRouter, Depends
from app.dependencies.db import get_db_session
from app.models.comment_models import *
from app.sevices.comment_service import CommentService

router = APIRouter(
    prefix='/v1/comment'
)

@router.get('/')
def get_comment(post_id: int,
                db=Depends(get_db_session),
                commService: CommentService = Depends()):
    return commService.get_comment(db=db,
                                   post_id=post_id)

@router.post('/{post_id}')
def create_comment(req: CreateCommReq, post_id:int,
                   db=Depends(get_db_session),
                   commService: CommentService = Depends()):
    return commService.create_comment(db=db,post_id=post_id,
                                      req=req)

@router.put('/{comment_id}')
def update_comment(comment_id: int,
                   req: UpdateCommReq,
                   db=Depends(get_db_session),
                   commService: CommentService = Depends()):
    return commService.update_comment(db=db,
                                      comment_id=comment_id,
                                      req=req)

@router.delete('/{comment_id}')
def delete_comment(comment_id: int,
                   db=Depends(get_db_session),
                   commService: CommentService = Depends()):
    return commService.delete_comment(db=db,
                                      comment_id=comment_id)
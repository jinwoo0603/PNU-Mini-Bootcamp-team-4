from fastapi import APIRouter, Depends
from ..dependencies.db import get_db_session
from ..models.comment_models import *
from ..sevices.comment_service import CommentService

router = APIRouter(
    prefix='/v1/comment'
)

@router.get('/')
def get_comment(post_id: int,
                db=Depends(get_db_session),
                commService: CommentService = Depends()):
    return commService.get_comment(db=db,
                                   post_id=post_id)

@router.post('/')
def create_comment(req: CreateCommReq,
                   db=Depends(get_db_session),
                   commService: CommentService = Depends()):
    return commService.create_comment(db=db,
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
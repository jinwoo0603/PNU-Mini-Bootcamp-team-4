from fastapi import APIRouter, Depends
from ..dependencies.db import get_db_session
from ..models.post_models import *
from ..sevices.post_service import PostService

router = APIRouter(
    prefix='/v1/post'
)

@router.post('/')
def create_post(req: CreatePostReq,
               db=Depends(get_db_session),
               postService: PostService = Depends()):
    return postService.create_post(db=db,
                                   req=req)

@router.get('/')
def get_posts(db=Depends(get_db_session),
              postService: PostService = Depends()):
    return postService.get_posts(db=db)

@router.get('/filter')
def get_filtered_post(user_id: int,
                      db=Depends(get_db_session),
                      postService: PostService = Depends()):
    return postService.get_filtered_posts(db=db,
                                          user_id=user_id)

@router.patch('/{post_id}')
def update_post(post_id: int,
                req: UpdatePostReq,
                db=Depends(get_db_session),
                postService: PostService = Depends()):
    return postService.update_post(db=db,
                                   post_id=post_id,
                                   req=req)

@router.delete('/{post_id}')
def delete_post(post_id: int,
                db=Depends(get_db_session),
                postService: PostService = Depends()):
    return postService.delete_post(db=db,
                                   post_id=post_id)

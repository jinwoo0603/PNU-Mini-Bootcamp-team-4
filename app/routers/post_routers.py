from fastapi import APIRouter, Depends
from app.dependencies.db import get_db_session
from app.models.post_models import *
from app.sevices.post_service import PostService

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
def get_posts(post_id: int = None,
              db=Depends(get_db_session),
              postService: PostService = Depends()):
    if post_id:
        return postService.get_post(db=db,
                                    post_id=post_id)
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

# 좋아요 기능 초안
@router.put('/{post_id}/like')
def like(post_id: int,
         like_op: LikeOp = Depends(),
         db=Depends(get_db_session),
         postService: PostService = Depends()):
    return postService.like(db=db,
                            post_id=post_id,
                            like_op=like_op)

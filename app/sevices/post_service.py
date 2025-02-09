from dataclasses import asdict
from sqlmodel import (
    Session, select
)
import time
from ..models.post_models import *
from ..models.utils import RESULT_CODE

class PostService:
    def get_filtered_posts(self,
                           db: Session,
                           user_id: int,
                           limit:int=10):
        if limit > 10:
            limit = 10
        posts = db.exec(
            select(Post)
            .filter(Post.user_id == user_id)
            .limit(limit)
        ).all()
        return posts
    
    def get_post(self,
                 db: Session,
                 post_id: int):
        post = db.get(Post, post_id)
        if not post:
            return RESULT_CODE.NOT_FOUND 
        return post

    def get_posts(self,
                  db: Session,
                  page: int=1,
                  limit:int=10):
        if limit > 10:
            limit = 10
        nOffset = (page-1) * limit
        posts = db.exec(
            select(Post)
            .offset(nOffset)
            .limit(limit)
        ).all()
        return posts

    def create_post(self,
                    db:Session,
                    req: CreatePostReq):
        postModel = Post()
        postModel.user_id = req.user_id
        postModel.title = req.title
        postModel.body = req.body
        postModel.created_at = int(time.time())
        postModel.published = req.published
        db.add(postModel)
        db.commit()
        db.refresh(postModel)
        return postModel

    def update_post(self,
                    db:Session, 
                    post_id: int,
                    req: UpdatePostReq) -> tuple[Post|None,RESULT_CODE]:
        oldPost = db.get(Post, post_id)
        if not oldPost:
            return (None, RESULT_CODE.NOT_FOUND)
        
        dictToUpdate = asdict(req)
        oldPost.sqlmodel_update(dictToUpdate)
        try:
            db.add(oldPost)
            db.commit()
            db.refresh(oldPost)
        except:
            return (None, RESULT_CODE.FAILED)
        return (oldPost, RESULT_CODE.SUCCESS)

    def delete_post(self,
                    db: Session,
                    post_id: int) -> RESULT_CODE:
        post = db.get(Post, post_id)
        if not post:
            return RESULT_CODE.NOT_FOUND 
        try:
            db.delete(post)
            db.commit()
        except:
            return RESULT_CODE.FAILED
        return RESULT_CODE.SUCCESS

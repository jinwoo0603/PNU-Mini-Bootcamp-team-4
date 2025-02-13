from fastapi import APIRouter, UploadFile, BackgroundTasks, Depends
from fastapi.responses import FileResponse
from app.dependencies.db import get_db_session
from app.dependencies.file_db import get_files_session
from app.models.post_models import *
from app.sevices.post_service import PostService
from app.sevices.file_service import FileService
from app.models.utils import RESULT_CODE

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
              page: int = 1,
              limit: int = 20,
              db=Depends(get_db_session),
              postService: PostService = Depends()):
    if post_id:
        return postService.get_post(db=db,
                                    post_id=post_id)
    return postService.get_posts(page=page,
                                 limit=limit,
                                 db=db)

@router.get('/filter')
def get_filtered_post(user_id: int,
                      limit: int = 20,
                      db=Depends(get_db_session),
                      postService: PostService = Depends()):
    return postService.get_filtered_posts(limit=limit,
                                          db=db,
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
                file_db=Depends(get_files_session),
                postService: PostService = Depends(),
                fileService: FileService = Depends()):
    fileService.delete_files(post_id=post_id,
                                file_db=file_db)
    return postService.delete_post(db=db,
                                   post_id=post_id)

@router.put('/{post_id}/like')
def like(post_id: int,
         like_op: LikeOp,
         db=Depends(get_db_session),
         postService: PostService = Depends()):
    return postService.like(db=db,
                            post_id=post_id,
                            like_op=like_op)

@router.post('/{post_id}/upload')
def upload_file(post_id: int,
                file: UploadFile,
                file_db=Depends(get_files_session),
                fileService: FileService = Depends()):
    if not file or len(file.filename) == 0:
        return {"error": "No file provided"}
    
    file_data = file.file.read()
    return fileService.save_file(post_id=post_id,
                                 file_db=file_db,
                                 file_name=file.filename,
                                 file_data=file_data)

@router.get('/{post_id}/files')
def get_files(post_id: int,
              file_db=Depends(get_files_session),
              fileService: FileService = Depends()):
    return fileService.get_file(post_id=post_id,
                                 file_db=file_db)
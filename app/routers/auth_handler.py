# app/routers/auth_router.py

from fastapi import APIRouter, Depends, HTTPException, Header
from typing import Annotated
import time

from app.models.parameter_model import AuthSignupReq, AuthSigninReq
from app.dependencies.db import get_db_session
from app.dependencies.jwt_db import JWTUtil
from app.sevices.auth_service import AuthService

router = APIRouter(prefix='/auth')

# 1. signup
@router.post('/signup')
def auth_signup(req: AuthSignupReq,
                db=Depends(get_db_session),
                jwtUtil: JWTUtil=Depends(),
                authService: AuthService=Depends()):
    user = authService.signup(db, req.login_id, req.pwd, req.name)
    if not user:
        raise HTTPException(status_code=400, detail="뭔가 잘못됐다.")
    user.access_token = jwtUtil.create_token(user.model_dump())
    return user


# 2. signin
@router.post("/signin")
def auth_signin(req: AuthSigninReq, 
                db=Depends(get_db_session),
                jwtUtil: JWTUtil=Depends(),
                authService: AuthService=Depends()):
    user = authService.signin(db, req.login_id, req.pwd)
    if not user:
        raise HTTPException(status_code=401, detail="로그인 실패")
    
    user.access_token = jwtUtil.create_token(user.model_dump())
    return user

# /auth/me
# {'name': 'linux'}
@router.get('/me')
def get_me(Authorization: Annotated[str, Header()],
           jwtUtil: JWTUtil = Depends()):
    token = Authorization.replace('Bearer ', '')
    userDict = jwtUtil.decode_token(token)
    if userDict is None:
        raise HTTPException(status_code=401, detail="bye")

    # 검증이 완료됐다.

    # 필요하다면 Redis에 저장된 토큰이 있는지 검사해본다.

    # post.author_id = userDict.get('id', 0)
    # postService.add_post(db, post, user.id)

    return {'user': userDict}

# app/routers/auth_router.py

import time
from fastapi import APIRouter, Depends, HTTPException, Header
from typing import Annotated

from app.models.parameter_model import AuthSignupReq, AuthSigninReq
from app.dependencies.db import get_db_session
from app.dependencies.redis_db import *
from app.dependencies.jwt_db import JWTUtil
from app.sevices.auth_service import AuthService



router = APIRouter(prefix='/auth')

# 1. signup
@router.post('/signup')
def auth_signup(req: AuthSignupReq,
                db=Depends(get_db_session),
                jwtUtil: JWTUtil=Depends(),
                authService: AuthService=Depends(),
                redisDB = Depends(get_redis)):

    user = authService.signup(db, req.login_id, req.pwd, req.name)
    if not user:
        raise HTTPException(status_code=400, detail="ERROR")
    

    access_token = jwtUtil.create_token(user.model_dump())
   
    user.access_token = access_token

    redis_key = f"user:{user.id}" 
    redisDB.setex(redis_key, 3600, access_token)

    return user


# 2. signin
@router.post("/signin")
def auth_signin(req: AuthSigninReq, 
                db=Depends(get_db_session),
                jwtUtil: JWTUtil=Depends(),
                authService: AuthService=Depends(),
                redisDB=Depends(get_redis)):
    user = authService.signin(db, req.login_id, req.pwd)
    if not user:
        raise HTTPException(status_code=401, detail="로그인 실패")

    access_token = jwtUtil.create_token(user.model_dump())
    user.access_token = access_token

    redis_key = f"user:{user.id}" 
    redisDB.setex(redis_key, 3600, access_token)


    return user



# 3. signout
@router.post('/signout')
def auth_signout(Authorization: Annotated[str, Header()],
                 jwtUtil: JWTUtil = Depends(),
                 redisDB=Depends(get_redis)):
    token = Authorization.replace('Bearer ', '')
    userDict = jwtUtil.decode_token(token)

    # 토큰이 유효하지 않으면 에러 반환
    if userDict is None:
        raise HTTPException(status_code=401, detail="Invalid Token")

    nUserId = userDict.get('id', 0)

    # Redis에서 해당 유저의 토큰 삭제
    redis_key = f"user:{nUserId}"
    redisDB.delete(redis_key)

    return {"message": "Successfully signed out"}

# /auth/me
# {'name': 'linux'}
@router.get('/me')
def get_me(Authorization: Annotated[str, Header()],
           jwtUtil: JWTUtil = Depends(),
           redisDB = Depends(get_redis)):
    token = Authorization.replace('Bearer ', '')
    userDict = jwtUtil.decode_token(token)
    if userDict is None:
        raise HTTPException(status_code=401, detail="Invaild Token")


    nUserId = userDict.get('id', 0)
    userName = userDict.get('name', '')
    # 검증이 완료됐다.

    # 차단여부 검사사
    strBlackKey = f'blacklist:{nUserId}'
    ret = redisDB.get(strBlackKey)
    if ret is not None:
        raise HTTPException(status_code=401, detail="Blocked")
    # 
    #redis에 액세스 토근을 검사
    # Redis에 저장된 토큰이 있는지 검사해본다.
    strBlackKey = f'user:{nUserId}'
    ret = redisDB.get(strBlackKey)
    if ret is None:
        raise HTTPException(status_code=401, detail="unauthorized")

    # Todo

    return {'user': userDict, 'ret': ret}


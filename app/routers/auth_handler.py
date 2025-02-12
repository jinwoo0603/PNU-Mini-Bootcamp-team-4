# app/routers/auth_router.py

import time
from fastapi import APIRouter, Depends, HTTPException, Header
from typing import Annotated

from app.models.parameter_model import AuthSignupReq, AuthSigninReq
from app.dependencies.db import get_db_session, get_redis
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
        raise HTTPException(status_code=400, detail="ERROR")
    user.access_token = jwtUtil.create_token(user.model_dump())
    
    # 
    #redis_key = f"user:{user.id}"
    
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

    #

    return user

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

#  로그아웃 엔드포인트
@router.post('/logout')
def logout(Authorization: Annotated[str, Header()],
           redis=Depends(get_redis),
           jwtUtil: JWTUtil = Depends()):
    
    # 헤더에서 토큰 추출
    token = Authorization.replace('Bearer ', '')
    
    # 토큰 검증
    payload = jwtUtil.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰")

    # 토큰 만료 시간 가져오기
    exp_time = payload.get("exp", 0)
    current_time = int(time.time())

    if exp_time <= current_time:
        raise HTTPException(status_code=401, detail="이미 만료된 토큰")

    # Redis에 블랙리스트 추가 (TTL: exp - 현재 시간)
    redis.setex(f"blacklist:{token}", exp_time - current_time, "true")

    return {"message": "로그아웃 성공"}
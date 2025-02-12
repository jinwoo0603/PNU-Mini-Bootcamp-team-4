# app/dependencies/jwt_utils.py
from jose import jwt
from datetime import datetime, timedelta, timezone
import time

SECRET_KEY ="cf2abc207680ba85bc9ce0e587183225"
ALG = "HS256"

class JWTUtil:    
    # 1. JWT Token 생성 함수
    # Payload={
    #   "id": 1,
    #   "login_id": "loiss",
    #   "name": "aaaaa",
    #   "exp":fsdfsfsdf
    # }, 유효기간
    # -> Jwt token
    def create_token(self, payload: dict,
                    expires_delta: timedelta | None = timedelta(minutes=30)):
        payload_to_encode = payload.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        payload_to_encode.update({
            'exp': expire
        })
        return jwt.encode(payload_to_encode, SECRET_KEY, algorithm=ALG)

    # 2. token 문자열로 payload 만드는 함수
    def decode_token(self, token: str) -> dict | None:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALG])
            if payload is not None:
                nNow = int(time.time())
                nExpireAt = payload.get('exp', 0)
                if nExpireAt < nNow:
                    return None
                return payload
        except:
            pass
        return None



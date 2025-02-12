import redis
# Redis 클라이언트 설정 (localhost, 기본 포트 6379)
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

def get_redis():
    return redis_client

def save_token(user_id: int, token: str, expire_time: int = 1800):  # 30분
    """ JWT 토큰을 Redis에 저장하는 함수 """
    redis_key = f"user:{user_id}:token"
    redis_client.setex(redis_key, expire_time, token)

def get_token(user_id: int) -> str | None:
    """ Redis에서 JWT 토큰 가져오는 함수 """
    redis_key = f"user:{user_id}:token"
    return redis_client.get(redis_key)

def delete_token(user_id: int):
    """ Redis에서 JWT 토큰 삭제하는 함수 (로그아웃 시 사용) """
    redis_key = f"user:{user_id}:token"
    redis_client.delete(redis_key)
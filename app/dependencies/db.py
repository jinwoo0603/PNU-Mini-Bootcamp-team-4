from sqlmodel import Session, create_engine, SQLModel
from dotenv import load_dotenv
import redis

load_dotenv()

#db_url = os.getenv('DB_URL')
db_url = 'sqlite:///blog.db'
db_conn_args = {'check_same_thread': False}
db_engine = create_engine(db_url, connect_args=db_conn_args)

def get_db_session():
    with Session(db_engine) as session:
        yield session

def create_db():
    SQLModel.metadata.create_all(db_engine)


# Redis 클라이언트 설정 (localhost, 기본 포트 6379)
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

def get_redis():
    return redis_client
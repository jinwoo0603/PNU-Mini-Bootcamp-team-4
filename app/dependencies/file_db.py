from sqlmodel import Session, create_engine, SQLModel
import os
from dotenv import load_dotenv

load_dotenv()

#db_url = os.getenv('DB_URL')
db_url = 'sqlite:///file.db'
db_conn_args = {'check_same_thread': False}
db_engine = create_engine(db_url, connect_args=db_conn_args)

def get_files_session():
    with Session(db_engine) as session:
        yield session

def create_file_db():
    SQLModel.metadata.create_all(db_engine)

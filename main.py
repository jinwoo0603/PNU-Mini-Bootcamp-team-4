from fastapi import FastAPI
from app.dependencies.db import create_db
from contextlib import asynccontextmanager
from app.routers import profile_handler
from app.routers import post_routers
from app.routers import comment_routers
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield
    
app = FastAPI(lifespan=lifespan)
app.include_router(profile_handler.router)
app.include_router(post_routers.router)
app.include_router(comment_routers.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from fastapi import FastAPI
from app.dependencies.db import create_db
from contextlib import asynccontextmanager
from app.routers import profile_handler

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(profile_handler.router)
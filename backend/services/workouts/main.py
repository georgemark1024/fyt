from contextlib import asynccontextmanager
from fastapi import FastAPI

from .database import create_db_and_tables
from . import routers as workouts_routers

@asynccontextmanager
async def lifespan(lifespan_app: FastAPI):
    # Startup logic
    create_db_and_tables()
    yield
    # Shutdown logic

app = FastAPI(lifespan=lifespan)

app.include_router(workouts_routers.router)

@app.get("/")
async def root():
    return {"message": f"Welcome to Fyt Gym Tracker"}

from contextlib import asynccontextmanager
from fastapi import FastAPI

from workouts.database import create_db_and_tables
from workouts import routers as workouts_routers
from workouts import database

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

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
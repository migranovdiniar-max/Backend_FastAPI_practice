from fastapi import FastAPI, Body, Path
from pydantic import BaseModel, EmailStr
from typing import Annotated
from item_views import router as item_router
from mypackage.view import router as mypackage_router
from contextlib import asynccontextmanager
from core.models import Base, db_helper
from sqlalchemy import text, inspect
# -------------------------------------------------------------------------------- 


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield



app = FastAPI()
app.include_router(item_router)
app.include_router(mypackage_router)    


@app.get("/")
def hello_index():
    return {
    "message": "Hello, World!"
    }


@app.get("/hello/")
def hello(name: str = "world"):
    name = name.strip().title()
    return {
        "message": f"Hello, {name}!"
    }


@app.post("/calc/add/")
def add(a: int, b: int):
    return {
        "result": a + b
    }
    





from fastapi import FastAPI, Body, Path
from pydantic import BaseModel, EmailStr
from typing import Annotated
from item_views import router as item_router
from mypackage.view import router as mypackage_router
from contextlib import asynccontextmanager
from core.models import Base, db_helper
from sqlalchemy import text, inspect
from api_v1 import router as api_v1_router
from core.config import settings
# -------------------------------------------------------------------------------- 


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield



app = FastAPI(lifespan=lifespan)
app.include_router(api_v1_router, prefix=settings.api_v1_prefix, tags=["api_v1"])
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
    





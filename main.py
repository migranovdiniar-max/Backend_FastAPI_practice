from fastapi import FastAPI, Body
from pydantic import BaseModel, EmailStr

app = FastAPI()


class createUserRequest(BaseModel):
    email: EmailStr


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


@app.post("/users/")
def create_user(user_request: createUserRequest = Body(...)):
    return {
        "message": "Success",
        "email": user_request.email
    }

@app.post("/calc/add/")
def add(a: int, b: int):
    return {
        "result": a + b
    }
    

@app.get("/items/")
def list_items():
    return {
        "items": ["item1", "item2", "item3"]
    }


@app.get("/items/latest/")
def get_latest_item():
    return {"item": {
        "id": "0", 
        "name": "The latest item"
    }}


@app.get("/items/{item_id}/")
def get_item_by_id(item_id: str):
    return {
        "item": {
            "id": len(item_id),
        }
    }



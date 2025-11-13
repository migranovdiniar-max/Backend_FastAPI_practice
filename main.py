from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def hello_index():
    return {
    "message": "Hello, World!"
    }

@app.get("/items/")
def list_items():
    return {
        "items": ["item1", "item2", "item3"]
    }

@app.get("/items/{item_id}/")
def get_item_by_id(item_id: str):
    return {
        "item": {
            "id": len(item_id),
        }
    }
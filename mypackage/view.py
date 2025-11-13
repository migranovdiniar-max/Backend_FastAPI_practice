from fastapi import APIRouter, Body

from mypackage.schemas import createUserRequest
from mypackage import crud  


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/")
def create_user(user_request: createUserRequest = Body(...)):
    return crud.create_user(user_in=user_request)
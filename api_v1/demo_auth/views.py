import secrets
from fastapi import APIRouter, Depends, HTTPException, status, Header
from typing import Annotated
from fastapi.security import HTTPBasicCredentials, HTTPBasic

router = APIRouter(prefix="/demo-auth", tags=["Demo Auth"])

security = HTTPBasic()


@router.get("/basic-auth/")
def demo_basic_auth_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    return {
        "message": "Hey there",
        "username": credentials.username,
        "password": credentials.password,
    }


usernames_to_password = {
    "admin": "admin",
    "john": "password",
}

static_auth_token_to_username = {
    "53e10e5b774dcf0e496f8e10e5acd0e0c2": "admin",
    "61fdca1b37afa73109343468c14399": "password",
}


def get_auth_user_username(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"}
    )

    correct_password = usernames_to_password.get(credentials.username)
    if correct_password is None:
        raise unauthed_exc

    if credentials.username not in usernames_to_password:
        raise unauthed_exc
    
    # secretes 
    if not secrets.compare_digest(
        credentials.password.encode("utf-8"),
        correct_password.encode("utf-8")
    ):
        raise unauthed_exc
    
    return credentials.username


def get_username_by_static_auth_token(
        static_token: str = Header(alias="x-auth-token")
) -> str:
    if username := static_auth_token_to_username.get(static_token):
        return username
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="invalid toked")
    

@router.get("/basic-auth-username/")
def demo_basic_auth_username(
    auth_username: str = Depends(get_auth_user_username),
):
    return {
        "message": f"Hello, {auth_username}",
        "username": auth_username
    }


@router.get("/some-http-header-auth/")
def demo_auth_some_http_header(
    username: str = Depends(get_username_by_static_auth_token)
):
    return {
        "message": f"Hello, {username}",
        "username": username
    }
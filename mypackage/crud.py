from mypackage.schemas import createUserRequest


def create_user(user_in: createUserRequest) -> dict:
    # Implementation for creating a user
    user = user_in.model_dump()
    return {
        "success": True,
        "user": user,
    }
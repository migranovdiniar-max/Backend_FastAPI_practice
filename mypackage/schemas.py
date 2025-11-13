from pydantic import BaseModel, EmailStr, Field
from typing import Annotated
from annotated_types import MinLen, MaxLen


class createUserRequest(BaseModel):
    # username = Field(..., min_length=3, max_length=50)    
    username: Annotated[str, MinLen(3), MaxLen(50)] 
    email: EmailStr

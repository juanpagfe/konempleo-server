from typing import Optional
from pydantic import BaseModel

from models.models import UserEnum


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserToken(BaseModel):
    email: str
    fullname: str
    role: UserEnum
    id: int

class UpdatePassword(BaseModel):
    email: str
    current_password: str
    new_password: str
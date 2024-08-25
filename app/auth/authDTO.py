from typing import Optional
from pydantic import BaseModel

from app.user.userDTO import UserEnum

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

class UserToken(BaseModel):
    email: str
    fullname: str
    role: UserEnum
    company: int
    result: int
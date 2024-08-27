from datetime import datetime
from enum import IntEnum
from pydantic import BaseModel, EmailStr

from models.user import UserEnum

class UserCreateDTO(BaseModel):
    fullname: str
    email: EmailStr
    role: UserEnum

class UserInsert(BaseModel):
    fullname: str
    email: EmailStr
    password: str
    role: UserEnum


class UserBase(BaseModel):
    email: str
    fullname: str
    usertype: UserEnum
    deleted: bool
    active: bool
    created_at: datetime
    updated_at: datetime

class UserCreate(UserInsert):
    company_uid: str

class UserEnrollInsert(BaseModel):
    user_id: int
    company_id: int

class UserUpdateUser(BaseModel):
    first_name: str
    last_name: str
    phone: str
    country: str
    city: str

class AdminUpdateUser(BaseModel):
    first_name: str
    last_name: str
    phone: str
    country: str
    city: str
    deleted: bool
    active: bool

class UserSoftDelete(BaseModel):
    deleted: bool
    active: bool

# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: int
    password: str

    class Config:
        orm_mode: True

class UserWithResult(BaseModel):
    user: UserInDBBase
    result_id: int


# Properties to return to client
class User(UserInDBBase):
    pass


# Properties properties stored in DB
class UserInDB(UserInDBBase):
    pass
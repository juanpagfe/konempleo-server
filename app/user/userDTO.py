from datetime import datetime
from enum import IntEnum
from pydantic import BaseModel, EmailStr


class UserEnum(IntEnum):
    SUPERADMIN = 1
    ADMIN = 2
    USER = 3

class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    usertype: UserEnum
    dni: str
    phone: str
    country: str
    city: str
    deleted: bool
    active: bool
    created_at: datetime
    updated_at: datetime

class UserInsert(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    usertype: UserEnum

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
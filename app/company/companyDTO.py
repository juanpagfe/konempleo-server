from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Extra, StrictBytes

from app.user.userDTO import UserCreateDTO


class CompanyBase(BaseModel):
    name: str
    sector: str
    document: str
    document_type: str
    address: str
    city: str
    picture: str
    activeoffers: int
    totaloffers: int
    active: bool
    employees: int

class CompanyCreate(BaseModel):
    name: str
    sector: str
    document: str
    document_type: str
    address: str
    city: str
    picture: str
    employees: int
    responsible_user: UserCreateDTO

class CompanyUpdate(BaseModel,extra = Extra.forbid):
    name: str
    sector: str
    document: str
    document_type: str
    address: str
    city: str
    picture: str
    
class CompanySoftDelete(BaseModel):
    deleted: bool
    active: bool

# Properties shared by models stored in DB
class CompanyInDBBase(CompanyBase):
    id: int

    class Config:
        orm_mode: True

# Properties to return to client
class Company(CompanyInDBBase):
    pass

# Properties properties stored in DB
class CompanyInDB(CompanyInDBBase):
    pass
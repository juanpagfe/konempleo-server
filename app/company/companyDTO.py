from datetime import datetime
from typing import Optional
from fastapi import File, UploadFile
from pydantic import BaseModel, EmailStr, Extra, StrictBytes

from app.user.userDTO import UserCreateDTO


class CompanyBase(BaseModel):
    name: str
    sector: str
    document: str
    document_type: str
    city: str
    picture: Optional[str] = None
    activeoffers: Optional[int] = 0
    totaloffers: Optional[int] = 0
    active: bool = True
    employees: int

class CompanyCreate(BaseModel):
    name: str
    sector: str
    document: str
    document_type: str
    city: str
    employees: int
    activeoffers: Optional[int] = 0
    totaloffers: Optional[int] = 0
    employees: Optional[int] = 0
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

# Properties shared by models stored in DB
class CompanyInDBBaseWCount(CompanyBase):
    id: int
    cv_count: int

    class Config:
        orm_mode: True

# Properties to return to client
class Company(CompanyInDBBase):
    pass

# Properties to return to client
class CompanyWCount(CompanyInDBBaseWCount):
    pass

# Properties properties stored in DB
class CompanyInDB(CompanyInDBBase):
    pass
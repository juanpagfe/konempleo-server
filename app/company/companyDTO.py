from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Extra, StrictBytes


class CompanyBase(BaseModel):
    name: str
    country: str
    deleted: bool
    active: bool
    uid: str
    created_at: datetime
    updated_at: datetime

class CompanyCreate(BaseModel):
    name: str
    country: str
    uid: Optional[str] = None

class CompanyUpdate(BaseModel,extra = Extra.forbid):
    id: int
    name: Optional[str] = None
    country: Optional[str] = None
    uid: str
    
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
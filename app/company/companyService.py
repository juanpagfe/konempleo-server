
import os

from fastapi import HTTPException
from db import session
from app.baseController import ControllerBase
from app.company.companyDTO import CompanyCreate, CompanyUpdate, CompanySoftDelete
from models.company import Company
from cryptography.fernet import Fernet


class ServiceCompany(ControllerBase[Company, CompanyCreate, CompanyUpdate, CompanySoftDelete]): 
    ...

company = ServiceCompany(Company)

def getByName(db: session, uid: str) -> Company:
    fernet = Fernet(os.getenv("UID_KEY"))
    try:
        name = fernet.decrypt(uid).decode()
    except:
        raise HTTPException(status_code=404, detail="No company with given uid")     
    return db.query(Company).filter(Company.name == name).first()
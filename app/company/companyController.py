

import base64
import os
from fastapi import APIRouter, Depends, HTTPException
from app.company.companyDTO import Company, CompanyCreate, CompanySoftDelete, CompanyUpdate
from sqlalchemy.orm import Session
from app.company.companyService import company
from app import deps
from cryptography.fernet import Fernet


companyRouter = APIRouter()
companyRouter.tags = ['Company']

@companyRouter.post("/company/", status_code=201, response_model=Company)
def create_company(
    *, company_in: CompanyCreate, db: Session = Depends(deps.get_db)
) -> dict:
    """
    Create a new company in the database.
    """
    fernet = Fernet(os.getenv("UID_KEY"))
    company_in.uid = str(fernet.encrypt(company_in.name.encode()), encoding='utf-8')
    companyCreated = company.create(db=db, obj_in=company_in)
    return companyCreated

@companyRouter.get("/company/{company_id}", status_code=200, response_model=Company)
def get_company(
    *, db: Session = Depends(deps.get_db), company_id
) -> dict:
    """
    gets company in the database.
    """
    currentCompany = company.get(db=db, id=company_id)
    if currentCompany == None:
        raise HTTPException(status_code=404, detail="No company with given id: "+company_id)

    return currentCompany

@companyRouter.put("/company/", status_code=200, response_model=Company)
def update_company(
    *, company_in: CompanyUpdate, db: Session = Depends(deps.get_db)
) -> dict:
    """
    Updates a company in the database.
    """
    company2Update = company.get(db=db, id=company_in.id)
    if company2Update == None:
        raise HTTPException(status_code=404, detail="No company with given id: " + company_in.id)
    companyUpdated = company.update(db=db, db_obj=company2Update, obj_in=company_in)

    return companyUpdated

@companyRouter.put("/company/delete/{company_id}", status_code=200, response_model=Company)
def update_company(
    *, db: Session = Depends(deps.get_db), company_id
) -> dict:
    """
    Deletes a company in the database.
    """
    company2Delete = company.get(db=db, id=company_id)
    if company2Delete == None:
        raise HTTPException(status_code=404, detail="No company with given id: " + company_id)
    softDeleteParams = CompanySoftDelete(**{ 'deleted':True, 'active':False})
    companyUpdated = company.softDelete(db=db, db_obj=company2Delete, obj_in=softDeleteParams)

    return companyUpdated
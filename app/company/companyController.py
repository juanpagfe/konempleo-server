

import base64
import os
from fastapi import APIRouter, Depends, HTTPException
from app.auth.authService import get_password_hash
from app.company.companyDTO import Company, CompanyCreate, CompanySoftDelete, CompanyUpdate
from sqlalchemy.orm import Session
from app.company.companyService import company
from app import deps
from cryptography.fernet import Fernet

from models.companyUser import CompanyUser
from models.user import Users


companyRouter = APIRouter()
companyRouter.tags = ['Company']

@companyRouter.post("/company/", status_code=201, response_model=Company)
def create_company(
    *, company_in: CompanyCreate, db: Session = Depends(deps.get_db)
) -> dict:
    """
    Create a new company in the database.
    """
    try:
        with db.begin():
            user = Users(
                fullname= company_in.responsible_user.fullname,
                email= company_in.responsible_user.email,
                password= get_password_hash('deeptalentUser'),
                role= company_in.responsible_user.role,
            )
            db.add(user)
            db.flush() 

            company = Company(
                name=company_in.name,
                sector= company_in.sector,
                document= company_in.document,
                document_type= company_in.document_type,
                address= company_in.address,
                city= company_in.city,
                picture= company_in.picture,
                employees= company_in.employees,
            )
            db.add(company)
            db.flush()  

            company_user = CompanyUser(
                companyId=company.id,
                userId=user.id
            )
            db.add(company_user)

        return company

    except Exception as e:
        # If any operation fails, the transaction is rolled back automatically
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

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

from typing import List, Optional
from fastapi import APIRouter, Body, Depends, File, HTTPException, UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func
from app.auth.authDTO import UserToken
from app.auth.authService import get_password_hash, get_user_current
from app.company.companyDTO import Company, CompanyCreate, CompanyWCount
from sqlalchemy.orm import Session
from app.company.companyService import company, upload_picture_to_s3
from app import deps
from models.models import CVitae, CompanyUser, UserEnum, Users
from models.models import Company as CompanyModel



companyRouter = APIRouter()
companyRouter.tags = ['Company']

@companyRouter.post("/company/", status_code=201, response_model=Company)
def create_company(
    *, company_in: CompanyCreate= Body(...), 
    ## picture: Optional[UploadFile] = File(None),
    db: Session = Depends(deps.get_db), userToken: UserToken = Depends(get_user_current)
) -> dict:
    """
    Create a new company in the database.
    """

    if userToken.role not in [UserEnum.super_admin, UserEnum.admin]:
        raise HTTPException(status_code=403, detail="No tiene los permisos para ejecutar este servicio")
    
    activeState = userToken.role == UserEnum.super_admin

    try:
        user = Users(
            fullname= company_in.responsible_user.fullname,
            email= company_in.responsible_user.email,
            password= get_password_hash('deeptalentUser'),
            phone= company_in.responsible_user.phone,
            role= 3
        )
        
        db.add(user)
        db.flush()

        ## picture_url = upload_picture_to_s3(picture)
        picture_url = 'aqui iria la url generada por s3'

        # konempleo_userId = company_in.konempleo_responsible 

        company_data = company_in.dict()
        # company_data.pop('konempleo_responsible', None)
        company_data.pop('responsible_user', None)
        company = CompanyModel(**company_data)

        company.picture = picture_url
        company.active = activeState
        db.add(company)
        db.flush()

        company_user = CompanyUser(
            companyId=company.id,
            userId=user.id
        )
        konempleo_user = CompanyUser(
            companyId=company.id,
            userId=konempleo_userId
        )
        db.add(company_user)
        db.add(konempleo_user)

        db.commit()
        db.refresh(company)

        return company

    except Exception as e:
        # If any operation fails, the transaction is rolled back automatically
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred while creating the company: {str(e)}")

@companyRouter.get("/company/owned/", status_code=200, response_model=List[CompanyWCount])
def get_company(
    *, db: Session = Depends(deps.get_db), userToken: UserToken = Depends(get_user_current)
) -> dict:
    """
    gets company in the database.
    """
    company_user_records = db.query(CompanyUser).filter(CompanyUser.userId == userToken.id).all()
    
    if not company_user_records:
        raise HTTPException(status_code=404, detail="No companies found for the given user ID.")
    
    company_ids = [record.companyId for record in company_user_records]

    # Query to get all companies and count of CVitae records for each company
    companies_with_cv_count = db.query(
        CompanyModel,
        func.count(CVitae.Id).label('cv_count')
    ).outerjoin(
        CVitae, CVitae.companyId == CompanyModel.id
    ).filter(
        CompanyModel.id.in_(company_ids)
    ).group_by(
        CompanyModel.id
    ).all()

    if not companies_with_cv_count:
        raise HTTPException(status_code=404, detail="No companies found.")
    
    # Format the response to include the company data along with the CV count
    result = []
    for company, cv_count in companies_with_cv_count:
        company_dict = company.__dict__.copy()
        company_dict['cv_count'] = cv_count
        result.append(company_dict)
    
    return result


@companyRouter.get("/company/all/", status_code=200, response_model=List[CompanyWCount])
def get_all_companies(
    *, db: Session = Depends(deps.get_db), userToken: UserToken = Depends(get_user_current)
) -> List[CompanyWCount]:
    """
    Gets all companies in the database if the user is a super admin.
    """
    if userToken.role != UserEnum.super_admin:
        raise HTTPException(status_code=403, detail="You do not have permission to view all companies.")

    # Query to get all companies and count of CVitae records for each company
    companies_with_cv_count = db.query(
        CompanyModel,
        func.count(CVitae.Id).label('cv_count')
    ).outerjoin(
        CVitae, CVitae.companyId == CompanyModel.id
    ).group_by(
        CompanyModel.id
    ).all()

    if not companies_with_cv_count:
        raise HTTPException(status_code=404, detail="No companies found.")
    
    # Format the response to include the company data along with the CV count
    result = []
    for company, cv_count in companies_with_cv_count:
        company_dict = company.__dict__.copy()
        company_dict['cv_count'] = cv_count
        result.append(CompanyWCount(**company_dict))
    
    return result

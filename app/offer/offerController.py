from typing import List
from fastapi import APIRouter, Depends, HTTPException
from requests import Session
from sqlalchemy import func

from app.auth.authDTO import UserToken
from app.auth.authService import get_user_current
from app.deps import get_db
from app.offer.offerDTO import Offer, OfferCreateDTO, OfferUpdateDTO, OfferWithVitaeCount
from models.models import Company, CompanyOffer, OfferSkill, Skill, UserEnum, VitaeOffer
from models.models import Offer as OfferModel

offerRouter = APIRouter()
offerRouter.tags = ['Offer']


@offerRouter.post("/offers/", response_model=Offer)
def create_offer(offer_in: OfferCreateDTO, skills: List[int], db: Session = Depends(get_db), userToken: UserToken = Depends(get_user_current)):
    """
    Create a new offer and associate it with the provided skills.
    """
    if userToken.role != UserEnum.company :
        raise HTTPException(status_code=403, detail="No tiene los permisos para ejecutar este servicio")
    
    offerCompanyId = offer_in.companyId
    company = db.query(Company).filter(Company.id == offerCompanyId).first()
    if not company:
        raise HTTPException(status_code=400, detail=f"Invalid company ID: {offer.companyId}")
    

    offer_data = offer_in.dict()
    offer_data.pop('companyId', None)
    offer = OfferModel(**offer_data)

    try:
        # Start creating the Offer
        new_offer = OfferModel(**offer.dict())
        db.add(new_offer)
        db.flush()  # Flush to get the new offer's ID

        # Now associate skills with the offer
        for skill_id in skills:
            # Check if the skill already exists
            skill = db.query(Skill).filter(Skill.id == skill_id).first()
            
            if not skill:
                raise HTTPException(status_code=400, detail=f"Invalid skill ID: {skill_id}")

            # Create the OfferSkill association
            offer_skill = OfferSkill(offerId=new_offer.id, skillId=skill.id)
            db.add(offer_skill)
            
        company_offer = CompanyOffer(offerId=new_offer.id, companyId=offerCompanyId)
        db.add(company_offer)
        # Commit the transaction to save everything to the DB
        db.commit()

        # Refresh to get the latest data of the new offer
        db.refresh(new_offer)

        return new_offer
    
    except HTTPException as e:
        # Re-raise the HTTPException for invalid skill ID
        raise e

    except Exception as e:
        # Rollback the transaction in case of any error
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred while creating the offer: {str(e)}")

@offerRouter.put("/offers/{offer_id}", response_model=Offer)
def update_offer(offer_id: int, offer: OfferUpdateDTO, db: Session = Depends(get_db), userToken: UserToken = Depends(get_user_current)):
    # Logic to update an offer
    pass

@offerRouter.get("/offers/company/details/{company_id}", response_model=List[OfferWithVitaeCount])
def get_offers_by_company(company_id: int, db: Session = Depends(get_db), userToken: UserToken = Depends(get_user_current)):
    """
    Get offers for a given company and count the number of associated VitaeOffer records for each offer.
    """

    if userToken.role not in [UserEnum.super_admin, UserEnum.company]:
        raise HTTPException(status_code=403, detail="No tiene los permisos para ejecutar este servicio")

    # Check if the company exists
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    # Query offers associated with the company and count associated VitaeOffer records
    offers_with_vitae_count = db.query(
        Offer, 
        func.count(VitaeOffer.id).label('vitae_offer_count')
    ).join(
        CompanyOffer, CompanyOffer.offerId == Offer.id
    ).outerjoin(
        VitaeOffer, VitaeOffer.offerId == Offer.id
    ).filter(
        CompanyOffer.companyId == company_id
    ).group_by(
        Offer.id
    ).all()

    # Format the response with the offer data and vitae_offer_count
    result = []
    for offer, vitae_offer_count in offers_with_vitae_count:
        offer_dict = offer.__dict__.copy()  # Convert the offer object to a dictionary
        offer_dict['vitae_offer_count'] = vitae_offer_count
        result.append(OfferWithVitaeCount(**offer_dict))
    
    return result

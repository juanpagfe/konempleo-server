from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.base_class import Base
from models.company import Company
from models.offer import Offer

class CompanyOffer(Base):
    __tablename__ = 'companyOffers'

    id = Column(Integer, primary_key=True)
    companyId = Column(Integer, ForeignKey('company.id'), nullable=False)
    offerId = Column(Integer, ForeignKey('offers.id'), nullable=False)

    company = relationship('Company', back_populates='company_offers')
    offer = relationship('Offer', back_populates='company_offers')
    Company.company_offers = relationship('CompanyOffer', back_populates='company')
    Offer.company_offers = relationship('CompanyOffer', back_populates='offer')
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.base_class import Base

class Company(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    sector = Column(String)
    KAM = Column(String)
    picture = Column(String)
    responsible = Column(String)
    responsibleMail = Column(String)
    activeoffers = Column(Integer)
    totaloffers = Column(Integer)

    company_users = relationship('CompanyUser', back_populates='company')
    company_offers = relationship('CompanyOffer', back_populates='company')
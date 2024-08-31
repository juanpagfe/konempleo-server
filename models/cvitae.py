from sqlalchemy import (
    Column, Integer, String, Boolean, Float
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CVitae(Base):
    __tablename__ = 'cvitae'

    Id = Column(Integer, primary_key=True)
    url = Column(String)
    size = Column(Float)
    extension = Column(String)
    active = Column(Boolean, default=True)
    candidate_dni = Column(String)
    candidate_dni_type = Column(String)
    candidate_name = Column(String)
    candidate_phone = Column(String)
    candidate_mail = Column(String)
    candidate_city = Column(String)
    background_check = Column(String)

    Vitae_offers = relationship('VitaeOffer', back_populates='Cvitae')
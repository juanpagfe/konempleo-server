from sqlalchemy import (
    Column, Integer, Enum, ForeignKey, Float, Text
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class VitaeOffer(Base):
    __tablename__ = 'vitaeOffer'

    id = Column(Integer, primary_key=True)
    cvitaeId = Column(Integer, ForeignKey('cvitae.Id'), nullable=False)
    offerId = Column(Integer, ForeignKey('offers.id'), nullable=False)
    status = Column(Enum('pending', 'accepted', 'rejected', name='status_enum'))
    ai_response = Column(Text)
    response_score = Column(Float)
    whatsapp_status = Column(Enum('sent', 'delivered', 'read', name='whatsapp_status_enum'))

    Cvitae = relationship('CVitae', back_populates='Vitae_offers')
    offer = relationship('Offer', back_populates='vitae_offers')
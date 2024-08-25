from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.base_class import Base

class OfferSkill(Base):
    __tablename__ = 'offerSkills'

    id = Column(Integer, primary_key=True)
    offerId = Column(Integer, ForeignKey('offers.id'), nullable=False)
    skillId = Column(Integer, ForeignKey('skills.id'), nullable=False)

    offer = relationship('Offer', back_populates='offer_skills')
    skill = relationship('Skill')
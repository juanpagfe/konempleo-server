from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.base_class import Base

class CargoSkill(Base):
    __tablename__ = 'cargoSkills'

    id = Column(Integer, primary_key=True)
    cargoId = Column(Integer, ForeignKey('cargo.id'), nullable=False)
    skillId = Column(Integer, ForeignKey('skills.id'), nullable=False)

    cargo = relationship('Cargo', back_populates='cargo_skills')
    skill = relationship('Skill')
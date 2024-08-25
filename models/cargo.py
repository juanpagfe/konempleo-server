from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.base_class import Base

class Cargo(Base):
    __tablename__ = 'cargo'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    cargo_skills = relationship('CargoSkill', back_populates='cargo')
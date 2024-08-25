from sqlalchemy import Column, Integer, String

from db.base_class import Base

class Skill(Base):
    __tablename__ = 'skills'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
from sqlalchemy import Boolean, Column, Integer, String

from db.base_class import Base

class Company(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    sector = Column(String)
    document = Column(String)
    document_type = Column(String)
    address = Column(String)
    picture = Column(String)
    activeoffers = Column(Integer)
    totaloffers = Column(Integer)
    employees = Column(Integer)
    city = Column(String)
    active = Column(Boolean, default=True)

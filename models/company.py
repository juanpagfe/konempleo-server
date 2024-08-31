from sqlalchemy import Boolean, Column, Integer, String, text
from sqlalchemy.orm import relationship

from db.base_class import Base

class Company(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    sector = Column(String)
    document = Column(String)
    document_type = Column(String)
    picture = Column(String)
    activeoffers = Column(Integer, server_default=text('0'))
    totaloffers = Column(Integer, server_default=text('0'))
    employees = Column(Integer, server_default=text('0'))
    city = Column(String)
    active = Column(Boolean, default=True)

    users = relationship("CompanyUser", back_populates="company")

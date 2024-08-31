from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from .user import Users
from .company import Company

from db.base_class import Base


class CompanyUser(Base):
    __tablename__ = 'companyUsers'

    id = Column(Integer, primary_key=True)
    companyId = Column(Integer, ForeignKey('company.id'), nullable=False)
    userId = Column(Integer, ForeignKey('users.id'), nullable=False)

    company = relationship('Company', back_populates='users')
    user = relationship("Users", back_populates="companies")
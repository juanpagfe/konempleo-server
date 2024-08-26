from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.base_class import Base
from models.company import Company
from models.user import Users


class CompanyUser(Base):
    __tablename__ = 'companyUsers'

    id = Column(Integer, primary_key=True)
    companyId = Column(Integer, ForeignKey('company.id'), nullable=False)
    userId = Column(Integer, ForeignKey('users.id'), nullable=False)

    company = relationship('Company', back_populates='company_users')
    user = relationship('Users', back_populates='companies_relationship')
    Users.companies_relationship = relationship('CompanyUser', back_populates='users')
    Company.company_users = relationship('CompanyUser', back_populates='company')
from sqlalchemy import TIMESTAMP, Boolean, Column, Enum, Integer, String
from sqlalchemy.orm import relationship

from db.base_class import Base

class UserEnum(Enum):
    super_admin = 1
    admin = 2
    company = 3

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    role = Column(Enum(UserEnum), nullable=False)
    active = Column(Boolean, default=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

    companies_relationship = relationship('CompanyUser', back_populates='user')

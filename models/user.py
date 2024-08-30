from enum import IntEnum
from sqlalchemy import TIMESTAMP, Boolean, Column, Enum, Integer, String, func

from db.base_class import Base

class UserEnum(IntEnum):
    super_admin = 1
    admin = 2
    company = 3

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    fullname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    role = Column(Enum(UserEnum), nullable=False)
    active = Column(Boolean, default=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    must_change_password = Column(Boolean, default=True)

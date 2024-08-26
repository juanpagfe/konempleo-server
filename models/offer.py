from enum import IntEnum
from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.base_class import Base

class contractEnum(IntEnum):
    full_time = 1
    part_time = 2

class shiftEnum(IntEnum):
    morning = 1
    evening = 2
    night = 3

class genderEnum(IntEnum):
    male = 1
    female = 2
    other = 3

class militaryEnum(IntEnum):
    yes = 1
    no = 2
    NA = 3

class licenseEnum(IntEnum):
    required = 1
    not_required = 2

class educationEnum(IntEnum):
    none = 1
    high_school = 2
    bachelor = 3
    master = 4
    doctorate = 5



class Offer(Base):
    __tablename__ = 'offers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    duties = Column(String)
    exp_area = Column(String)
    vacants = Column(Integer)
    contract_type = Column(Enum(contractEnum))
    salary = Column(String)
    city = Column(Integer)
    shift = Column(Enum(shiftEnum))
    gender = Column(Enum(genderEnum))
    military_notebook = Column(Enum(militaryEnum))
    age = Column(String)
    job_type = Column(String)
    license = Column(Enum(licenseEnum))
    disabled = Column(Boolean, default=False)
    experience_years = Column(Integer)
    offer_type = Column(String)
    ed_required = Column(Enum(educationEnum))
    cargoId = Column(Integer, ForeignKey('cargo.id'))

    company_offers = relationship('CompanyOffer', back_populates='offer')
    offer_skills = relationship('OfferSkill', back_populates='offer')
    vitae_offers = relationship('VitaeOffer', back_populates='offer')
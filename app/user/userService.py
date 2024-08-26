
import csv
import inspect
from pathlib import Path
import random
from typing import Optional
from fastapi import HTTPException
from app.auth.authService import get_password_hash
from app.baseController import ControllerBase
from app.user.userDTO import UserEnrollInsert, UserInDBBase, UserInsert, UserSoftDelete, UserUpdateUser, UserWithResult
from models.companyUser import CompanyUser
from models.user import Users
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

import pandas as pd

class ServiceUser(ControllerBase[Users, UserInsert, UserUpdateUser, UserSoftDelete]): 
    ...

user = ServiceUser(Users)

def insertEnroll( db: Session, *, obj_in: UserEnrollInsert) -> None:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = Company_Enroll(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

def createUser(db: Session, *, obj_in: UserInsert, company: int) -> UserWithResult:
    try:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['password'] = get_password_hash(obj_in_data['password'])
        db_obj = Users(**obj_in_data)
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        encodedUser = jsonable_encoder(db_obj)
        enroll_in_data = jsonable_encoder(UserEnrollInsert(**{ 'user_id':encodedUser.get('id'), 'company_id':company}))
        enroll_obj = CompanyUser(**enroll_in_data)
        db.add(enroll_obj)
        db.commit()
        return UserWithResult(**{'user':UserInDBBase(**encodedUser), 'result_id':db_obj.id})
    except():
        db.rollback()
        raise HTTPException(status_code=400, detail="Error inserting new user")
    
def createAdmin(db: Session, *, obj_in: UserInsert, company: int) -> Users:
    try:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['password'] = get_password_hash(obj_in_data['password'])
        db_obj = Users(**obj_in_data)
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        encodedUser = jsonable_encoder(db_obj)
        enroll_in_data = jsonable_encoder(UserEnrollInsert(**{ 'user_id':encodedUser.get('id'), 'company_id':company}))
        enroll_obj = CompanyUser(**enroll_in_data)
        db.add(enroll_obj)
        db.commit()
        return encodedUser
    except():
        db.rollback()
        raise HTTPException(status_code=400, detail="Error inserting new user")

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

def get_num_lines(fname):
    with open(fname) as f:
        for i, _ in enumerate(f):
            pass
    return i + 1

def get_num_lines_speaking(fname):
    with open(fname) as f:
        rdr = csv.reader(f)
        for i, _ in enumerate(rdr):
            pass
    return i + 1

def get_random_question_listening(file, sample):
    path = Path(__file__).resolve().parent.parent/file
    num_lines = get_num_lines(path)
    rows_to_skip = random.sample(range(num_lines), num_lines-sample)
    return pd.read_csv(path, skiprows=rows_to_skip, header=None)

def get_random_question(file, sample):
    path = Path(__file__).resolve().parent.parent/file
    num_lines_speaking = get_num_lines_speaking(path)
    rows_to_skip = random.sample(range(num_lines_speaking), num_lines_speaking-sample)
    questions = pd.read_csv(path, skiprows=rows_to_skip, header=None)
    return questions

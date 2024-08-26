from fastapi import APIRouter, Depends, HTTPException
from app.user.userService import createAdmin, createUser, get_random_question, get_random_question_listening
from app.user.userDTO import UserCreate, UserInsert, UserWithResult
from sqlalchemy.orm import Session
from app.company.companyService import getByName
from app import deps


userRouter = APIRouter()
userRouter.tags = ['User']

@userRouter.post("/user/", status_code=201, response_model=None)
def create_user(
    *, user_in: UserCreate, db: Session = Depends(deps.get_db)
) -> dict:
    
    """
    Create a new user in the database.
    """  
    userDict = dict(user_in)
    companyUid = userDict.pop('company_uid')
    companyExist = getByName(db=db, uid=companyUid)
    if companyExist == None:
         raise HTTPException(status_code=404, detail="No company with given company")
    userInsertObject = UserInsert.model_validate(userDict)

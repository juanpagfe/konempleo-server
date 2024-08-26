from fastapi import APIRouter, Depends, HTTPException
from app.auth.authDTO import UserToken
from app.auth.authService import get_user_current
from app.user.userDTO import UserInsert
from sqlalchemy.orm import Session
from app.company.companyService import getByName
from app import deps
from models.user import UserEnum


userRouter = APIRouter()
userRouter.tags = ['User']

@userRouter.post("/user/", status_code=201, response_model=None)
def create_user(
    *, user_in: UserInsert, db: Session = Depends(deps.get_db), userToken: UserToken = Depends(get_user_current)
) -> dict:
    
    """
    Create a new user in the database.
    """  
    if userToken.role == UserEnum.super_admin :
        raise HTTPException(status_code=404, detail="the role is right!!")
    userDict = {}
    return userDict


import os
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.auth.authDTO import Token
from app.auth.authService import generate_token
from app import deps


authRouter = APIRouter()
authRouter.tags = ['Auth']

@authRouter.post("/login")
def login_for_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(deps.get_db)):
    access_token = generate_token(db=db, username=form_data.username, password=form_data.password)
    return Token(access_token = access_token, token_type="bearer")

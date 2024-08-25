import os
from fastapi import APIRouter, Depends, HTTPException
from app.resultsWriting.resultsWritingService import create_result_writing
from app.resultsSpeaking.resultsSpeakingService import create_result_speaking
from app.resultsListening.resultsListeningService import create_result_listening
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
    if userInsertObject.usertype == 3:
        userCreated = createUser(db=db, obj_in=userInsertObject, company=companyExist.id)
        listeningQuestions = get_random_question_listening('resources/results_listening.csv', 3)
        speakingQuestions = get_random_question('resources/results_speaking.csv', 1)
        writingQuestions = get_random_question('resources/results_writing.csv', 1)
        create_result_listening(db=db, obj_in=listeningQuestions, result_id=userCreated.result_id)
        create_result_speaking(db=db, obj_in=speakingQuestions, result_id=userCreated.result_id)
        create_result_writing(db=db, obj_in=writingQuestions, result_id=userCreated.result_id)
    else :
        userCreated = createAdmin(db=db, obj_in=userInsertObject, company=companyExist.id)

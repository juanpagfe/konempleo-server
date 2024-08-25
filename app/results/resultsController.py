from fastapi import APIRouter, Depends, HTTPException
from app.auth.authDTO import UserToken
from app.auth.authService import get_user_current
from app.user.userService import user
from app.results.resultsDTO import ResultCreate, Result, ResultFeedbackUpdate
from sqlalchemy.orm import Session
from app.company.companyService import company
from app.results.resultsService import getByUser, getCompanyResults, result, update_result_feedback
from app import deps


resultsRouter = APIRouter()
resultsRouter.tags = ['Results']

@resultsRouter.post("/results/", status_code=201, response_model=Result)
def create_result(
    *, result_in: ResultCreate, db: Session = Depends(deps.get_db)
) -> dict:
    
    """
    Create a new result in the database.
    """
    userExist = user.get(db=db, id=result_in.users_id)
    if userExist == None:
        raise HTTPException(status_code=404, detail="No user with given id: "+str(result_in.users_id))
    userResult = result.create(db=db, obj_in=result_in)

    return userResult

@resultsRouter.get("/results/{result_id}", status_code=200, response_model=Result)
def get_result(
    *, db: Session = Depends(deps.get_db), result_id
) -> dict:
    """
    gets results in the database.
    """
    currentResult = result.get(db=db, id=result_id)
    if currentResult == None:
        raise HTTPException(status_code=404, detail="No result with given id: "+result_id)

    return currentResult

@resultsRouter.put("/results/feedback/", status_code=200, response_model=None)
def result_feedback(
    *, result_in: ResultFeedbackUpdate, db: Session = Depends(deps.get_db)
) -> dict:
    """
    gets results in the database.
    """
    currentResult = result.get(db=db, id= result_in.id)
    if currentResult == None:
        raise HTTPException(status_code=404, detail="No result with given id: "+ result_in.id)

    update_result_feedback(db=db, db_obj=currentResult, obj_in=result_in)

@resultsRouter.get("/user_results/{user_id}", status_code=200, response_model=Result)
def get_user_result(
    *, db: Session = Depends(deps.get_db), user_id
) -> dict:
    """
    gets results by user in the database.
    """
    currentResult = getByUser(db=db, user_id=user_id)
    if currentResult == None:
        raise HTTPException(status_code=404, detail="No result for given user id: "+user_id)

    return currentResult

@resultsRouter.get("/company_results/", status_code=200, response_model= None)
def get_company_results(
    db: Session = Depends(deps.get_db), userToken: UserToken = Depends(get_user_current)
) -> dict:
    """
    gets results by user in the database.
    """
    currentCompany = company.get(db=db, id=userToken.company)
    if currentCompany == None:
        raise HTTPException(status_code=404, detail="No company with the given company")
    results = getCompanyResults(db= db, company_id=userToken.company)

    return results
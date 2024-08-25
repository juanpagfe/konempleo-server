from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime

from fastapi.encoders import jsonable_encoder
from models.resultsListening import Results_listening
from app.resultsListening.resultsListeningDTO import Results_listeningUpdate, ResultsListeningResponse
from app.resultsListening.resultsListeningService import get_results_listening, resultListening
from app.results.resultsService import result, updateResultScores
from sqlalchemy.orm import Session
from app import deps


resultsListeningRouter = APIRouter()
resultsListeningRouter.tags = ['Results Listening']

@resultsListeningRouter.put("/results/listening/", status_code=200, response_model=None)
def update_listening_result(
    *, results_listening: Results_listeningUpdate, db: Session = Depends(deps.get_db)
) -> dict:
    """
    Updates a listening result in the database.
    """
    resultL2Update = resultListening.get(db=db, id=results_listening.id)
    if resultL2Update == None:
        raise HTTPException(status_code=404, detail="No record with given id: " + str(results_listening.id))
    if resultL2Update.updated_at != None:
        raise HTTPException(status_code=404, detail="This record has already been answered")
    resultL2Update.given_answer = resultL2Update.question[0]+ '. ' +results_listening.given_answer
    resultL2Update.updated_at = datetime.now()
    if resultL2Update.correct_answer == results_listening.given_answer:
        resultL2Update.score = 5
        resultL2Update.evaluation = 'Right'
    else:
        resultL2Update.score = 0
        resultL2Update.evaluation = 'Wrong'
    db.add(resultL2Update)
    updateResultScores(db=db, result_type='Listening', result_id=resultL2Update.results_id)
    db.commit()
    db.refresh(resultL2Update)

    return resultL2Update

@resultsListeningRouter.get("/results/listening/{result_id}", status_code=200, response_model= Optional[List[ResultsListeningResponse]])
def get_listening_results(
    *, db: Session = Depends(deps.get_db), result_id
) -> dict:
    """
    gets listening results in the database for the given result id.
    """
    currentResult = get_results_listening(db=db, results_id=result_id)
    if currentResult == None:
        raise HTTPException(status_code=404, detail="No results for given result_id: "+result_id)

    return currentResult
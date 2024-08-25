from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from app.results.resultsService import updateResultScores
from app.resultsWriting.resultsWritingDTO import Results_writingUpdate, ResultsWriting
from app.resultsWriting.resultsWritingService import get_results_writing, resultWriting
from app.resultsSpeaking.resultsSpeakingService import get_transcription_from_audio, set_calification
from sqlalchemy.orm import Session
from app import deps


resultsWritingRouter = APIRouter()
resultsWritingRouter.tags = ['Results Writing']

@resultsWritingRouter.put("/results/writing/", status_code=200, response_model=None)
async def update_writing_result(
    *, results_writing: Results_writingUpdate, db: Session = Depends(deps.get_db)
) -> dict:
    """
    Updates a writing result in the database.
    """
    resultW2Update = resultWriting.get(db=db, id=results_writing.id)
    if resultW2Update == None:
        raise HTTPException(status_code=404, detail="No record with given id: " + str(results_writing.id))
    ai_evaluation = await set_calification(resultW2Update.question, results_writing.answer)
    resultW2Update.answer = resultW2Update.question[0] + '. ' + results_writing.answer
    resultW2Update.updated_at = datetime.now()
    resultW2Update.score = ai_evaluation['score']
    resultW2Update.evaluation = ai_evaluation['feedback']
    db.add(resultW2Update)
    updateResultScores(db=db, result_type='Writing', result_id=resultW2Update.results_id)
    db.commit()
    db.refresh(resultW2Update)

    return resultW2Update

@resultsWritingRouter.get("/results/writing/{result_id}", status_code=200, response_model= Optional[List[ResultsWriting]])
def get_writing_results(
    *, db: Session = Depends(deps.get_db), result_id
) -> dict:
    """
    gets writing results in the database for the given result id.
    """
    currentResult = get_results_writing(db=db, results_id=result_id)
    if currentResult == None:
        raise HTTPException(status_code=404, detail="No results for given result_id: "+result_id)

    return currentResult
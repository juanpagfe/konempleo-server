from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from app.results.resultsService import updateResultScores
from app.resultsSpeaking.resultsSpeakingService import get_results_speaking, get_transcription_from_audio, set_calification
from app.resultsSpeaking.resultsSpeakingDTO import Results_speakingUpdate, ResultsSpeaking
from app.resultsSpeaking.resultsSpeakingService import resultSpeaking
from sqlalchemy.orm import Session
from app import deps


resultsSpeakingRouter = APIRouter()
resultsSpeakingRouter.tags = ['Results Speaking']

@resultsSpeakingRouter.put("/results/speaking/", status_code=200, response_model=None)
async def update_speaking_result(
    *, results_speaking: Results_speakingUpdate, db: Session = Depends(deps.get_db)
) -> dict:
    """
    Updates a speaking result in the database.
    """
    resultS2Update = resultSpeaking.get(db=db, id=results_speaking.id)
    if resultS2Update == None:
        raise HTTPException(status_code=404, detail="No record with given id: " + str(results_speaking.id))
    audio_transcript = await get_transcription_from_audio(results_speaking.answer_audio)
    ai_evaluation = await set_calification(resultS2Update.question, audio_transcript)
    resultS2Update.answer_audio = results_speaking.answer_audio
    resultS2Update.answer = audio_transcript
    resultS2Update.updated_at = datetime.now()
    resultS2Update.score = ai_evaluation['score']
    resultS2Update.evaluation = ai_evaluation['feedback']
    db.add(resultS2Update)
    updateResultScores(db=db, result_type='Speaking', result_id=resultS2Update.results_id)
    db.commit()
    db.refresh(resultS2Update)

    return resultS2Update


@resultsSpeakingRouter.get("/results/speaking/{result_id}", status_code=200, response_model= Optional[List[ResultsSpeaking]])
def get_speaking_results(
    *, db: Session = Depends(deps.get_db), result_id
) -> dict:
    """
    gets speaking results in the database for the given result id.
    """
    currentResult = get_results_speaking(db=db, results_id=result_id)
    if currentResult == None:
        raise HTTPException(status_code=404, detail="No results for given result_id: "+result_id)

    return currentResult
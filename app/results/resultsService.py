
from fastapi.encoders import jsonable_encoder
from app.resultsListening.resultsListeningService import get_results_listening
from app.resultsSpeaking.resultsSpeakingService import get_results_speaking
from app.resultsWriting.resultsWritingService import get_results_writing
from app.baseController import ControllerBase
from app.results.resultsDTO import ResultCreate, ResultFeedbackUpdate, ResultUpdate
from models.results import Results
from sqlalchemy.orm import Session
from typing import Optional, Union, Dict, Any
from sqlalchemy import text 


class ServiceResults(ControllerBase[Results, ResultCreate, ResultUpdate, None]): 
    ...

result = ServiceResults(Results)

def getByUser(db: Session, user_id: int) -> Optional[Results]:
        return db.query(Results).filter(Results.users_id == user_id).first()

def update_result_feedback(
        db: Session,
        db_obj: Results,
        obj_in: Union[ResultFeedbackUpdate, Dict[str, Any]]
    ) -> Results:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])     
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

def getCompanyResults(db: Session, company_id: int) -> Optional[None]:
        statement = text('SELECT results.id as results_id, users.created_at, users.first_name, users.last_name, users.dni, '+
                        'users.email, users.city, users.phone,results.english_level, results.result_score, results.score_listening, '+ 
                        'results.score_writing,results.score_speaking,results.feedback FROM users '+
                        'LEFT JOIN results ON users.id = results.users_id '+
                        'LEFT JOIN company_enroll as enroll ON users.id = enroll.user_id '+
                        'WHERE enroll.company_id = :companyParam '+
                        "AND users.usertype= :usertype "
                        'GROUP BY results.id, users.id, results.english_level, results.result_score, results.score_listening, '+
                        'results.score_writing, results.score_speaking,results.feedback ORDER BY results.result_score DESC')
        results= db.execute(statement, {'companyParam':int(company_id), 'usertype':'USER'})
        results_dict = results.mappings().all()
        return results_dict

def updateResultScores(db: Session, result_type: str, result_id: int) -> None:
    result2Update = result.get(db= db, id=result_id)
    if result_type == 'Listening':
        listeningResults = get_results_listening(db=db, results_id=result_id)
        listening_score = 0
        for listeningResult in listeningResults:
            listening_score = listening_score + listeningResult.score
        result2Update.score_listening = listening_score/len(listeningResults)
    if result_type == 'Speaking':
        speakingResults = get_results_speaking(db=db, results_id=result_id)
        speaking_score = 0
        for speakingResult in speakingResults:
            speaking_score = speaking_score + speakingResult.score
        result2Update.score_speaking = speaking_score/len(speakingResults)
    if result_type == 'Writing':
        writingResults = get_results_writing(db=db, results_id=result_id)
        writing_score = 0
        for writingResult in writingResults:
            writing_score = writing_score + writingResult.score
        result2Update.score_writing = writing_score/len(writingResults)
    result2Update.result_score = (result2Update.score_listening*0.3) + (result2Update.score_writing*0.3) + (result2Update.score_speaking*0.4)
    result2Update.english_level = set_english_level(result2Update.result_score)
    db.add(result2Update)


def set_english_level(score: float) -> str:
    if(score <= 3):
        return 'A1'
    elif(score <= 3.25):
        return 'A2'
    elif(score <= 3.5):
        return 'B1'    
    elif(score <= 3.75):
        return 'B2'   
    elif(score <= 4.25):
        return 'C1' 
    else:
        return 'C2'
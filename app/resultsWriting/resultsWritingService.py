
from typing import Optional
from pandas import DataFrame
from sqlalchemy import insert
from app.resultsSpeaking.resultsSpeakingDTO import ResultsSpeaking
from app.resultsWriting.resultsWritingDTO import Results_writingCreate, Results_writingUpdate
from models.resultsWriting import Results_writing
from app.baseController import ControllerBase
from sqlalchemy.orm import Session


class ServiceResultsWriting(ControllerBase[Results_writing, Results_writingCreate, Results_writingUpdate, None]): 
    ...

resultWriting = ServiceResultsWriting(Results_writing)

def create_result_writing( db: Session, *, obj_in: DataFrame, result_id: int)-> None:
    questions = []
    for index in range(len(obj_in.iloc[0])):
        question = Results_writingCreate(**{
            'results_id':result_id,
            'question': str(index+1) + '. ' + obj_in.iloc[0,index]
            })
        questions.append(question)
    questions.append(Results_writingCreate(**{
            'results_id':result_id,
            'question': "3. Answer the following client request: Hello, this is Adam. I have an appointment scheduled for next week, but I need to reschedule. Could I please review the doctor's available slots again? I appreciate your help. Thank you."
            }))
    db.execute(insert(Results_writing),questions)
    db.commit()

def get_results_writing(db: Session, results_id: int) -> Optional[ResultsSpeaking]:
        return db.query(Results_writing).filter(Results_writing.results_id == results_id).all()    
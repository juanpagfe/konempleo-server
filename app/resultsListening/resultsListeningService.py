from fastapi.encoders import jsonable_encoder
from pandas import DataFrame
from sqlalchemy import insert
from app.resultsListening.resultsListeningDTO import Results_listeningCreate, Results_listeningUpdate, ResultsListening
from models.resultsListening import Results_listening
from app.baseController import ControllerBase
from sqlalchemy.orm import Session
from typing import Optional


class ServiceResultsListening(ControllerBase[Results_listening, Results_listeningCreate, Results_listeningUpdate, None]): 
    ...

resultListening = ServiceResultsListening(Results_listening)

def create_result_listening( db: Session, *, obj_in: DataFrame, result_id: int)-> None:
    questions = []
    for index in range(len(obj_in)):
        question = Results_listeningCreate(**{
            'results_id':result_id,
            'question': str(index+1) + '. ' + obj_in.iloc[index,0],
            'answer1': obj_in.iloc[index,1],
            'answer2': obj_in.iloc[index,2],
            'answer3': obj_in.iloc[index,3],
            'correct_answer': obj_in.iloc[index,4],
            'audio_name': obj_in.iloc[index,5].replace('.txt','')
            })
        questions.append(question)
    db.execute(insert(Results_listening),questions)
    db.commit()

def get_results_listening(db: Session, results_id: int) -> Optional[ResultsListening]:
        return db.query(Results_listening).filter(Results_listening.results_id == results_id).all()    
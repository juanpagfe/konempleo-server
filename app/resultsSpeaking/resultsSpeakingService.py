import asyncio
import json
import os
from typing import Optional
from deepgram import Deepgram
import openai
from pandas import DataFrame
from sqlalchemy import insert
from app.resultsSpeaking.resultsSpeakingDTO import Results_speakingCreate, Results_speakingUpdate, ResultsSpeaking
from models.resultsSpeaking import Results_speaking
from app.baseController import ControllerBase
from sqlalchemy.orm import Session


class ServiceResultsSpeaking(ControllerBase[Results_speaking, Results_speakingCreate, Results_speakingUpdate, None]): 
    ...

resultSpeaking = ServiceResultsSpeaking(Results_speaking)

def get_results_speaking(db: Session, results_id: int) -> Optional[ResultsSpeaking]:
        return db.query(Results_speaking).filter(Results_speaking.results_id == results_id).all()    

def create_result_speaking( db: Session, *, obj_in: DataFrame, result_id: int)-> None:
    questions = []
    for index in range(len(obj_in.iloc[0])):
        question = Results_speakingCreate(**{
            'results_id':result_id,
            'question': str(index+1) + '. ' + obj_in.iloc[0,index].replace('\n', ' ').replace('\r', '')
            })
        questions.append(question)
    db.execute(insert(Results_speaking),questions)
    db.commit()

async def get_transcription_from_audio(audio_url):
    deepgram = Deepgram(os.getenv('DG_KEY'))
    source = {
      'url': audio_url
    }
    response = await asyncio.create_task(
        deepgram.transcription.prerecorded(
            source,
            {
                'smart_format': True,
                'model': 'nova-2',
                'detect_language': False,
                'language': 'en'
            }
        )
    )
    
    return response['results']['channels'][0]['alternatives'][0]['transcript']

async def set_calification(question, answer):
    
    client = openai.AsyncOpenAI(
        api_key=os.getenv('OPENAI_KEY'),
    )
    prompt_questions = f'''Assume the role of a native English teacher and evaluate the response to the question "{question}" with the answer "{answer}". Please rate the answer strictly on a scale of 1 to 5, with 1 representing poor quality and 5 representing excellent quality. Consider factors such as grammar, vocabulary, fluency, and clarity in expressing ideas.
                        Please present your evaluation in a JSON object with two values: score and feedback.
                        '''
    response = await client.chat.completions.create(
         messages=[
            {
                "role": "user",
                "content": prompt_questions
            }
        ],
        model=os.getenv('OPENAI_MODEL'),
        temperature=0.2
    )
    res = response.choices[0].message.content
    format_res = json.loads(res)
    return format_res
    
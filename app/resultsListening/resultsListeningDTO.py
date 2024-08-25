from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Extra

class Results_listeningBase(BaseModel):
    results_id: int
    answer1: str
    answer2: str
    answer3: str
    question: str
    correct_answer: str
    given_answer: str
    audio_name: str
    evaluation: str
    score: float
    created_at: datetime
    updated_at: datetime

class Results_listeningBaseResponse(BaseModel):
    id: int
    results_id: int
    answer1: str
    answer2: str
    answer3: str
    question: str
    given_answer: Optional[str] = None
    audio_name: str
    evaluation: Optional[str] = None
    score: float
    created_at: datetime
    updated_at: Optional[datetime] = None

class Results_listeningCreate(BaseModel):
    results_id: int
    answer1: str
    answer2: str
    answer3: str
    question: str
    correct_answer: str
    audio_name: str

class Results_listeningUpdate(BaseModel,extra = Extra.forbid):
    id: int
    given_answer: str

class Results_listeningEvaluation(Results_listeningUpdate,extra = Extra.forbid):
    updated_at: datetime
    score: float

# Properties shared by models stored in DB
class ResultsListeningInDBBase(Results_listeningBase):
    id: int

    class Config:
        orm_mode: True

# Properties to return to client
class ResultsListening(Results_listeningBase):
    pass

# Properties to return to client
class ResultsListeningResponse(Results_listeningBaseResponse):
    pass

# Properties properties stored in DB
class ResultsListeningInDB(Results_listeningBase):
    pass
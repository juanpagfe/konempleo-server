from datetime import datetime
from enum import IntEnum
from typing import Optional
from pydantic import BaseModel, Extra

class FeedbackEnum(IntEnum):
    UNDER = 1
    FAIR = 2
    OVER = 3

class Results_speakingBase(BaseModel):
    id: int
    results_id: int
    answer: Optional[str] = None
    question: str
    answer_audio: Optional[str] = None
    evaluation: Optional[str] = None
    score: float
    created_at: datetime
    updated_at: Optional[datetime] = None

class Results_speakingCreate(BaseModel):
    results_id: int
    question: str

class Results_speakingUpdate(BaseModel,extra = Extra.forbid):
    id: int
    answer_audio: str

# Properties shared by models stored in DB
class ResultsSpeakingInDBBase(Results_speakingBase):
    id: int

    class Config:
        orm_mode: True

# Properties to return to client
class ResultsSpeaking(Results_speakingBase):
    pass

# Properties properties stored in DB
class ResultsSpeakingInDB(Results_speakingBase):
    pass
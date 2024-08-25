from datetime import datetime
from enum import IntEnum
from typing import Optional
from pydantic import BaseModel, Extra

class FeedbackEnum(IntEnum):
    UNDER = 1
    FAIR = 2
    OVER = 3

class Results_writingBase(BaseModel):
    id: int
    results_id: int
    answer: Optional[str] = None
    question: str
    evaluation: Optional[str] = None
    score: float
    created_at: datetime
    updated_at: Optional[datetime] = None

class Results_writingCreate(BaseModel):
    results_id: int
    question: str

class Results_writingUpdate(BaseModel,extra = Extra.forbid):
    id: int
    answer: str

# Properties shared by models stored in DB
class ResultsWritingInDBBase(Results_writingBase):
    id: int

    class Config:
        orm_mode: True

# Properties to return to client
class ResultsWriting(Results_writingBase):
    pass

# Properties properties stored in DB
class ResultsWritingInDB(Results_writingBase):
    pass
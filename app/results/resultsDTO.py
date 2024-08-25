from datetime import datetime
from typing import Optional
from enum import IntEnum
from pydantic import BaseModel, Extra

class FeedbackEnum(IntEnum):
    UNDER = 1
    FAIR = 2
    OVER = 3

class ResultBase(BaseModel):
    users_id: int
    english_level: str
    result_score: float
    score_writing: float
    score_speaking: float
    score_listening: float
    completed: bool
    feedback: Optional[FeedbackEnum] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: datetime

class ResultCreate(BaseModel):
    users_id: int

class ResultUpdate(BaseModel,extra = Extra.forbid):
    id: int
    english_level: Optional[str] = None
    result_score: Optional[float] = None
    score_writing: Optional[float] = None
    score_speaking: Optional[float] = None
    score_listening: Optional[float] = None

class ResultFeedbackUpdate(BaseModel):
    id: int
    feedback: FeedbackEnum

# Properties shared by models stored in DB
class ResultInDBBase(ResultBase):
    id: int

    class Config:
        orm_mode: True

# Properties to return to client
class Result(ResultInDBBase):
    pass

# Properties properties stored in DB
class ResultInDB(ResultInDBBase):
    pass
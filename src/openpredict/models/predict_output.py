from typing import List, Optional

from pydantic import BaseModel


class PredictHit(BaseModel):
    id: str
    type: str
    score: float
    label: Optional[str]


class PredictOutput(BaseModel):
    hits: List[PredictHit]
    count: int
    input: str


class TrapiRelation(BaseModel):
    subject: str
    predicate: str
    object: str
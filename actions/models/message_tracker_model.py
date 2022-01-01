from pydantic import BaseModel, Field
from typing import List, Literal, Optional


class Entity(BaseModel):
    type: str = Field(None, alias="entity")
    start: int
    end: int
    confidence_entity: Optional[float]
    value: str
    extractor: Optional[str]
    processors: Optional[List[str]]


class Intent(BaseModel):
    id: Optional[int]
    name: str
    confidence: float


class MessageTracker(BaseModel):
    text: str
    intent: Intent
    entities: List[Entity]
    intent_ranking: Optional[List[Intent]]

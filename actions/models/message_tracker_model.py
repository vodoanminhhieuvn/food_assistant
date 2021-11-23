from pydantic import BaseModel, Field
from typing import List, Literal, Optional


class Entity(BaseModel):
    type: str = Field(None, alias="entity")
    start: int
    end: int
    confidence_entity: float
    value: str
    extractor: str
    processors: Optional[List[str]]


class Intent(BaseModel):
    id_: int = Field(..., alias="id")
    name: str
    confidence: float


class MessageTracker(BaseModel):
    text: str
    intent: Intent
    entities: List[Entity]
    intent_ranking: List[Intent]

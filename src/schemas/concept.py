import uuid
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from schemas.example import ExampleRead


class ConceptBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    card_id: uuid.UUID
    language_id: uuid.UUID
    concept: str
    explanation: str


class ConceptCreate(ConceptBase):
    examples: List[str] = []


class ConceptUpdate(BaseModel):
    card_id: Optional[uuid.UUID] = None
    language_id: Optional[uuid.UUID] = None
    concept: Optional[str] = None
    explanation: Optional[str] = None


class ConceptRead(ConceptBase):
    id: uuid.UUID
    user_id: uuid.UUID
    examples: List[ExampleRead] = []

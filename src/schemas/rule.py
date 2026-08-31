import uuid
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from schemas.example import ExampleRead


class RuleBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    card_id: uuid.UUID
    language_id: uuid.UUID
    rule: str
    explanation: str


class RuleCreate(RuleBase):
    examples: List[str] = []


class RuleUpdate(BaseModel):
    card_id: Optional[uuid.UUID] = None
    language_id: Optional[uuid.UUID] = None
    rule: Optional[str] = None
    explanation: Optional[str] = None


class RuleRead(RuleBase):
    id: uuid.UUID
    user_id: uuid.UUID
    examples: List[ExampleRead] = []

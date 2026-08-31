import uuid
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from models.card import CardType
from schemas.concept import ConceptRead
from schemas.rule import RuleRead
from schemas.tag import TagRead


class CardBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    deck_id: uuid.UUID
    card_type: CardType


class CardCreate(CardBase):
    tag_ids: List[uuid.UUID] = []


class CardUpdate(BaseModel):
    deck_id: Optional[uuid.UUID] = None
    card_type: Optional[CardType] = None


class CardRead(CardBase):
    id: uuid.UUID
    user_id: uuid.UUID
    tags: List[TagRead] = []
    concepts: List[ConceptRead] = []
    rules: List[RuleRead] = []


class CardAddTags(BaseModel):
    tag_ids: List[uuid.UUID]

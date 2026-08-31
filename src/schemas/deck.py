import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DeckBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str


class DeckCreate(DeckBase):
    pass


class DeckUpdate(BaseModel):
    name: Optional[str] = None


class DeckRead(DeckBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime

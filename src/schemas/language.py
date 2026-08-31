import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class LanguageBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    code: str


class LanguageCreate(LanguageBase):
    started_at: Optional[datetime] = None


class LanguageUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None


class LanguageRead(LanguageBase):
    id: uuid.UUID
    user_id: uuid.UUID

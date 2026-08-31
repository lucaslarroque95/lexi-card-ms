import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TagBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    key: str
    value: str


class TagCreate(TagBase):
    pass


class TagUpdate(BaseModel):
    key: Optional[str] = None
    value: Optional[str] = None


class TagRead(TagBase):
    id: uuid.UUID
    user_id: uuid.UUID

import uuid
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class ExampleBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    example: str


class ExampleCreate(ExampleBase):
    concept_id: Optional[uuid.UUID] = None
    rule_id: Optional[uuid.UUID] = None


class ExampleUpdate(BaseModel):
    example: Optional[str] = None


class ExampleRead(ExampleBase):
    id: uuid.UUID
    concept_id: Optional[uuid.UUID] = None
    rule_id: Optional[uuid.UUID] = None


class ExamplesAdd(BaseModel):
    examples: List[str]

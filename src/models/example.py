import uuid
from dataclasses import dataclass
from typing import Optional


@dataclass
class Example:
    example: str
    concept_id: Optional[uuid.UUID] = None
    rule_id: Optional[uuid.UUID] = None
    id: Optional[uuid.UUID] = None

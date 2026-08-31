import uuid
from dataclasses import dataclass
from typing import Optional


@dataclass
class Rule:
    user_id: uuid.UUID
    card_id: uuid.UUID
    language_id: uuid.UUID
    rule: str
    explanation: str
    id: Optional[uuid.UUID] = None

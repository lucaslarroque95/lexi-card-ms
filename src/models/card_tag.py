import uuid
from dataclasses import dataclass
from typing import Optional


@dataclass
class CardTag:
    user_id: uuid.UUID
    card_id: uuid.UUID
    tag_id: uuid.UUID
    id: Optional[uuid.UUID] = None

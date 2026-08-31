import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Deck:
    user_id: uuid.UUID
    name: str
    created_at: datetime = field(default_factory=datetime.now)
    id: Optional[uuid.UUID] = None

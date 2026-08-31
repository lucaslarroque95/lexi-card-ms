import uuid
from dataclasses import dataclass
from typing import Optional


@dataclass
class Tag:
    user_id: uuid.UUID
    key: str
    value: str
    id: Optional[uuid.UUID] = None

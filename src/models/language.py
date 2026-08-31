import uuid
from dataclasses import dataclass
from typing import Optional


@dataclass
class Language:
    user_id: uuid.UUID
    name: str
    code: str
    id: Optional[uuid.UUID] = None

import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class UserLanguage:
    user_id: uuid.UUID
    language_id: uuid.UUID
    started_at: datetime
    id: Optional[uuid.UUID] = None

import uuid
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional


@dataclass
class ReviewState:
    card_id: uuid.UUID
    user_id: uuid.UUID
    ease_factor: float = 2.5
    interval_days: int = 0
    due_date: date = field(default_factory=date.today)
    repetitions: int = 0
    last_reviewed: Optional[datetime] = None
    id: Optional[uuid.UUID] = None

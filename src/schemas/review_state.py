import uuid
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ReviewStateBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    card_id: uuid.UUID
    ease_factor: float = 2.5
    interval_days: int = 0
    due_date: Optional[date] = None
    repetitions: int = 0
    last_reviewed: Optional[datetime] = None


class ReviewStateCreate(ReviewStateBase):
    pass


class ReviewStateUpdate(BaseModel):
    card_id: Optional[uuid.UUID] = None
    ease_factor: Optional[float] = None
    interval_days: Optional[int] = None
    due_date: Optional[date] = None
    repetitions: Optional[int] = None
    last_reviewed: Optional[datetime] = None


class ReviewStateRead(ReviewStateBase):
    id: uuid.UUID
    user_id: uuid.UUID

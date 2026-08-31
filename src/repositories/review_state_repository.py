import uuid
from abc import ABC, abstractmethod
from typing import List, Optional

from models.review_state import ReviewState


class ReviewStateRepository(ABC):
    @abstractmethod
    def create(self, review_state: ReviewState) -> ReviewState: ...

    @abstractmethod
    def get(self, review_state_id: uuid.UUID) -> Optional[ReviewState]: ...

    @abstractmethod
    def get_all(self) -> List[ReviewState]: ...

    @abstractmethod
    def update(self, review_state_id: uuid.UUID, review_state: ReviewState) -> Optional[ReviewState]: ...

    @abstractmethod
    def delete(self, review_state_id: uuid.UUID) -> bool: ...

    @abstractmethod
    def get_by_user(self, user_id: uuid.UUID) -> List[ReviewState]: ...

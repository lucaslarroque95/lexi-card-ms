import uuid
from typing import List, Optional

from models.review_state import ReviewState
from repositories.review_state_repository import ReviewStateRepository


class ReviewStateService:
    def __init__(self, repository: ReviewStateRepository):
        self.repository = repository

    def create_review_state(self, review_state: ReviewState) -> ReviewState:
        return self.repository.create(review_state)

    def get_review_state(self, review_state_id: uuid.UUID) -> Optional[ReviewState]:
        return self.repository.get(review_state_id)

    def list_review_states(self, user_id: uuid.UUID) -> List[ReviewState]:
        return self.repository.get_by_user(user_id)

    def update_review_state(self, review_state_id: uuid.UUID, review_state: ReviewState) -> Optional[ReviewState]:
        return self.repository.update(review_state_id, review_state)

    def delete_review_state(self, review_state_id: uuid.UUID) -> bool:
        return self.repository.delete(review_state_id)

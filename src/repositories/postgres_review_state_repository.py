import uuid
from dataclasses import asdict
from typing import List, Optional

from sqlmodel import Session, select

from db.orm_models import ReviewStateORM
from models.review_state import ReviewState
from repositories.review_state_repository import ReviewStateRepository


class PostgresReviewStateRepository(ReviewStateRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, review_state: ReviewState) -> ReviewState:
        data = {k: v for k, v in asdict(review_state).items() if k != "id"}
        orm_review_state = ReviewStateORM(**data)
        self.session.add(orm_review_state)
        self.session.commit()
        self.session.refresh(orm_review_state)
        return self._to_domain(orm_review_state)

    def get(self, review_state_id: uuid.UUID) -> Optional[ReviewState]:
        orm_review_state = self.session.get(ReviewStateORM, review_state_id)
        return self._to_domain(orm_review_state) if orm_review_state else None

    def get_all(self) -> List[ReviewState]:
        orm_review_states = self.session.exec(select(ReviewStateORM)).all()
        return [self._to_domain(orm_review_state) for orm_review_state in orm_review_states]

    def update(self, review_state_id: uuid.UUID, review_state: ReviewState) -> Optional[ReviewState]:
        orm_review_state = self.session.get(ReviewStateORM, review_state_id)
        if orm_review_state is None:
            return None

        for field, value in asdict(review_state).items():
            if field != "id":
                setattr(orm_review_state, field, value)

        self.session.add(orm_review_state)
        self.session.commit()
        self.session.refresh(orm_review_state)
        return self._to_domain(orm_review_state)

    def delete(self, review_state_id: uuid.UUID) -> bool:
        orm_review_state = self.session.get(ReviewStateORM, review_state_id)
        if orm_review_state is None:
            return False

        self.session.delete(orm_review_state)
        self.session.commit()
        return True

    def get_by_user(self, user_id: uuid.UUID) -> List[ReviewState]:
        orm_review_states = self.session.exec(
            select(ReviewStateORM).where(ReviewStateORM.user_id == user_id)
        ).all()
        return [self._to_domain(orm_review_state) for orm_review_state in orm_review_states]

    @staticmethod
    def _to_domain(orm_review_state: ReviewStateORM) -> ReviewState:
        return ReviewState(**orm_review_state.model_dump())

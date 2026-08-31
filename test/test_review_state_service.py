import uuid

from fakes import FakeReviewStateRepository
from models.review_state import ReviewState
from services.review_state_service import ReviewStateService


def make_service():
    return ReviewStateService(FakeReviewStateRepository())


def test_create_review_state_defaults():
    service = make_service()
    card_id, user_id = uuid.uuid4(), uuid.uuid4()

    created = service.create_review_state(ReviewState(card_id=card_id, user_id=user_id))

    assert created.ease_factor == 2.5
    assert created.interval_days == 0
    assert created.repetitions == 0
    assert created.due_date is not None
    assert created.last_reviewed is None


def test_list_review_states_scoped_to_user():
    service = make_service()
    user_a, user_b = uuid.uuid4(), uuid.uuid4()
    service.create_review_state(ReviewState(card_id=uuid.uuid4(), user_id=user_a))
    service.create_review_state(ReviewState(card_id=uuid.uuid4(), user_id=user_b))

    assert len(service.list_review_states(user_a)) == 1


def test_update_and_delete_review_state():
    service = make_service()
    card_id, user_id = uuid.uuid4(), uuid.uuid4()
    created = service.create_review_state(ReviewState(card_id=card_id, user_id=user_id))

    updated = service.update_review_state(
        created.id, ReviewState(card_id=card_id, user_id=user_id, repetitions=3, id=created.id)
    )
    assert updated.repetitions == 3

    assert service.delete_review_state(created.id) is True
    assert service.get_review_state(created.id) is None

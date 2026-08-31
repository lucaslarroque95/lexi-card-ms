import uuid

from fakes import FakeDeckRepository
from models.deck import Deck
from services.deck_service import DeckService


def make_service():
    return DeckService(FakeDeckRepository())


def test_create_and_get_deck():
    service = make_service()
    user_id = uuid.uuid4()
    created = service.create_deck(Deck(user_id=user_id, name="My deck"))

    assert created.id is not None
    assert created.created_at is not None
    assert service.get_deck(created.id) == created


def test_list_decks_scoped_to_user():
    service = make_service()
    user_a, user_b = uuid.uuid4(), uuid.uuid4()
    service.create_deck(Deck(user_id=user_a, name="A's deck"))
    service.create_deck(Deck(user_id=user_b, name="B's deck"))

    assert [d.name for d in service.list_decks(user_a)] == ["A's deck"]


def test_update_and_delete_deck():
    service = make_service()
    user_id = uuid.uuid4()
    created = service.create_deck(Deck(user_id=user_id, name="Deck"))

    updated = service.update_deck(created.id, Deck(user_id=user_id, name="Renamed", id=created.id))
    assert updated.name == "Renamed"

    assert service.delete_deck(created.id) is True
    assert service.get_deck(created.id) is None
    assert service.delete_deck(uuid.uuid4()) is False

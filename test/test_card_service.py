import uuid

from fakes import FakeCardRepository, FakeCardTagRepository, FakeTagRepository
from models.card import Card, CardType
from models.tag import Tag
from services.card_service import CardService


def make_service():
    card_tag_repo = FakeCardTagRepository()
    return CardService(FakeCardRepository(), card_tag_repo, FakeTagRepository(card_tag_repo))


def test_create_card_links_given_tags():
    service = make_service()
    user_id = uuid.uuid4()
    tag1 = service.tag_repository.create(Tag(user_id=user_id, key="level", value="A1"))
    tag2 = service.tag_repository.create(Tag(user_id=user_id, key="topic", value="food"))

    created = service.create_card(
        Card(user_id=user_id, deck_id=uuid.uuid4(), card_type=CardType.VOCAB), [tag1.id, tag2.id]
    )

    tags = service.get_tags(created.id)
    assert {t.id for t in tags} == {tag1.id, tag2.id}


def test_create_card_without_tags():
    service = make_service()
    created = service.create_card(Card(user_id=uuid.uuid4(), deck_id=uuid.uuid4(), card_type=CardType.GRAMMAR), [])
    assert service.get_tags(created.id) == []


def test_get_tags_does_not_leak_tags_from_other_cards():
    service = make_service()
    user_id = uuid.uuid4()
    tag = service.tag_repository.create(Tag(user_id=user_id, key="a", value="1"))
    card1 = service.create_card(Card(user_id=user_id, deck_id=uuid.uuid4(), card_type=CardType.VOCAB), [tag.id])
    card2 = service.create_card(Card(user_id=user_id, deck_id=uuid.uuid4(), card_type=CardType.VOCAB), [])

    assert len(service.get_tags(card1.id)) == 1
    assert service.get_tags(card2.id) == []


def test_add_tags_appends_more_tags():
    service = make_service()
    user_id = uuid.uuid4()
    tag1 = service.tag_repository.create(Tag(user_id=user_id, key="a", value="1"))
    tag2 = service.tag_repository.create(Tag(user_id=user_id, key="b", value="2"))
    created = service.create_card(Card(user_id=user_id, deck_id=uuid.uuid4(), card_type=CardType.VOCAB), [tag1.id])

    service.add_tags(created.id, [tag2.id], user_id)

    assert {t.id for t in service.get_tags(created.id)} == {tag1.id, tag2.id}


def test_list_cards_scoped_to_user():
    service = make_service()
    user_a, user_b = uuid.uuid4(), uuid.uuid4()
    service.create_card(Card(user_id=user_a, deck_id=uuid.uuid4(), card_type=CardType.VOCAB), [])
    service.create_card(Card(user_id=user_b, deck_id=uuid.uuid4(), card_type=CardType.VOCAB), [])

    assert len(service.list_cards(user_a)) == 1


def test_update_and_delete_card():
    service = make_service()
    user_id = uuid.uuid4()
    created = service.create_card(Card(user_id=user_id, deck_id=uuid.uuid4(), card_type=CardType.VOCAB), [])

    updated = service.update_card(
        created.id, Card(user_id=user_id, deck_id=created.deck_id, card_type=CardType.GRAMMAR, id=created.id)
    )
    assert updated.card_type == CardType.GRAMMAR

    assert service.delete_card(created.id) is True
    assert service.get_card(created.id) is None

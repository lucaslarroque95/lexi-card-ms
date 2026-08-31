import uuid

from fakes import FakeConceptRepository, FakeExampleRepository
from models.concept import Concept
from services.concept_service import ConceptService


def make_service():
    return ConceptService(FakeConceptRepository(), FakeExampleRepository())


def make_concept(user_id, card_id, language_id):
    return Concept(
        user_id=user_id, card_id=card_id, language_id=language_id, concept="run", explanation="to move fast"
    )


def test_create_concept_creates_examples():
    service = make_service()
    user_id, card_id, language_id = uuid.uuid4(), uuid.uuid4(), uuid.uuid4()

    created = service.create_concept(make_concept(user_id, card_id, language_id), ["He runs.", "She ran."])

    examples = service.get_examples(created.id)
    assert {e.example for e in examples} == {"He runs.", "She ran."}
    assert all(e.concept_id == created.id for e in examples)


def test_create_concept_without_examples():
    service = make_service()
    created = service.create_concept(make_concept(uuid.uuid4(), uuid.uuid4(), uuid.uuid4()), [])
    assert service.get_examples(created.id) == []


def test_add_examples_appends_to_existing():
    service = make_service()
    created = service.create_concept(make_concept(uuid.uuid4(), uuid.uuid4(), uuid.uuid4()), ["e1"])

    service.add_examples(created.id, ["e2", "e3"])

    assert {e.example for e in service.get_examples(created.id)} == {"e1", "e2", "e3"}


def test_list_concepts_by_card_and_by_user():
    service = make_service()
    user_id, card_id, other_card_id = uuid.uuid4(), uuid.uuid4(), uuid.uuid4()
    c1 = service.create_concept(make_concept(user_id, card_id, uuid.uuid4()), [])
    service.create_concept(make_concept(user_id, other_card_id, uuid.uuid4()), [])

    by_card = service.list_concepts_by_card(card_id)
    assert [c.id for c in by_card] == [c1.id]

    by_user = service.list_concepts(user_id)
    assert len(by_user) == 2


def test_update_and_delete_concept():
    service = make_service()
    user_id = uuid.uuid4()
    created = service.create_concept(make_concept(user_id, uuid.uuid4(), uuid.uuid4()), [])

    updated = service.update_concept(
        created.id,
        Concept(
            user_id=user_id,
            card_id=created.card_id,
            language_id=created.language_id,
            concept="jump",
            explanation="x",
            id=created.id,
        ),
    )
    assert updated.concept == "jump"

    assert service.delete_concept(created.id) is True
    assert service.get_concept(created.id) is None

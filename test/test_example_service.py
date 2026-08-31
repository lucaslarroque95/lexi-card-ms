import uuid

from fakes import FakeConceptRepository, FakeExampleRepository, FakeRuleRepository
from models.concept import Concept
from models.example import Example
from models.rule import Rule
from services.example_service import ExampleService


def make_service():
    return ExampleService(FakeExampleRepository(), FakeConceptRepository(), FakeRuleRepository())


def test_get_owner_via_concept():
    service = make_service()
    user_id = uuid.uuid4()
    concept = service.concept_repository.create(
        Concept(user_id=user_id, card_id=uuid.uuid4(), language_id=uuid.uuid4(), concept="c", explanation="x")
    )

    assert service.get_owner(Example(example="ex", concept_id=concept.id)) == user_id


def test_get_owner_via_rule():
    service = make_service()
    user_id = uuid.uuid4()
    rule = service.rule_repository.create(
        Rule(user_id=user_id, card_id=uuid.uuid4(), language_id=uuid.uuid4(), rule="r", explanation="x")
    )

    assert service.get_owner(Example(example="ex", rule_id=rule.id)) == user_id


def test_get_owner_none_when_neither_parent_set():
    service = make_service()
    assert service.get_owner(Example(example="ex")) is None


def test_get_owner_none_when_parent_missing():
    service = make_service()
    assert service.get_owner(Example(example="ex", concept_id=uuid.uuid4())) is None
    assert service.get_owner(Example(example="ex", rule_id=uuid.uuid4())) is None


def test_list_examples_aggregates_concept_and_rule_examples_for_user_only():
    service = make_service()
    user_id, other_user = uuid.uuid4(), uuid.uuid4()
    concept = service.concept_repository.create(
        Concept(user_id=user_id, card_id=uuid.uuid4(), language_id=uuid.uuid4(), concept="c", explanation="x")
    )
    rule = service.rule_repository.create(
        Rule(user_id=user_id, card_id=uuid.uuid4(), language_id=uuid.uuid4(), rule="r", explanation="x")
    )
    other_concept = service.concept_repository.create(
        Concept(user_id=other_user, card_id=uuid.uuid4(), language_id=uuid.uuid4(), concept="c2", explanation="x")
    )

    service.repository.create(Example(example="concept example", concept_id=concept.id))
    service.repository.create(Example(example="rule example", rule_id=rule.id))
    service.repository.create(Example(example="other user's example", concept_id=other_concept.id))

    examples = service.list_examples(user_id)
    assert {e.example for e in examples} == {"concept example", "rule example"}


def test_create_get_update_delete_example():
    service = make_service()
    created = service.create_example(Example(example="ex"))

    assert service.get_example(created.id) == created

    updated = service.update_example(created.id, Example(example="updated", id=created.id))
    assert updated.example == "updated"

    assert service.delete_example(created.id) is True
    assert service.get_example(created.id) is None

import uuid

from fakes import FakeExampleRepository, FakeRuleRepository
from models.rule import Rule
from services.rule_service import RuleService


def make_service():
    return RuleService(FakeRuleRepository(), FakeExampleRepository())


def make_rule(user_id, card_id, language_id):
    return Rule(
        user_id=user_id,
        card_id=card_id,
        language_id=language_id,
        rule="ser vs estar",
        explanation="permanent vs temporary",
    )


def test_create_rule_creates_examples():
    service = make_service()
    user_id, card_id, language_id = uuid.uuid4(), uuid.uuid4(), uuid.uuid4()

    created = service.create_rule(make_rule(user_id, card_id, language_id), ["Soy alto.", "Estoy cansado."])

    examples = service.get_examples(created.id)
    assert {e.example for e in examples} == {"Soy alto.", "Estoy cansado."}
    assert all(e.rule_id == created.id for e in examples)


def test_create_rule_without_examples():
    service = make_service()
    created = service.create_rule(make_rule(uuid.uuid4(), uuid.uuid4(), uuid.uuid4()), [])
    assert service.get_examples(created.id) == []


def test_add_examples_appends_to_existing():
    service = make_service()
    created = service.create_rule(make_rule(uuid.uuid4(), uuid.uuid4(), uuid.uuid4()), ["e1"])

    service.add_examples(created.id, ["e2", "e3"])

    assert {e.example for e in service.get_examples(created.id)} == {"e1", "e2", "e3"}


def test_list_rules_by_card_and_by_user():
    service = make_service()
    user_id, card_id, other_card_id = uuid.uuid4(), uuid.uuid4(), uuid.uuid4()
    r1 = service.create_rule(make_rule(user_id, card_id, uuid.uuid4()), [])
    service.create_rule(make_rule(user_id, other_card_id, uuid.uuid4()), [])

    by_card = service.list_rules_by_card(card_id)
    assert [r.id for r in by_card] == [r1.id]

    by_user = service.list_rules(user_id)
    assert len(by_user) == 2


def test_update_and_delete_rule():
    service = make_service()
    user_id = uuid.uuid4()
    created = service.create_rule(make_rule(user_id, uuid.uuid4(), uuid.uuid4()), [])

    updated = service.update_rule(
        created.id,
        Rule(
            user_id=user_id,
            card_id=created.card_id,
            language_id=created.language_id,
            rule="por vs para",
            explanation="x",
            id=created.id,
        ),
    )
    assert updated.rule == "por vs para"

    assert service.delete_rule(created.id) is True
    assert service.get_rule(created.id) is None

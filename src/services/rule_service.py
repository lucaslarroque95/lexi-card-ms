import uuid
from typing import List, Optional

from models.example import Example
from models.rule import Rule
from repositories.example_repository import ExampleRepository
from repositories.rule_repository import RuleRepository


class RuleService:
    def __init__(self, repository: RuleRepository, example_repository: ExampleRepository):
        self.repository = repository
        self.example_repository = example_repository

    def create_rule(self, rule: Rule, examples: List[str]) -> Rule:
        created = self.repository.create(rule)
        for example in examples:
            self.example_repository.create(Example(example=example, rule_id=created.id))
        return created

    def get_rule(self, rule_id: uuid.UUID) -> Optional[Rule]:
        return self.repository.get(rule_id)

    def list_rules(self, user_id: uuid.UUID) -> List[Rule]:
        return self.repository.get_by_user(user_id)

    def list_rules_by_card(self, card_id: uuid.UUID) -> List[Rule]:
        return self.repository.get_by_card(card_id)

    def update_rule(self, rule_id: uuid.UUID, rule: Rule) -> Optional[Rule]:
        return self.repository.update(rule_id, rule)

    def delete_rule(self, rule_id: uuid.UUID) -> bool:
        return self.repository.delete(rule_id)

    def get_examples(self, rule_id: uuid.UUID) -> List[Example]:
        return self.example_repository.get_by_rule(rule_id)

    def add_examples(self, rule_id: uuid.UUID, examples: List[str]) -> List[Example]:
        return [self.example_repository.create(Example(example=text, rule_id=rule_id)) for text in examples]

import uuid
from typing import List, Optional

from models.example import Example
from repositories.concept_repository import ConceptRepository
from repositories.example_repository import ExampleRepository
from repositories.rule_repository import RuleRepository


class ExampleService:
    def __init__(
        self,
        repository: ExampleRepository,
        concept_repository: ConceptRepository,
        rule_repository: RuleRepository,
    ):
        self.repository = repository
        self.concept_repository = concept_repository
        self.rule_repository = rule_repository

    def create_example(self, example: Example) -> Example:
        return self.repository.create(example)

    def get_example(self, example_id: uuid.UUID) -> Optional[Example]:
        return self.repository.get(example_id)

    def list_examples(self, user_id: uuid.UUID) -> List[Example]:
        examples: List[Example] = []
        for concept in self.concept_repository.get_by_user(user_id):
            examples.extend(self.repository.get_by_concept(concept.id))
        for rule in self.rule_repository.get_by_user(user_id):
            examples.extend(self.repository.get_by_rule(rule.id))
        return examples

    def update_example(self, example_id: uuid.UUID, example: Example) -> Optional[Example]:
        return self.repository.update(example_id, example)

    def delete_example(self, example_id: uuid.UUID) -> bool:
        return self.repository.delete(example_id)

    def get_owner(self, example: Example) -> Optional[uuid.UUID]:
        """El user_id del Concept o Rule al que pertenece el example."""
        if example.concept_id is not None:
            concept = self.concept_repository.get(example.concept_id)
            return concept.user_id if concept else None
        if example.rule_id is not None:
            rule = self.rule_repository.get(example.rule_id)
            return rule.user_id if rule else None
        return None

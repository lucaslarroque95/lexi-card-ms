import uuid
from typing import List, Optional

from models.concept import Concept
from models.example import Example
from repositories.concept_repository import ConceptRepository
from repositories.example_repository import ExampleRepository


class ConceptService:
    def __init__(self, repository: ConceptRepository, example_repository: ExampleRepository):
        self.repository = repository
        self.example_repository = example_repository

    def create_concept(self, concept: Concept, examples: List[str]) -> Concept:
        created = self.repository.create(concept)
        for example in examples:
            self.example_repository.create(Example(example=example, concept_id=created.id))
        return created

    def get_concept(self, concept_id: uuid.UUID) -> Optional[Concept]:
        return self.repository.get(concept_id)

    def list_concepts(self, user_id: uuid.UUID) -> List[Concept]:
        return self.repository.get_by_user(user_id)

    def list_concepts_by_card(self, card_id: uuid.UUID) -> List[Concept]:
        return self.repository.get_by_card(card_id)

    def update_concept(self, concept_id: uuid.UUID, concept: Concept) -> Optional[Concept]:
        return self.repository.update(concept_id, concept)

    def delete_concept(self, concept_id: uuid.UUID) -> bool:
        return self.repository.delete(concept_id)

    def get_examples(self, concept_id: uuid.UUID) -> List[Example]:
        return self.example_repository.get_by_concept(concept_id)

    def add_examples(self, concept_id: uuid.UUID, examples: List[str]) -> List[Example]:
        return [
            self.example_repository.create(Example(example=text, concept_id=concept_id)) for text in examples
        ]

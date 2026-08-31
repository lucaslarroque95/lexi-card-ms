import uuid
from dataclasses import replace
from typing import Dict, Generic, List, Optional, TypeVar

from repositories.card_repository import CardRepository
from repositories.card_tag_repository import CardTagRepository
from repositories.concept_repository import ConceptRepository
from repositories.deck_repository import DeckRepository
from repositories.example_repository import ExampleRepository
from repositories.language_repository import LanguageRepository
from repositories.review_state_repository import ReviewStateRepository
from repositories.rule_repository import RuleRepository
from repositories.tag_repository import TagRepository
from repositories.user_language_repository import UserLanguageRepository

T = TypeVar("T")


class InMemoryRepository(Generic[T]):
    """Repositorio genérico en memoria: cubre el CRUD común a todos los ABC."""

    def __init__(self):
        self._store: Dict[uuid.UUID, T] = {}

    def create(self, item: T) -> T:
        new_id = uuid.uuid4()
        stored = replace(item, id=new_id)
        self._store[new_id] = stored
        return stored

    def get(self, item_id: uuid.UUID) -> Optional[T]:
        return self._store.get(item_id)

    def get_all(self) -> List[T]:
        return list(self._store.values())

    def update(self, item_id: uuid.UUID, item: T) -> Optional[T]:
        if item_id not in self._store:
            return None
        updated = replace(item, id=item_id)
        self._store[item_id] = updated
        return updated

    def delete(self, item_id: uuid.UUID) -> bool:
        return self._store.pop(item_id, None) is not None


class FakeLanguageRepository(InMemoryRepository, LanguageRepository):
    def get_by_user(self, user_id: uuid.UUID) -> List:
        return [item for item in self._store.values() if item.user_id == user_id]


class FakeUserLanguageRepository(InMemoryRepository, UserLanguageRepository):
    pass


class FakeDeckRepository(InMemoryRepository, DeckRepository):
    def get_by_user(self, user_id: uuid.UUID) -> List:
        return [item for item in self._store.values() if item.user_id == user_id]


class FakeConceptRepository(InMemoryRepository, ConceptRepository):
    def get_by_user(self, user_id: uuid.UUID) -> List:
        return [item for item in self._store.values() if item.user_id == user_id]

    def get_by_card(self, card_id: uuid.UUID) -> List:
        return [item for item in self._store.values() if item.card_id == card_id]


class FakeRuleRepository(InMemoryRepository, RuleRepository):
    def get_by_user(self, user_id: uuid.UUID) -> List:
        return [item for item in self._store.values() if item.user_id == user_id]

    def get_by_card(self, card_id: uuid.UUID) -> List:
        return [item for item in self._store.values() if item.card_id == card_id]


class FakeCardRepository(InMemoryRepository, CardRepository):
    def get_by_user(self, user_id: uuid.UUID) -> List:
        return [item for item in self._store.values() if item.user_id == user_id]


class FakeCardTagRepository(InMemoryRepository, CardTagRepository):
    pass


class FakeTagRepository(InMemoryRepository, TagRepository):
    """Necesita el repo de card_tags para poder resolver get_by_card, igual que el join real."""

    def __init__(self, card_tag_repository: FakeCardTagRepository):
        super().__init__()
        self._card_tag_repository = card_tag_repository

    def get_by_user(self, user_id: uuid.UUID) -> List:
        return [item for item in self._store.values() if item.user_id == user_id]

    def get_by_card(self, card_id: uuid.UUID) -> List:
        tag_ids = {ct.tag_id for ct in self._card_tag_repository.get_all() if ct.card_id == card_id}
        return [item for item in self._store.values() if item.id in tag_ids]


class FakeExampleRepository(InMemoryRepository, ExampleRepository):
    def get_by_concept(self, concept_id: uuid.UUID) -> List:
        return [item for item in self._store.values() if item.concept_id == concept_id]

    def get_by_rule(self, rule_id: uuid.UUID) -> List:
        return [item for item in self._store.values() if item.rule_id == rule_id]


class FakeReviewStateRepository(InMemoryRepository, ReviewStateRepository):
    def get_by_user(self, user_id: uuid.UUID) -> List:
        return [item for item in self._store.values() if item.user_id == user_id]

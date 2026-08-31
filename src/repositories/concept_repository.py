import uuid
from abc import ABC, abstractmethod
from typing import List, Optional

from models.concept import Concept


class ConceptRepository(ABC):
    @abstractmethod
    def create(self, concept: Concept) -> Concept: ...

    @abstractmethod
    def get(self, concept_id: uuid.UUID) -> Optional[Concept]: ...

    @abstractmethod
    def get_all(self) -> List[Concept]: ...

    @abstractmethod
    def update(self, concept_id: uuid.UUID, concept: Concept) -> Optional[Concept]: ...

    @abstractmethod
    def delete(self, concept_id: uuid.UUID) -> bool: ...

    @abstractmethod
    def get_by_user(self, user_id: uuid.UUID) -> List[Concept]: ...

    @abstractmethod
    def get_by_card(self, card_id: uuid.UUID) -> List[Concept]: ...

import uuid
from abc import ABC, abstractmethod
from typing import List, Optional

from models.deck import Deck


class DeckRepository(ABC):
    @abstractmethod
    def create(self, deck: Deck) -> Deck: ...

    @abstractmethod
    def get(self, deck_id: uuid.UUID) -> Optional[Deck]: ...

    @abstractmethod
    def get_all(self) -> List[Deck]: ...

    @abstractmethod
    def update(self, deck_id: uuid.UUID, deck: Deck) -> Optional[Deck]: ...

    @abstractmethod
    def delete(self, deck_id: uuid.UUID) -> bool: ...

    @abstractmethod
    def get_by_user(self, user_id: uuid.UUID) -> List[Deck]: ...

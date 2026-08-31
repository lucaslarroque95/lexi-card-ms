import uuid
from abc import ABC, abstractmethod
from typing import List, Optional

from models.card import Card


class CardRepository(ABC):
    @abstractmethod
    def create(self, card: Card) -> Card: ...

    @abstractmethod
    def get(self, card_id: uuid.UUID) -> Optional[Card]: ...

    @abstractmethod
    def get_all(self) -> List[Card]: ...

    @abstractmethod
    def update(self, card_id: uuid.UUID, card: Card) -> Optional[Card]: ...

    @abstractmethod
    def delete(self, card_id: uuid.UUID) -> bool: ...

    @abstractmethod
    def get_by_user(self, user_id: uuid.UUID) -> List[Card]: ...

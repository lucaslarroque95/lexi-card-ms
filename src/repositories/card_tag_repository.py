import uuid
from abc import ABC, abstractmethod
from typing import List, Optional

from models.card_tag import CardTag


class CardTagRepository(ABC):
    @abstractmethod
    def create(self, card_tag: CardTag) -> CardTag: ...

    @abstractmethod
    def get(self, card_tag_id: uuid.UUID) -> Optional[CardTag]: ...

    @abstractmethod
    def get_all(self) -> List[CardTag]: ...

    @abstractmethod
    def update(self, card_tag_id: uuid.UUID, card_tag: CardTag) -> Optional[CardTag]: ...

    @abstractmethod
    def delete(self, card_tag_id: uuid.UUID) -> bool: ...

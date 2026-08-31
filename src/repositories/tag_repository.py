import uuid
from abc import ABC, abstractmethod
from typing import List, Optional

from models.tag import Tag


class TagRepository(ABC):
    @abstractmethod
    def create(self, tag: Tag) -> Tag: ...

    @abstractmethod
    def get(self, tag_id: uuid.UUID) -> Optional[Tag]: ...

    @abstractmethod
    def get_all(self) -> List[Tag]: ...

    @abstractmethod
    def update(self, tag_id: uuid.UUID, tag: Tag) -> Optional[Tag]: ...

    @abstractmethod
    def delete(self, tag_id: uuid.UUID) -> bool: ...

    @abstractmethod
    def get_by_card(self, card_id: uuid.UUID) -> List[Tag]: ...

    @abstractmethod
    def get_by_user(self, user_id: uuid.UUID) -> List[Tag]: ...

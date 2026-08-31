import uuid
from abc import ABC, abstractmethod
from typing import List, Optional

from models.language import Language


class LanguageRepository(ABC):
    @abstractmethod
    def create(self, language: Language) -> Language: ...

    @abstractmethod
    def get(self, language_id: uuid.UUID) -> Optional[Language]: ...

    @abstractmethod
    def get_all(self) -> List[Language]: ...

    @abstractmethod
    def update(self, language_id: uuid.UUID, language: Language) -> Optional[Language]: ...

    @abstractmethod
    def delete(self, language_id: uuid.UUID) -> bool: ...

    @abstractmethod
    def get_by_user(self, user_id: uuid.UUID) -> List[Language]: ...

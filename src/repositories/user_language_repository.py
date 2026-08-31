import uuid
from abc import ABC, abstractmethod
from typing import List, Optional

from models.user_language import UserLanguage


class UserLanguageRepository(ABC):
    @abstractmethod
    def create(self, user_language: UserLanguage) -> UserLanguage: ...

    @abstractmethod
    def get(self, user_language_id: uuid.UUID) -> Optional[UserLanguage]: ...

    @abstractmethod
    def get_all(self) -> List[UserLanguage]: ...

    @abstractmethod
    def update(self, user_language_id: uuid.UUID, user_language: UserLanguage) -> Optional[UserLanguage]: ...

    @abstractmethod
    def delete(self, user_language_id: uuid.UUID) -> bool: ...

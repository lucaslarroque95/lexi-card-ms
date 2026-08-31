import uuid
from datetime import datetime
from typing import List, Optional

from models.language import Language
from models.user_language import UserLanguage
from repositories.language_repository import LanguageRepository
from repositories.user_language_repository import UserLanguageRepository


class LanguageService:
    def __init__(self, language_repository: LanguageRepository, user_language_repository: UserLanguageRepository):
        self.language_repository = language_repository
        self.user_language_repository = user_language_repository

    def create_language(self, language: Language, user_id: uuid.UUID, started_at: Optional[datetime] = None) -> Language:
        created = self.language_repository.create(language)
        self.user_language_repository.create(
            UserLanguage(user_id=user_id, language_id=created.id, started_at=started_at or datetime.now())
        )
        return created

    def get_language(self, language_id: uuid.UUID) -> Optional[Language]:
        return self.language_repository.get(language_id)

    def list_languages(self, user_id: uuid.UUID) -> List[Language]:
        return self.language_repository.get_by_user(user_id)

    def update_language(self, language_id: uuid.UUID, language: Language) -> Optional[Language]:
        return self.language_repository.update(language_id, language)

    def delete_language(self, language_id: uuid.UUID) -> bool:
        return self.language_repository.delete(language_id)

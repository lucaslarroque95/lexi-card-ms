import uuid
from dataclasses import asdict
from typing import List, Optional

from sqlmodel import Session, select

from db.orm_models import UserLanguageORM
from models.user_language import UserLanguage
from repositories.user_language_repository import UserLanguageRepository


class PostgresUserLanguageRepository(UserLanguageRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, user_language: UserLanguage) -> UserLanguage:
        data = {k: v for k, v in asdict(user_language).items() if k != "id"}
        orm_user_language = UserLanguageORM(**data)
        self.session.add(orm_user_language)
        self.session.commit()
        self.session.refresh(orm_user_language)
        return self._to_domain(orm_user_language)

    def get(self, user_language_id: uuid.UUID) -> Optional[UserLanguage]:
        orm_user_language = self.session.get(UserLanguageORM, user_language_id)
        return self._to_domain(orm_user_language) if orm_user_language else None

    def get_all(self) -> List[UserLanguage]:
        orm_user_languages = self.session.exec(select(UserLanguageORM)).all()
        return [self._to_domain(orm_user_language) for orm_user_language in orm_user_languages]

    def update(self, user_language_id: uuid.UUID, user_language: UserLanguage) -> Optional[UserLanguage]:
        orm_user_language = self.session.get(UserLanguageORM, user_language_id)
        if orm_user_language is None:
            return None

        for field, value in asdict(user_language).items():
            if field != "id":
                setattr(orm_user_language, field, value)

        self.session.add(orm_user_language)
        self.session.commit()
        self.session.refresh(orm_user_language)
        return self._to_domain(orm_user_language)

    def delete(self, user_language_id: uuid.UUID) -> bool:
        orm_user_language = self.session.get(UserLanguageORM, user_language_id)
        if orm_user_language is None:
            return False

        self.session.delete(orm_user_language)
        self.session.commit()
        return True

    @staticmethod
    def _to_domain(orm_user_language: UserLanguageORM) -> UserLanguage:
        return UserLanguage(**orm_user_language.model_dump())

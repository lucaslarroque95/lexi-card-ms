import uuid
from dataclasses import asdict
from typing import List, Optional

from sqlmodel import Session, select

from db.orm_models import LanguageORM
from models.language import Language
from repositories.language_repository import LanguageRepository


class PostgresLanguageRepository(LanguageRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, language: Language) -> Language:
        data = {k: v for k, v in asdict(language).items() if k != "id"}
        orm_language = LanguageORM(**data)
        self.session.add(orm_language)
        self.session.commit()
        self.session.refresh(orm_language)
        return self._to_domain(orm_language)

    def get(self, language_id: uuid.UUID) -> Optional[Language]:
        orm_language = self.session.get(LanguageORM, language_id)
        return self._to_domain(orm_language) if orm_language else None

    def get_all(self) -> List[Language]:
        orm_languages = self.session.exec(select(LanguageORM)).all()
        return [self._to_domain(orm_language) for orm_language in orm_languages]

    def update(self, language_id: uuid.UUID, language: Language) -> Optional[Language]:
        orm_language = self.session.get(LanguageORM, language_id)
        if orm_language is None:
            return None

        for field, value in asdict(language).items():
            if field != "id":
                setattr(orm_language, field, value)

        self.session.add(orm_language)
        self.session.commit()
        self.session.refresh(orm_language)
        return self._to_domain(orm_language)

    def delete(self, language_id: uuid.UUID) -> bool:
        orm_language = self.session.get(LanguageORM, language_id)
        if orm_language is None:
            return False

        self.session.delete(orm_language)
        self.session.commit()
        return True

    def get_by_user(self, user_id: uuid.UUID) -> List[Language]:
        orm_languages = self.session.exec(select(LanguageORM).where(LanguageORM.user_id == user_id)).all()
        return [self._to_domain(orm_language) for orm_language in orm_languages]

    @staticmethod
    def _to_domain(orm_language: LanguageORM) -> Language:
        return Language(**orm_language.model_dump())

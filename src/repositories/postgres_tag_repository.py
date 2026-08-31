import uuid
from dataclasses import asdict
from typing import List, Optional

from sqlmodel import Session, select

from db.orm_models import CardTagORM, TagORM
from models.tag import Tag
from repositories.tag_repository import TagRepository


class PostgresTagRepository(TagRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, tag: Tag) -> Tag:
        data = {k: v for k, v in asdict(tag).items() if k != "id"}
        orm_tag = TagORM(**data)
        self.session.add(orm_tag)
        self.session.commit()
        self.session.refresh(orm_tag)
        return self._to_domain(orm_tag)

    def get(self, tag_id: uuid.UUID) -> Optional[Tag]:
        orm_tag = self.session.get(TagORM, tag_id)
        return self._to_domain(orm_tag) if orm_tag else None

    def get_all(self) -> List[Tag]:
        orm_tags = self.session.exec(select(TagORM)).all()
        return [self._to_domain(orm_tag) for orm_tag in orm_tags]

    def update(self, tag_id: uuid.UUID, tag: Tag) -> Optional[Tag]:
        orm_tag = self.session.get(TagORM, tag_id)
        if orm_tag is None:
            return None

        for field, value in asdict(tag).items():
            if field != "id":
                setattr(orm_tag, field, value)

        self.session.add(orm_tag)
        self.session.commit()
        self.session.refresh(orm_tag)
        return self._to_domain(orm_tag)

    def delete(self, tag_id: uuid.UUID) -> bool:
        orm_tag = self.session.get(TagORM, tag_id)
        if orm_tag is None:
            return False

        self.session.delete(orm_tag)
        self.session.commit()
        return True

    def get_by_card(self, card_id: uuid.UUID) -> List[Tag]:
        orm_tags = self.session.exec(
            select(TagORM).join(CardTagORM, CardTagORM.tag_id == TagORM.id).where(CardTagORM.card_id == card_id)
        ).all()
        return [self._to_domain(orm_tag) for orm_tag in orm_tags]

    def get_by_user(self, user_id: uuid.UUID) -> List[Tag]:
        orm_tags = self.session.exec(select(TagORM).where(TagORM.user_id == user_id)).all()
        return [self._to_domain(orm_tag) for orm_tag in orm_tags]

    @staticmethod
    def _to_domain(orm_tag: TagORM) -> Tag:
        return Tag(**orm_tag.model_dump())

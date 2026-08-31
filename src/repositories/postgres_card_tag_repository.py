import uuid
from dataclasses import asdict
from typing import List, Optional

from sqlmodel import Session, select

from db.orm_models import CardTagORM
from models.card_tag import CardTag
from repositories.card_tag_repository import CardTagRepository


class PostgresCardTagRepository(CardTagRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, card_tag: CardTag) -> CardTag:
        data = {k: v for k, v in asdict(card_tag).items() if k != "id"}
        orm_card_tag = CardTagORM(**data)
        self.session.add(orm_card_tag)
        self.session.commit()
        self.session.refresh(orm_card_tag)
        return self._to_domain(orm_card_tag)

    def get(self, card_tag_id: uuid.UUID) -> Optional[CardTag]:
        orm_card_tag = self.session.get(CardTagORM, card_tag_id)
        return self._to_domain(orm_card_tag) if orm_card_tag else None

    def get_all(self) -> List[CardTag]:
        orm_card_tags = self.session.exec(select(CardTagORM)).all()
        return [self._to_domain(orm_card_tag) for orm_card_tag in orm_card_tags]

    def update(self, card_tag_id: uuid.UUID, card_tag: CardTag) -> Optional[CardTag]:
        orm_card_tag = self.session.get(CardTagORM, card_tag_id)
        if orm_card_tag is None:
            return None

        for field, value in asdict(card_tag).items():
            if field != "id":
                setattr(orm_card_tag, field, value)

        self.session.add(orm_card_tag)
        self.session.commit()
        self.session.refresh(orm_card_tag)
        return self._to_domain(orm_card_tag)

    def delete(self, card_tag_id: uuid.UUID) -> bool:
        orm_card_tag = self.session.get(CardTagORM, card_tag_id)
        if orm_card_tag is None:
            return False

        self.session.delete(orm_card_tag)
        self.session.commit()
        return True

    @staticmethod
    def _to_domain(orm_card_tag: CardTagORM) -> CardTag:
        return CardTag(**orm_card_tag.model_dump())

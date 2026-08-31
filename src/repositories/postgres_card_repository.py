import uuid
from dataclasses import asdict
from typing import List, Optional

from sqlmodel import Session, select

from db.orm_models import CardORM
from models.card import Card
from repositories.card_repository import CardRepository


class PostgresCardRepository(CardRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, card: Card) -> Card:
        data = {k: v for k, v in asdict(card).items() if k != "id"}
        orm_card = CardORM(**data)
        self.session.add(orm_card)
        self.session.commit()
        self.session.refresh(orm_card)
        return self._to_domain(orm_card)

    def get(self, card_id: uuid.UUID) -> Optional[Card]:
        orm_card = self.session.get(CardORM, card_id)
        return self._to_domain(orm_card) if orm_card else None

    def get_all(self) -> List[Card]:
        orm_cards = self.session.exec(select(CardORM)).all()
        return [self._to_domain(orm_card) for orm_card in orm_cards]

    def update(self, card_id: uuid.UUID, card: Card) -> Optional[Card]:
        orm_card = self.session.get(CardORM, card_id)
        if orm_card is None:
            return None

        for field, value in asdict(card).items():
            if field != "id":
                setattr(orm_card, field, value)

        self.session.add(orm_card)
        self.session.commit()
        self.session.refresh(orm_card)
        return self._to_domain(orm_card)

    def delete(self, card_id: uuid.UUID) -> bool:
        orm_card = self.session.get(CardORM, card_id)
        if orm_card is None:
            return False

        self.session.delete(orm_card)
        self.session.commit()
        return True

    def get_by_user(self, user_id: uuid.UUID) -> List[Card]:
        orm_cards = self.session.exec(select(CardORM).where(CardORM.user_id == user_id)).all()
        return [self._to_domain(orm_card) for orm_card in orm_cards]

    @staticmethod
    def _to_domain(orm_card: CardORM) -> Card:
        return Card(**orm_card.model_dump())

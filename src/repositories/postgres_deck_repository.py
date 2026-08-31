import uuid
from dataclasses import asdict
from typing import List, Optional

from sqlmodel import Session, select

from db.orm_models import DeckORM
from models.deck import Deck
from repositories.deck_repository import DeckRepository


class PostgresDeckRepository(DeckRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, deck: Deck) -> Deck:
        data = {k: v for k, v in asdict(deck).items() if k != "id"}
        orm_deck = DeckORM(**data)
        self.session.add(orm_deck)
        self.session.commit()
        self.session.refresh(orm_deck)
        return self._to_domain(orm_deck)

    def get(self, deck_id: uuid.UUID) -> Optional[Deck]:
        orm_deck = self.session.get(DeckORM, deck_id)
        return self._to_domain(orm_deck) if orm_deck else None

    def get_all(self) -> List[Deck]:
        orm_decks = self.session.exec(select(DeckORM)).all()
        return [self._to_domain(orm_deck) for orm_deck in orm_decks]

    def update(self, deck_id: uuid.UUID, deck: Deck) -> Optional[Deck]:
        orm_deck = self.session.get(DeckORM, deck_id)
        if orm_deck is None:
            return None

        for field, value in asdict(deck).items():
            if field != "id":
                setattr(orm_deck, field, value)

        self.session.add(orm_deck)
        self.session.commit()
        self.session.refresh(orm_deck)
        return self._to_domain(orm_deck)

    def delete(self, deck_id: uuid.UUID) -> bool:
        orm_deck = self.session.get(DeckORM, deck_id)
        if orm_deck is None:
            return False

        self.session.delete(orm_deck)
        self.session.commit()
        return True

    def get_by_user(self, user_id: uuid.UUID) -> List[Deck]:
        orm_decks = self.session.exec(select(DeckORM).where(DeckORM.user_id == user_id)).all()
        return [self._to_domain(orm_deck) for orm_deck in orm_decks]

    @staticmethod
    def _to_domain(orm_deck: DeckORM) -> Deck:
        return Deck(**orm_deck.model_dump())

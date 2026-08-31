import uuid
from typing import List, Optional

from models.deck import Deck
from repositories.deck_repository import DeckRepository


class DeckService:
    def __init__(self, repository: DeckRepository):
        self.repository = repository

    def create_deck(self, deck: Deck) -> Deck:
        return self.repository.create(deck)

    def get_deck(self, deck_id: uuid.UUID) -> Optional[Deck]:
        return self.repository.get(deck_id)

    def list_decks(self, user_id: uuid.UUID) -> List[Deck]:
        return self.repository.get_by_user(user_id)

    def update_deck(self, deck_id: uuid.UUID, deck: Deck) -> Optional[Deck]:
        return self.repository.update(deck_id, deck)

    def delete_deck(self, deck_id: uuid.UUID) -> bool:
        return self.repository.delete(deck_id)

import uuid
from typing import List, Optional

from models.card import Card
from models.card_tag import CardTag
from models.tag import Tag
from repositories.card_repository import CardRepository
from repositories.card_tag_repository import CardTagRepository
from repositories.tag_repository import TagRepository


class CardService:
    def __init__(
        self,
        card_repository: CardRepository,
        card_tag_repository: CardTagRepository,
        tag_repository: TagRepository,
    ):
        self.card_repository = card_repository
        self.card_tag_repository = card_tag_repository
        self.tag_repository = tag_repository

    def create_card(self, card: Card, tag_ids: List[uuid.UUID]) -> Card:
        created = self.card_repository.create(card)
        for tag_id in tag_ids:
            self.card_tag_repository.create(CardTag(user_id=created.user_id, card_id=created.id, tag_id=tag_id))
        return created

    def get_card(self, card_id: uuid.UUID) -> Optional[Card]:
        return self.card_repository.get(card_id)

    def list_cards(self, user_id: uuid.UUID) -> List[Card]:
        return self.card_repository.get_by_user(user_id)

    def update_card(self, card_id: uuid.UUID, card: Card) -> Optional[Card]:
        return self.card_repository.update(card_id, card)

    def delete_card(self, card_id: uuid.UUID) -> bool:
        return self.card_repository.delete(card_id)

    def get_tags(self, card_id: uuid.UUID) -> List[Tag]:
        return self.tag_repository.get_by_card(card_id)

    def add_tags(self, card_id: uuid.UUID, tag_ids: List[uuid.UUID], user_id: uuid.UUID) -> None:
        for tag_id in tag_ids:
            self.card_tag_repository.create(CardTag(user_id=user_id, card_id=card_id, tag_id=tag_id))

import uuid
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class CardType(str, Enum):
    VOCAB = "vocab"
    GRAMMAR = "grammar"


@dataclass
class Card:
    user_id: uuid.UUID
    deck_id: uuid.UUID
    card_type: CardType
    id: Optional[uuid.UUID] = None

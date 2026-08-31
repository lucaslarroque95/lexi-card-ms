import uuid
from datetime import date, datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

from models.card import CardType


# Lista de idiomas
class LanguageORM(SQLModel, table=True):
    __tablename__ = "languages"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID
    name: str
    code: str

    user_languages: List["UserLanguageORM"] = Relationship(back_populates="language")
    concepts: List["ConceptORM"] = Relationship(back_populates="language")
    rules: List["RuleORM"] = Relationship(back_populates="language")


# Qué idiomas estudia cada usuario (many-to-many)
class UserLanguageORM(SQLModel, table=True):
    __tablename__ = "user_languages"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID
    language_id: uuid.UUID = Field(foreign_key="languages.id")
    started_at: datetime = Field(default_factory=datetime.now)

    language: LanguageORM = Relationship(back_populates="user_languages")


class DeckORM(SQLModel, table=True):
    __tablename__ = "decks"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID
    name: str
    created_at: datetime = Field(default_factory=datetime.now)

    cards: List["CardORM"] = Relationship(back_populates="deck")


# Qué tag contiene cada card (many-to-many) — declarada antes para poder
# usarla como link_model en CardORM y TagORM.
class CardTagORM(SQLModel, table=True):
    __tablename__ = "card_tags"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID
    card_id: uuid.UUID = Field(foreign_key="cards.id")
    tag_id: uuid.UUID = Field(foreign_key="tags.id")


# Un concepto de vocabulario dentro de una card (una card puede tener varios)
class ConceptORM(SQLModel, table=True):
    __tablename__ = "concepts"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID
    card_id: uuid.UUID = Field(foreign_key="cards.id")
    language_id: uuid.UUID = Field(foreign_key="languages.id")
    concept: str
    explanation: str

    card: "CardORM" = Relationship(back_populates="concepts")
    language: LanguageORM = Relationship(back_populates="concepts")
    examples: List["ExampleORM"] = Relationship(back_populates="concept")


# Una regla gramatical dentro de una card (una card puede tener varias)
class RuleORM(SQLModel, table=True):
    __tablename__ = "rules"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID
    card_id: uuid.UUID = Field(foreign_key="cards.id")
    language_id: uuid.UUID = Field(foreign_key="languages.id")
    rule: str
    explanation: str

    card: "CardORM" = Relationship(back_populates="rules")
    language: LanguageORM = Relationship(back_populates="rules")
    examples: List["ExampleORM"] = Relationship(back_populates="rule")


class CardORM(SQLModel, table=True):
    __tablename__ = "cards"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID
    deck_id: uuid.UUID = Field(foreign_key="decks.id")
    card_type: CardType

    deck: DeckORM = Relationship(back_populates="cards")
    concepts: List[ConceptORM] = Relationship(back_populates="card")
    rules: List[RuleORM] = Relationship(back_populates="card")
    tags: List["TagORM"] = Relationship(back_populates="cards", link_model=CardTagORM)
    review_states: List["ReviewStateORM"] = Relationship(back_populates="card")


class TagORM(SQLModel, table=True):
    __tablename__ = "tags"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID
    key: str
    value: str

    cards: List["CardORM"] = Relationship(back_populates="tags", link_model=CardTagORM)


# Un ejemplo de uso — pertenece a un ConceptORM o a un RuleORM (no ambos)
class ExampleORM(SQLModel, table=True):
    __tablename__ = "examples"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    concept_id: Optional[uuid.UUID] = Field(default=None, foreign_key="concepts.id")
    rule_id: Optional[uuid.UUID] = Field(default=None, foreign_key="rules.id")
    example: str

    concept: Optional[ConceptORM] = Relationship(back_populates="examples")
    rule: Optional[RuleORM] = Relationship(back_populates="examples")


# Estado de repaso del usuario para cada card (spaced repetition)
class ReviewStateORM(SQLModel, table=True):
    __tablename__ = "review_states"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    card_id: uuid.UUID = Field(foreign_key="cards.id")
    user_id: uuid.UUID
    ease_factor: float = Field(default=2.5)
    interval_days: int = Field(default=0)
    due_date: date = Field(default_factory=date.today)
    repetitions: int = Field(default=0)
    last_reviewed: Optional[datetime] = None

    card: CardORM = Relationship(back_populates="review_states")

import uuid
from dataclasses import asdict
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from auth.dependencies import get_current_user_id
from db.db import get_session
from models.card import Card
from models.tag import Tag
from repositories.postgres_card_repository import PostgresCardRepository
from repositories.postgres_card_tag_repository import PostgresCardTagRepository
from repositories.postgres_tag_repository import PostgresTagRepository
from routes.concept import concept_to_read, get_concept_service
from routes.rule import get_rule_service, rule_to_read
from routes.tag import get_tag_service
from schemas.card import CardAddTags, CardCreate, CardRead, CardUpdate
from schemas.tag import TagRead
from services.card_service import CardService
from services.concept_service import ConceptService
from services.rule_service import RuleService
from services.tag_service import TagService

router = APIRouter(prefix="/cards", tags=["Cards"])


def get_card_service(session: Annotated[Session, Depends(get_session)]) -> CardService:
    return CardService(
        PostgresCardRepository(session),
        PostgresCardTagRepository(session),
        PostgresTagRepository(session),
    )


def _to_read(card: Card, tags: List[Tag], concept_service: ConceptService, rule_service: RuleService) -> CardRead:
    concepts = [
        concept_to_read(c, concept_service.get_examples(c.id))
        for c in concept_service.list_concepts_by_card(card.id)
    ]
    rules = [rule_to_read(r, rule_service.get_examples(r.id)) for r in rule_service.list_rules_by_card(card.id)]
    return CardRead(
        **asdict(card),
        tags=[TagRead(**asdict(tag)) for tag in tags],
        concepts=concepts,
        rules=rules,
    )


@router.post("/", response_model=CardRead, status_code=status.HTTP_201_CREATED)
def create_card(
    payload: CardCreate,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[CardService, Depends(get_card_service)],
    concept_service: Annotated[ConceptService, Depends(get_concept_service)],
    rule_service: Annotated[RuleService, Depends(get_rule_service)],
):
    data = payload.model_dump(exclude_none=True, exclude={"tag_ids"})
    card = Card(user_id=user_id, **data)
    created = service.create_card(card, payload.tag_ids)
    return _to_read(created, service.get_tags(created.id), concept_service, rule_service)


@router.get("/", response_model=list[CardRead])
def list_cards(
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[CardService, Depends(get_card_service)],
    concept_service: Annotated[ConceptService, Depends(get_concept_service)],
    rule_service: Annotated[RuleService, Depends(get_rule_service)],
):
    return [
        _to_read(card, service.get_tags(card.id), concept_service, rule_service)
        for card in service.list_cards(user_id)
    ]


@router.get("/{card_id}", response_model=CardRead)
def get_card(
    card_id: uuid.UUID,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[CardService, Depends(get_card_service)],
    concept_service: Annotated[ConceptService, Depends(get_concept_service)],
    rule_service: Annotated[RuleService, Depends(get_rule_service)],
):
    card = service.get_card(card_id)
    if card is None or card.user_id != user_id:
        raise HTTPException(status_code=404, detail="Card not found")
    return _to_read(card, service.get_tags(card_id), concept_service, rule_service)


@router.put("/{card_id}", response_model=CardRead)
def update_card(
    card_id: uuid.UUID,
    payload: CardUpdate,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[CardService, Depends(get_card_service)],
    concept_service: Annotated[ConceptService, Depends(get_concept_service)],
    rule_service: Annotated[RuleService, Depends(get_rule_service)],
):
    existing = service.get_card(card_id)
    if existing is None or existing.user_id != user_id:
        raise HTTPException(status_code=404, detail="Card not found")

    updated_data = {**asdict(existing), **payload.model_dump(exclude_none=True)}
    updated_card = Card(**updated_data)
    updated = service.update_card(card_id, updated_card)
    return _to_read(updated, service.get_tags(card_id), concept_service, rule_service)


@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_card(
    card_id: uuid.UUID,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[CardService, Depends(get_card_service)],
):
    existing = service.get_card(card_id)
    if existing is None or existing.user_id != user_id:
        raise HTTPException(status_code=404, detail="Card not found")
    service.delete_card(card_id)


@router.post("/{card_id}/tags", response_model=CardRead, status_code=status.HTTP_201_CREATED)
def add_tags(
    card_id: uuid.UUID,
    payload: CardAddTags,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[CardService, Depends(get_card_service)],
    tag_service: Annotated[TagService, Depends(get_tag_service)],
    concept_service: Annotated[ConceptService, Depends(get_concept_service)],
    rule_service: Annotated[RuleService, Depends(get_rule_service)],
):
    existing = service.get_card(card_id)
    if existing is None or existing.user_id != user_id:
        raise HTTPException(status_code=404, detail="Card not found")

    for tag_id in payload.tag_ids:
        tag = tag_service.get_tag(tag_id)
        if tag is None or tag.user_id != user_id:
            raise HTTPException(status_code=404, detail=f"Tag {tag_id} not found")

    service.add_tags(card_id, payload.tag_ids, user_id)
    return _to_read(existing, service.get_tags(card_id), concept_service, rule_service)

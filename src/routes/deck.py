import uuid
from dataclasses import asdict
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from auth.dependencies import get_current_user_id
from db.db import get_session
from models.deck import Deck
from repositories.postgres_deck_repository import PostgresDeckRepository
from schemas.deck import DeckCreate, DeckRead, DeckUpdate
from services.deck_service import DeckService

router = APIRouter(prefix="/decks", tags=["Decks"])


def get_deck_service(session: Annotated[Session, Depends(get_session)]) -> DeckService:
    repository = PostgresDeckRepository(session)
    return DeckService(repository)


@router.post("/", response_model=DeckRead, status_code=status.HTTP_201_CREATED)
def create_deck(
    payload: DeckCreate,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[DeckService, Depends(get_deck_service)],
):
    deck = Deck(user_id=user_id, **payload.model_dump(exclude_none=True))
    return service.create_deck(deck)


@router.get("/", response_model=list[DeckRead])
def list_decks(
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[DeckService, Depends(get_deck_service)],
):
    return service.list_decks(user_id)


@router.get("/{deck_id}", response_model=DeckRead)
def get_deck(
    deck_id: uuid.UUID,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[DeckService, Depends(get_deck_service)],
):
    deck = service.get_deck(deck_id)
    if deck is None or deck.user_id != user_id:
        raise HTTPException(status_code=404, detail="Deck not found")
    return deck


@router.put("/{deck_id}", response_model=DeckRead)
def update_deck(
    deck_id: uuid.UUID,
    payload: DeckUpdate,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[DeckService, Depends(get_deck_service)],
):
    existing = service.get_deck(deck_id)
    if existing is None or existing.user_id != user_id:
        raise HTTPException(status_code=404, detail="Deck not found")

    updated_data = {**asdict(existing), **payload.model_dump(exclude_none=True)}
    updated_deck = Deck(**updated_data)
    return service.update_deck(deck_id, updated_deck)


@router.delete("/{deck_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_deck(
    deck_id: uuid.UUID,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[DeckService, Depends(get_deck_service)],
):
    existing = service.get_deck(deck_id)
    if existing is None or existing.user_id != user_id:
        raise HTTPException(status_code=404, detail="Deck not found")
    service.delete_deck(deck_id)

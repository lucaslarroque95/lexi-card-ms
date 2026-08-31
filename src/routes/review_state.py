import uuid
from dataclasses import asdict
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from auth.dependencies import get_current_user_id
from db.db import get_session
from models.review_state import ReviewState
from repositories.postgres_review_state_repository import PostgresReviewStateRepository
from schemas.review_state import ReviewStateCreate, ReviewStateRead, ReviewStateUpdate
from services.review_state_service import ReviewStateService

router = APIRouter(prefix="/review-states", tags=["Review States"])


def get_review_state_service(session: Annotated[Session, Depends(get_session)]) -> ReviewStateService:
    repository = PostgresReviewStateRepository(session)
    return ReviewStateService(repository)


@router.post("/", response_model=ReviewStateRead, status_code=status.HTTP_201_CREATED)
def create_review_state(
    payload: ReviewStateCreate,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[ReviewStateService, Depends(get_review_state_service)],
):
    review_state = ReviewState(user_id=user_id, **payload.model_dump(exclude_none=True))
    return service.create_review_state(review_state)


@router.get("/", response_model=list[ReviewStateRead])
def list_review_states(
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[ReviewStateService, Depends(get_review_state_service)],
):
    return service.list_review_states(user_id)


@router.get("/{review_state_id}", response_model=ReviewStateRead)
def get_review_state(
    review_state_id: uuid.UUID,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[ReviewStateService, Depends(get_review_state_service)],
):
    review_state = service.get_review_state(review_state_id)
    if review_state is None or review_state.user_id != user_id:
        raise HTTPException(status_code=404, detail="Review state not found")
    return review_state


@router.put("/{review_state_id}", response_model=ReviewStateRead)
def update_review_state(
    review_state_id: uuid.UUID,
    payload: ReviewStateUpdate,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[ReviewStateService, Depends(get_review_state_service)],
):
    existing = service.get_review_state(review_state_id)
    if existing is None or existing.user_id != user_id:
        raise HTTPException(status_code=404, detail="Review state not found")

    updated_data = {**asdict(existing), **payload.model_dump(exclude_none=True)}
    updated_review_state = ReviewState(**updated_data)
    return service.update_review_state(review_state_id, updated_review_state)


@router.delete("/{review_state_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review_state(
    review_state_id: uuid.UUID,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[ReviewStateService, Depends(get_review_state_service)],
):
    existing = service.get_review_state(review_state_id)
    if existing is None or existing.user_id != user_id:
        raise HTTPException(status_code=404, detail="Review state not found")
    service.delete_review_state(review_state_id)

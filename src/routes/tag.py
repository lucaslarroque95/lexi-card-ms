import uuid
from dataclasses import asdict
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from auth.dependencies import get_current_user_id
from db.db import get_session
from models.tag import Tag
from repositories.postgres_tag_repository import PostgresTagRepository
from schemas.tag import TagCreate, TagRead, TagUpdate
from services.tag_service import TagService

router = APIRouter(prefix="/tags", tags=["Tags"])


def get_tag_service(session: Annotated[Session, Depends(get_session)]) -> TagService:
    repository = PostgresTagRepository(session)
    return TagService(repository)


@router.post("/", response_model=TagRead, status_code=status.HTTP_201_CREATED)
def create_tag(
    payload: TagCreate,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[TagService, Depends(get_tag_service)],
):
    tag = Tag(user_id=user_id, **payload.model_dump(exclude_none=True))
    return service.create_tag(tag)


@router.get("/", response_model=list[TagRead])
def list_tags(
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[TagService, Depends(get_tag_service)],
):
    return service.list_tags(user_id)


@router.get("/{tag_id}", response_model=TagRead)
def get_tag(
    tag_id: uuid.UUID,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[TagService, Depends(get_tag_service)],
):
    tag = service.get_tag(tag_id)
    if tag is None or tag.user_id != user_id:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.put("/{tag_id}", response_model=TagRead)
def update_tag(
    tag_id: uuid.UUID,
    payload: TagUpdate,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[TagService, Depends(get_tag_service)],
):
    existing = service.get_tag(tag_id)
    if existing is None or existing.user_id != user_id:
        raise HTTPException(status_code=404, detail="Tag not found")

    updated_data = {**asdict(existing), **payload.model_dump(exclude_none=True)}
    updated_tag = Tag(**updated_data)
    return service.update_tag(tag_id, updated_tag)


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(
    tag_id: uuid.UUID,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[TagService, Depends(get_tag_service)],
):
    existing = service.get_tag(tag_id)
    if existing is None or existing.user_id != user_id:
        raise HTTPException(status_code=404, detail="Tag not found")
    service.delete_tag(tag_id)

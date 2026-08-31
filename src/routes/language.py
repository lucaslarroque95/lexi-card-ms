import uuid
from dataclasses import asdict
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from auth.dependencies import get_current_user_id
from db.db import get_session
from models.language import Language
from repositories.postgres_language_repository import PostgresLanguageRepository
from repositories.postgres_user_language_repository import PostgresUserLanguageRepository
from schemas.language import LanguageCreate, LanguageRead, LanguageUpdate
from services.language_service import LanguageService

router = APIRouter(prefix="/languages", tags=["Languages"])


def get_language_service(session: Annotated[Session, Depends(get_session)]) -> LanguageService:
    return LanguageService(
        PostgresLanguageRepository(session),
        PostgresUserLanguageRepository(session),
    )


@router.post("/", response_model=LanguageRead, status_code=status.HTTP_201_CREATED)
def create_language(
    payload: LanguageCreate,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[LanguageService, Depends(get_language_service)],
):
    language = Language(user_id=user_id, name=payload.name, code=payload.code)
    return service.create_language(language, user_id, payload.started_at)


@router.get("/", response_model=list[LanguageRead])
def list_languages(
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[LanguageService, Depends(get_language_service)],
):
    return service.list_languages(user_id)


@router.get("/{language_id}", response_model=LanguageRead)
def get_language(
    language_id: uuid.UUID,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[LanguageService, Depends(get_language_service)],
):
    language = service.get_language(language_id)
    if language is None or language.user_id != user_id:
        raise HTTPException(status_code=404, detail="Language not found")
    return language


@router.put("/{language_id}", response_model=LanguageRead)
def update_language(
    language_id: uuid.UUID,
    payload: LanguageUpdate,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[LanguageService, Depends(get_language_service)],
):
    existing = service.get_language(language_id)
    if existing is None or existing.user_id != user_id:
        raise HTTPException(status_code=404, detail="Language not found")

    updated_data = {**asdict(existing), **payload.model_dump(exclude_none=True)}
    updated_language = Language(**updated_data)
    return service.update_language(language_id, updated_language)


@router.delete("/{language_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_language(
    language_id: uuid.UUID,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[LanguageService, Depends(get_language_service)],
):
    existing = service.get_language(language_id)
    if existing is None or existing.user_id != user_id:
        raise HTTPException(status_code=404, detail="Language not found")
    service.delete_language(language_id)

import uuid
from dataclasses import asdict
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from auth.dependencies import get_current_user_id
from db.db import get_session
from models.example import Example
from repositories.postgres_concept_repository import PostgresConceptRepository
from repositories.postgres_example_repository import PostgresExampleRepository
from repositories.postgres_rule_repository import PostgresRuleRepository
from schemas.example import ExampleCreate, ExampleRead, ExampleUpdate
from services.example_service import ExampleService

router = APIRouter(prefix="/examples", tags=["Examples"])


def get_example_service(session: Annotated[Session, Depends(get_session)]) -> ExampleService:
    return ExampleService(
        PostgresExampleRepository(session),
        PostgresConceptRepository(session),
        PostgresRuleRepository(session),
    )


@router.post("/", response_model=ExampleRead, status_code=status.HTTP_201_CREATED)
def create_example(
    payload: ExampleCreate,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[ExampleService, Depends(get_example_service)],
):
    if (payload.concept_id is None) == (payload.rule_id is None):
        raise HTTPException(status_code=400, detail="Debe indicarse exactamente uno de concept_id o rule_id")

    example = Example(example=payload.example, concept_id=payload.concept_id, rule_id=payload.rule_id)
    owner = service.get_owner(example)
    if owner is None or owner != user_id:
        raise HTTPException(status_code=404, detail="Concept or Rule not found")
    return service.create_example(example)


@router.get("/", response_model=list[ExampleRead])
def list_examples(
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[ExampleService, Depends(get_example_service)],
):
    return service.list_examples(user_id)


@router.get("/{example_id}", response_model=ExampleRead)
def get_example(
    example_id: uuid.UUID,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[ExampleService, Depends(get_example_service)],
):
    example = service.get_example(example_id)
    if example is None or service.get_owner(example) != user_id:
        raise HTTPException(status_code=404, detail="Example not found")
    return example


@router.put("/{example_id}", response_model=ExampleRead)
def update_example(
    example_id: uuid.UUID,
    payload: ExampleUpdate,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[ExampleService, Depends(get_example_service)],
):
    existing = service.get_example(example_id)
    if existing is None or service.get_owner(existing) != user_id:
        raise HTTPException(status_code=404, detail="Example not found")

    updated_data = {**asdict(existing), **payload.model_dump(exclude_none=True)}
    updated_example = Example(**updated_data)
    return service.update_example(example_id, updated_example)


@router.delete("/{example_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_example(
    example_id: uuid.UUID,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[ExampleService, Depends(get_example_service)],
):
    existing = service.get_example(example_id)
    if existing is None or service.get_owner(existing) != user_id:
        raise HTTPException(status_code=404, detail="Example not found")
    service.delete_example(example_id)

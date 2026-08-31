import uuid
from dataclasses import asdict
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from auth.dependencies import get_current_user_id
from db.db import get_session
from models.concept import Concept
from models.example import Example
from repositories.postgres_concept_repository import PostgresConceptRepository
from repositories.postgres_example_repository import PostgresExampleRepository
from schemas.concept import ConceptCreate, ConceptRead, ConceptUpdate
from schemas.example import ExampleRead, ExamplesAdd
from services.concept_service import ConceptService

router = APIRouter(prefix="/concepts", tags=["Concepts"])


def get_concept_service(session: Annotated[Session, Depends(get_session)]) -> ConceptService:
    return ConceptService(
        PostgresConceptRepository(session),
        PostgresExampleRepository(session),
    )


def concept_to_read(concept: Concept, examples: List[Example]) -> ConceptRead:
    return ConceptRead(**asdict(concept), examples=[ExampleRead(**asdict(e)) for e in examples])


@router.post("/", response_model=ConceptRead, status_code=status.HTTP_201_CREATED)
def create_concept(
    payload: ConceptCreate,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[ConceptService, Depends(get_concept_service)],
):
    data = payload.model_dump(exclude_none=True, exclude={"examples"})
    concept = Concept(user_id=user_id, **data)
    created = service.create_concept(concept, payload.examples)
    return concept_to_read(created, service.get_examples(created.id))


@router.get("/", response_model=list[ConceptRead])
def list_concepts(
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[ConceptService, Depends(get_concept_service)],
):
    return [concept_to_read(c, service.get_examples(c.id)) for c in service.list_concepts(user_id)]


@router.get("/{concept_id}", response_model=ConceptRead)
def get_concept(
    concept_id: uuid.UUID,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[ConceptService, Depends(get_concept_service)],
):
    concept = service.get_concept(concept_id)
    if concept is None or concept.user_id != user_id:
        raise HTTPException(status_code=404, detail="Concept not found")
    return concept_to_read(concept, service.get_examples(concept_id))


@router.put("/{concept_id}", response_model=ConceptRead)
def update_concept(
    concept_id: uuid.UUID,
    payload: ConceptUpdate,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[ConceptService, Depends(get_concept_service)],
):
    existing = service.get_concept(concept_id)
    if existing is None or existing.user_id != user_id:
        raise HTTPException(status_code=404, detail="Concept not found")

    updated_data = {**asdict(existing), **payload.model_dump(exclude_none=True)}
    updated_concept = Concept(**updated_data)
    updated = service.update_concept(concept_id, updated_concept)
    return concept_to_read(updated, service.get_examples(concept_id))


@router.delete("/{concept_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_concept(
    concept_id: uuid.UUID,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[ConceptService, Depends(get_concept_service)],
):
    existing = service.get_concept(concept_id)
    if existing is None or existing.user_id != user_id:
        raise HTTPException(status_code=404, detail="Concept not found")
    service.delete_concept(concept_id)


@router.post("/{concept_id}/examples", response_model=ConceptRead, status_code=status.HTTP_201_CREATED)
def add_examples(
    concept_id: uuid.UUID,
    payload: ExamplesAdd,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[ConceptService, Depends(get_concept_service)],
):
    existing = service.get_concept(concept_id)
    if existing is None or existing.user_id != user_id:
        raise HTTPException(status_code=404, detail="Concept not found")

    service.add_examples(concept_id, payload.examples)
    return concept_to_read(existing, service.get_examples(concept_id))

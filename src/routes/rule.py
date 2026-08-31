import uuid
from dataclasses import asdict
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from auth.dependencies import get_current_user_id
from db.db import get_session
from models.example import Example
from models.rule import Rule
from repositories.postgres_example_repository import PostgresExampleRepository
from repositories.postgres_rule_repository import PostgresRuleRepository
from schemas.example import ExampleRead, ExamplesAdd
from schemas.rule import RuleCreate, RuleRead, RuleUpdate
from services.rule_service import RuleService

router = APIRouter(prefix="/rules", tags=["Rules"])


def get_rule_service(session: Annotated[Session, Depends(get_session)]) -> RuleService:
    return RuleService(
        PostgresRuleRepository(session),
        PostgresExampleRepository(session),
    )


def rule_to_read(rule: Rule, examples: List[Example]) -> RuleRead:
    return RuleRead(**asdict(rule), examples=[ExampleRead(**asdict(e)) for e in examples])


@router.post("/", response_model=RuleRead, status_code=status.HTTP_201_CREATED)
def create_rule(
    payload: RuleCreate,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[RuleService, Depends(get_rule_service)],
):
    data = payload.model_dump(exclude_none=True, exclude={"examples"})
    rule = Rule(user_id=user_id, **data)
    created = service.create_rule(rule, payload.examples)
    return rule_to_read(created, service.get_examples(created.id))


@router.get("/", response_model=list[RuleRead])
def list_rules(
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[RuleService, Depends(get_rule_service)],
):
    return [rule_to_read(r, service.get_examples(r.id)) for r in service.list_rules(user_id)]


@router.get("/{rule_id}", response_model=RuleRead)
def get_rule(
    rule_id: uuid.UUID,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[RuleService, Depends(get_rule_service)],
):
    rule = service.get_rule(rule_id)
    if rule is None or rule.user_id != user_id:
        raise HTTPException(status_code=404, detail="Rule not found")
    return rule_to_read(rule, service.get_examples(rule_id))


@router.put("/{rule_id}", response_model=RuleRead)
def update_rule(
    rule_id: uuid.UUID,
    payload: RuleUpdate,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[RuleService, Depends(get_rule_service)],
):
    existing = service.get_rule(rule_id)
    if existing is None or existing.user_id != user_id:
        raise HTTPException(status_code=404, detail="Rule not found")

    updated_data = {**asdict(existing), **payload.model_dump(exclude_none=True)}
    updated_rule = Rule(**updated_data)
    updated = service.update_rule(rule_id, updated_rule)
    return rule_to_read(updated, service.get_examples(rule_id))


@router.delete("/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rule(
    rule_id: uuid.UUID,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[RuleService, Depends(get_rule_service)],
):
    existing = service.get_rule(rule_id)
    if existing is None or existing.user_id != user_id:
        raise HTTPException(status_code=404, detail="Rule not found")
    service.delete_rule(rule_id)


@router.post("/{rule_id}/examples", response_model=RuleRead, status_code=status.HTTP_201_CREATED)
def add_examples(
    rule_id: uuid.UUID,
    payload: ExamplesAdd,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
    service: Annotated[RuleService, Depends(get_rule_service)],
):
    existing = service.get_rule(rule_id)
    if existing is None or existing.user_id != user_id:
        raise HTTPException(status_code=404, detail="Rule not found")

    service.add_examples(rule_id, payload.examples)
    return rule_to_read(existing, service.get_examples(rule_id))

import uuid
from dataclasses import asdict
from typing import List, Optional

from sqlmodel import Session, select

from db.orm_models import RuleORM
from models.rule import Rule
from repositories.rule_repository import RuleRepository


class PostgresRuleRepository(RuleRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, rule: Rule) -> Rule:
        data = {k: v for k, v in asdict(rule).items() if k != "id"}
        orm_rule = RuleORM(**data)
        self.session.add(orm_rule)
        self.session.commit()
        self.session.refresh(orm_rule)
        return self._to_domain(orm_rule)

    def get(self, rule_id: uuid.UUID) -> Optional[Rule]:
        orm_rule = self.session.get(RuleORM, rule_id)
        return self._to_domain(orm_rule) if orm_rule else None

    def get_all(self) -> List[Rule]:
        orm_rules = self.session.exec(select(RuleORM)).all()
        return [self._to_domain(orm_rule) for orm_rule in orm_rules]

    def update(self, rule_id: uuid.UUID, rule: Rule) -> Optional[Rule]:
        orm_rule = self.session.get(RuleORM, rule_id)
        if orm_rule is None:
            return None

        for field, value in asdict(rule).items():
            if field != "id":
                setattr(orm_rule, field, value)

        self.session.add(orm_rule)
        self.session.commit()
        self.session.refresh(orm_rule)
        return self._to_domain(orm_rule)

    def delete(self, rule_id: uuid.UUID) -> bool:
        orm_rule = self.session.get(RuleORM, rule_id)
        if orm_rule is None:
            return False

        self.session.delete(orm_rule)
        self.session.commit()
        return True

    def get_by_user(self, user_id: uuid.UUID) -> List[Rule]:
        orm_rules = self.session.exec(select(RuleORM).where(RuleORM.user_id == user_id)).all()
        return [self._to_domain(orm_rule) for orm_rule in orm_rules]

    def get_by_card(self, card_id: uuid.UUID) -> List[Rule]:
        orm_rules = self.session.exec(select(RuleORM).where(RuleORM.card_id == card_id)).all()
        return [self._to_domain(orm_rule) for orm_rule in orm_rules]

    @staticmethod
    def _to_domain(orm_rule: RuleORM) -> Rule:
        return Rule(**orm_rule.model_dump())

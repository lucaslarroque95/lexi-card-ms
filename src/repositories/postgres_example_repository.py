import uuid
from dataclasses import asdict
from typing import List, Optional

from sqlmodel import Session, select

from db.orm_models import ExampleORM
from models.example import Example
from repositories.example_repository import ExampleRepository


class PostgresExampleRepository(ExampleRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, example: Example) -> Example:
        data = {k: v for k, v in asdict(example).items() if k != "id"}
        orm_example = ExampleORM(**data)
        self.session.add(orm_example)
        self.session.commit()
        self.session.refresh(orm_example)
        return self._to_domain(orm_example)

    def get(self, example_id: uuid.UUID) -> Optional[Example]:
        orm_example = self.session.get(ExampleORM, example_id)
        return self._to_domain(orm_example) if orm_example else None

    def get_all(self) -> List[Example]:
        orm_examples = self.session.exec(select(ExampleORM)).all()
        return [self._to_domain(orm_example) for orm_example in orm_examples]

    def update(self, example_id: uuid.UUID, example: Example) -> Optional[Example]:
        orm_example = self.session.get(ExampleORM, example_id)
        if orm_example is None:
            return None

        for field, value in asdict(example).items():
            if field != "id":
                setattr(orm_example, field, value)

        self.session.add(orm_example)
        self.session.commit()
        self.session.refresh(orm_example)
        return self._to_domain(orm_example)

    def delete(self, example_id: uuid.UUID) -> bool:
        orm_example = self.session.get(ExampleORM, example_id)
        if orm_example is None:
            return False

        self.session.delete(orm_example)
        self.session.commit()
        return True

    def get_by_concept(self, concept_id: uuid.UUID) -> List[Example]:
        orm_examples = self.session.exec(select(ExampleORM).where(ExampleORM.concept_id == concept_id)).all()
        return [self._to_domain(orm_example) for orm_example in orm_examples]

    def get_by_rule(self, rule_id: uuid.UUID) -> List[Example]:
        orm_examples = self.session.exec(select(ExampleORM).where(ExampleORM.rule_id == rule_id)).all()
        return [self._to_domain(orm_example) for orm_example in orm_examples]

    @staticmethod
    def _to_domain(orm_example: ExampleORM) -> Example:
        return Example(**orm_example.model_dump())

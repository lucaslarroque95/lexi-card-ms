import uuid
from dataclasses import asdict
from typing import List, Optional

from sqlmodel import Session, select

from db.orm_models import ConceptORM
from models.concept import Concept
from repositories.concept_repository import ConceptRepository


class PostgresConceptRepository(ConceptRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, concept: Concept) -> Concept:
        data = {k: v for k, v in asdict(concept).items() if k != "id"}
        orm_concept = ConceptORM(**data)
        self.session.add(orm_concept)
        self.session.commit()
        self.session.refresh(orm_concept)
        return self._to_domain(orm_concept)

    def get(self, concept_id: uuid.UUID) -> Optional[Concept]:
        orm_concept = self.session.get(ConceptORM, concept_id)
        return self._to_domain(orm_concept) if orm_concept else None

    def get_all(self) -> List[Concept]:
        orm_concepts = self.session.exec(select(ConceptORM)).all()
        return [self._to_domain(orm_concept) for orm_concept in orm_concepts]

    def update(self, concept_id: uuid.UUID, concept: Concept) -> Optional[Concept]:
        orm_concept = self.session.get(ConceptORM, concept_id)
        if orm_concept is None:
            return None

        for field, value in asdict(concept).items():
            if field != "id":
                setattr(orm_concept, field, value)

        self.session.add(orm_concept)
        self.session.commit()
        self.session.refresh(orm_concept)
        return self._to_domain(orm_concept)

    def delete(self, concept_id: uuid.UUID) -> bool:
        orm_concept = self.session.get(ConceptORM, concept_id)
        if orm_concept is None:
            return False

        self.session.delete(orm_concept)
        self.session.commit()
        return True

    def get_by_user(self, user_id: uuid.UUID) -> List[Concept]:
        orm_concepts = self.session.exec(select(ConceptORM).where(ConceptORM.user_id == user_id)).all()
        return [self._to_domain(orm_concept) for orm_concept in orm_concepts]

    def get_by_card(self, card_id: uuid.UUID) -> List[Concept]:
        orm_concepts = self.session.exec(select(ConceptORM).where(ConceptORM.card_id == card_id)).all()
        return [self._to_domain(orm_concept) for orm_concept in orm_concepts]

    @staticmethod
    def _to_domain(orm_concept: ConceptORM) -> Concept:
        return Concept(**orm_concept.model_dump())

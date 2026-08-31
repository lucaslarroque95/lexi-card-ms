import uuid
from abc import ABC, abstractmethod
from typing import List, Optional

from models.rule import Rule


class RuleRepository(ABC):
    @abstractmethod
    def create(self, rule: Rule) -> Rule: ...

    @abstractmethod
    def get(self, rule_id: uuid.UUID) -> Optional[Rule]: ...

    @abstractmethod
    def get_all(self) -> List[Rule]: ...

    @abstractmethod
    def update(self, rule_id: uuid.UUID, rule: Rule) -> Optional[Rule]: ...

    @abstractmethod
    def delete(self, rule_id: uuid.UUID) -> bool: ...

    @abstractmethod
    def get_by_user(self, user_id: uuid.UUID) -> List[Rule]: ...

    @abstractmethod
    def get_by_card(self, card_id: uuid.UUID) -> List[Rule]: ...

import uuid
from abc import ABC, abstractmethod
from typing import List, Optional

from models.example import Example


class ExampleRepository(ABC):
    @abstractmethod
    def create(self, example: Example) -> Example: ...

    @abstractmethod
    def get(self, example_id: uuid.UUID) -> Optional[Example]: ...

    @abstractmethod
    def get_all(self) -> List[Example]: ...

    @abstractmethod
    def update(self, example_id: uuid.UUID, example: Example) -> Optional[Example]: ...

    @abstractmethod
    def delete(self, example_id: uuid.UUID) -> bool: ...

    @abstractmethod
    def get_by_concept(self, concept_id: uuid.UUID) -> List[Example]: ...

    @abstractmethod
    def get_by_rule(self, rule_id: uuid.UUID) -> List[Example]: ...

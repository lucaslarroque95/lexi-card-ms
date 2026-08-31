import uuid
from typing import List, Optional

from models.tag import Tag
from repositories.tag_repository import TagRepository


class TagService:
    def __init__(self, repository: TagRepository):
        self.repository = repository

    def create_tag(self, tag: Tag) -> Tag:
        return self.repository.create(tag)

    def get_tag(self, tag_id: uuid.UUID) -> Optional[Tag]:
        return self.repository.get(tag_id)

    def list_tags(self, user_id: uuid.UUID) -> List[Tag]:
        return self.repository.get_by_user(user_id)

    def update_tag(self, tag_id: uuid.UUID, tag: Tag) -> Optional[Tag]:
        return self.repository.update(tag_id, tag)

    def delete_tag(self, tag_id: uuid.UUID) -> bool:
        return self.repository.delete(tag_id)

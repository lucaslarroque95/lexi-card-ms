import uuid

from fakes import FakeCardTagRepository, FakeTagRepository
from models.tag import Tag
from services.tag_service import TagService


def make_service():
    return TagService(FakeTagRepository(FakeCardTagRepository()))


def test_create_get_update_delete_tag():
    service = make_service()
    user_id = uuid.uuid4()
    created = service.create_tag(Tag(user_id=user_id, key="level", value="A1"))

    assert service.get_tag(created.id) == created

    updated = service.update_tag(created.id, Tag(user_id=user_id, key="level", value="A2", id=created.id))
    assert updated.value == "A2"

    assert service.delete_tag(created.id) is True
    assert service.get_tag(created.id) is None
    assert service.delete_tag(uuid.uuid4()) is False


def test_list_tags_scoped_to_user():
    service = make_service()
    user_a, user_b = uuid.uuid4(), uuid.uuid4()
    service.create_tag(Tag(user_id=user_a, key="a", value="1"))
    service.create_tag(Tag(user_id=user_b, key="b", value="2"))

    assert len(service.list_tags(user_a)) == 1

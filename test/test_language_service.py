import uuid
from datetime import datetime

from fakes import FakeLanguageRepository, FakeUserLanguageRepository
from models.language import Language
from services.language_service import LanguageService


def make_service():
    return LanguageService(FakeLanguageRepository(), FakeUserLanguageRepository())


def test_create_language_auto_creates_user_language():
    service = make_service()
    user_id = uuid.uuid4()

    created = service.create_language(Language(user_id=user_id, name="English", code="en"), user_id)

    assert created.id is not None
    user_languages = service.user_language_repository.get_all()
    assert len(user_languages) == 1
    assert user_languages[0].user_id == user_id
    assert user_languages[0].language_id == created.id
    assert isinstance(user_languages[0].started_at, datetime)


def test_create_language_uses_explicit_started_at():
    service = make_service()
    user_id = uuid.uuid4()
    started_at = datetime(2020, 1, 1)

    service.create_language(Language(user_id=user_id, name="English", code="en"), user_id, started_at)

    assert service.user_language_repository.get_all()[0].started_at == started_at


def test_list_languages_scoped_to_user():
    service = make_service()
    user_a, user_b = uuid.uuid4(), uuid.uuid4()
    service.create_language(Language(user_id=user_a, name="English", code="en"), user_a)
    service.create_language(Language(user_id=user_b, name="Spanish", code="es"), user_b)

    assert [lang.name for lang in service.list_languages(user_a)] == ["English"]
    assert [lang.name for lang in service.list_languages(user_b)] == ["Spanish"]


def test_get_update_delete_language():
    service = make_service()
    user_id = uuid.uuid4()
    created = service.create_language(Language(user_id=user_id, name="English", code="en"), user_id)

    assert service.get_language(created.id) == created

    updated = service.update_language(
        created.id, Language(user_id=user_id, name="British English", code="en", id=created.id)
    )
    assert updated.name == "British English"

    assert service.delete_language(created.id) is True
    assert service.get_language(created.id) is None
    assert service.delete_language(uuid.uuid4()) is False

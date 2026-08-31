import uuid

import pytest
from fastapi import HTTPException

from auth.dependencies import get_current_user_id


class _State:
    pass


class _FakeRequest:
    def __init__(self):
        self.state = _State()


def test_get_current_user_id_valid():
    request = _FakeRequest()
    user_id = uuid.uuid4()
    request.state.user_id = str(user_id)

    assert get_current_user_id(request) == user_id


def test_get_current_user_id_missing_raises_401():
    request = _FakeRequest()

    with pytest.raises(HTTPException) as exc_info:
        get_current_user_id(request)

    assert exc_info.value.status_code == 401


def test_get_current_user_id_malformed_raises_401():
    request = _FakeRequest()
    request.state.user_id = "not-a-uuid"

    with pytest.raises(HTTPException) as exc_info:
        get_current_user_id(request)

    assert exc_info.value.status_code == 401

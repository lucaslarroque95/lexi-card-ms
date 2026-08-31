import asyncio
import time
import uuid

import jwt as pyjwt
import pytest
from fastapi import HTTPException
from rsa_keys import generate_keypair
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

import auth.jwt as auth_jwt
from middlewares.auth import AuthMiddleware, require_role


async def _public_endpoint(request):
    return JSONResponse({"ok": True})


async def _protected_endpoint(request):
    return JSONResponse({"user_id": getattr(request.state, "user_id", None)})


def _build_app():
    app = Starlette(routes=[
        Route("/health/", _public_endpoint),
        Route("/protected", _protected_endpoint),
    ])
    app.add_middleware(AuthMiddleware)
    return app


async def _call(app, method, path, headers=None):
    scope = {
        "type": "http",
        "method": method,
        "path": path,
        "raw_path": path.encode(),
        "query_string": b"",
        "headers": [(k.lower().encode(), v.encode()) for k, v in (headers or {}).items()],
        "client": ("test", 123),
        "server": ("test", 80),
        "scheme": "http",
        "http_version": "1.1",
    }
    messages = []

    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message):
        messages.append(message)

    await app(scope, receive, send)
    status = next(m["status"] for m in messages if m["type"] == "http.response.start")
    body = b"".join(m.get("body", b"") for m in messages if m["type"] == "http.response.body")
    return status, body


@pytest.fixture(scope="module")
def keypair():
    return generate_keypair()


@pytest.fixture(autouse=True)
def patch_public_key(keypair, monkeypatch):
    _, public_pem = keypair
    monkeypatch.setattr(auth_jwt, "_PUBLIC_KEY", public_pem)


def test_public_path_bypasses_auth():
    status, _ = asyncio.run(_call(_build_app(), "GET", "/health/"))
    assert status == 200


def test_protected_path_without_token_is_401():
    status, _ = asyncio.run(_call(_build_app(), "GET", "/protected"))
    assert status == 401


def test_protected_path_with_garbage_token_is_401():
    status, _ = asyncio.run(_call(_build_app(), "GET", "/protected", {"Authorization": "garbage"}))
    assert status == 401


def test_protected_path_with_expired_token_is_401(keypair):
    private_pem, _ = keypair
    token = pyjwt.encode({"userId": str(uuid.uuid4()), "exp": int(time.time()) - 10}, private_pem, algorithm="RS256")

    status, _ = asyncio.run(_call(_build_app(), "GET", "/protected", {"Authorization": token}))
    assert status == 401


def test_protected_path_with_valid_token_sets_request_state(keypair):
    private_pem, _ = keypair
    user_id = str(uuid.uuid4())
    token = pyjwt.encode({"userId": user_id, "role": "user", "exp": int(time.time()) + 3600}, private_pem, algorithm="RS256")

    status, body = asyncio.run(_call(_build_app(), "GET", "/protected", {"Authorization": token}))

    assert status == 200
    assert user_id.encode() in body


class _State:
    pass


class _FakeRequest:
    def __init__(self, roles=None):
        self.state = _State()
        if roles is not None:
            self.state.roles = roles


def test_require_role_allows_when_role_present():
    check = require_role("admin")
    check(_FakeRequest(roles=["user", "admin"]))  # no debe lanzar


def test_require_role_blocks_when_role_missing():
    check = require_role("admin")
    with pytest.raises(HTTPException) as exc_info:
        check(_FakeRequest(roles=["user"]))
    assert exc_info.value.status_code == 403


def test_require_role_blocks_when_no_roles_set_at_all():
    check = require_role("admin")
    with pytest.raises(HTTPException) as exc_info:
        check(_FakeRequest())
    assert exc_info.value.status_code == 403

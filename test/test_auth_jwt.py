import time
import uuid

import jwt as pyjwt
import pytest
from rsa_keys import generate_keypair

import auth.jwt as auth_jwt


@pytest.fixture(scope="module")
def keypair():
    return generate_keypair()


@pytest.fixture(autouse=True)
def patch_public_key(keypair, monkeypatch):
    _, public_pem = keypair
    monkeypatch.setattr(auth_jwt, "_PUBLIC_KEY", public_pem)


def make_token(private_pem, claims):
    return pyjwt.encode(claims, private_pem, algorithm="RS256")


def test_verify_token_valid(keypair):
    private_pem, _ = keypair
    user_id = str(uuid.uuid4())
    token = make_token(private_pem, {"userId": user_id, "role": "user,admin", "exp": int(time.time()) + 3600})

    user = auth_jwt.verify_token(token)

    assert user.user_id == user_id
    assert user.roles == ["user", "admin"]


def test_verify_token_no_role_claim(keypair):
    private_pem, _ = keypair
    user_id = str(uuid.uuid4())
    token = make_token(private_pem, {"userId": user_id, "exp": int(time.time()) + 3600})

    user = auth_jwt.verify_token(token)

    assert user.roles == []


def test_verify_token_single_role(keypair):
    private_pem, _ = keypair
    token = make_token(private_pem, {"userId": str(uuid.uuid4()), "role": "admin", "exp": int(time.time()) + 3600})

    user = auth_jwt.verify_token(token)

    assert user.roles == ["admin"]


def test_verify_token_expired(keypair):
    private_pem, _ = keypair
    token = make_token(private_pem, {"userId": str(uuid.uuid4()), "exp": int(time.time()) - 10})

    with pytest.raises(auth_jwt.InvalidTokenError):
        auth_jwt.verify_token(token)


def test_verify_token_tampered_signature(keypair):
    private_pem, _ = keypair
    token = make_token(private_pem, {"userId": str(uuid.uuid4()), "exp": int(time.time()) + 3600})

    with pytest.raises(auth_jwt.InvalidTokenError):
        auth_jwt.verify_token(token[:-4] + "abcd")


def test_verify_token_signed_with_wrong_key():
    other_private_pem, _ = generate_keypair()
    token = make_token(other_private_pem, {"userId": str(uuid.uuid4()), "exp": int(time.time()) + 3600})

    with pytest.raises(auth_jwt.InvalidTokenError):
        auth_jwt.verify_token(token)


def test_verify_token_missing_user_id_claim(keypair):
    private_pem, _ = keypair
    token = make_token(private_pem, {"exp": int(time.time()) + 3600})

    with pytest.raises(auth_jwt.InvalidTokenError):
        auth_jwt.verify_token(token)


def test_verify_token_non_string_user_id_claim(keypair):
    private_pem, _ = keypair
    token = make_token(private_pem, {"userId": 12345, "exp": int(time.time()) + 3600})

    with pytest.raises(auth_jwt.InvalidTokenError):
        auth_jwt.verify_token(token)


def test_verify_token_garbage_input():
    with pytest.raises(auth_jwt.InvalidTokenError):
        auth_jwt.verify_token("not-a-jwt-at-all")

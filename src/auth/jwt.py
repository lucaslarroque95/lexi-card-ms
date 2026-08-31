import os
from dataclasses import dataclass
from typing import List

import jwt
from dotenv import load_dotenv

load_dotenv()

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_PUBLIC_KEY_PATH = os.environ.get("JWT_PUBLIC_KEY_PATH", os.path.join(_BASE_DIR, "keys", "public.pem"))

with open(_PUBLIC_KEY_PATH, "rb") as _key_file:
    _PUBLIC_KEY = _key_file.read()


class InvalidTokenError(Exception):
    pass


@dataclass(frozen=True)
class AuthenticatedUser:
    user_id: str
    roles: List[str]


def verify_token(token: str) -> AuthenticatedUser:
    """Valida el JWT RS256 emitido por lexi-users-ms con su clave pública."""
    try:
        claims = jwt.decode(token, _PUBLIC_KEY, algorithms=["RS256"])
    except jwt.PyJWTError as exc:
        raise InvalidTokenError(str(exc)) from exc

    user_id = claims.get("userId")
    if not isinstance(user_id, str):
        raise InvalidTokenError("invalid userId claim")

    role_claim = claims.get("role") or ""
    roles = role_claim.split(",") if role_claim else []

    return AuthenticatedUser(user_id=user_id, roles=roles)

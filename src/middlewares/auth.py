from typing import Awaitable, Callable

from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from auth.jwt import InvalidTokenError, verify_token

PUBLIC_PATHS = {
    "/",
    "/health/",
    "/docs",
    "/docs/oauth2-redirect",
    "/redoc",
    "/openapi.json",
}


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable]):
        root_path = request.scope.get("root_path", "")
        path = request.url.path
        if root_path and path.startswith(root_path):
            path = path[len(root_path):] or "/"
        if path in PUBLIC_PATHS:
            return await call_next(request)

        token = request.headers.get("Authorization")
        if not token:
            return JSONResponse({"message": "Not authorized"}, status_code=401)

        try:
            user = verify_token(token)
        except InvalidTokenError:
            return JSONResponse({"message": "Not authorized"}, status_code=401)

        request.state.user_id = user.user_id
        request.state.roles = user.roles
        return await call_next(request)


def require_role(role: str):
    """Dependency para restringir un endpoint puntual a un rol (equivalente a RequireRole en Go)."""

    def _check(request: Request) -> None:
        roles = getattr(request.state, "roles", [])
        if role not in roles:
            raise HTTPException(status_code=403, detail="Forbidden")

    return _check

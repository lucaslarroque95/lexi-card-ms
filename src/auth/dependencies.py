import uuid

from fastapi import HTTPException, Request


def get_current_user_id(request: Request) -> uuid.UUID:
    """El userId que puso AuthMiddleware en request.state tras validar el JWT."""
    raw_user_id = getattr(request.state, "user_id", None)
    if raw_user_id is None:
        raise HTTPException(status_code=401, detail="Not authorized")

    try:
        return uuid.UUID(raw_user_id)
    except ValueError:
        raise HTTPException(status_code=401, detail="Not authorized")

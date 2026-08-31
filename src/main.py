import os

import uvicorn
from fastapi import Depends, FastAPI
from routes import (
    card,
    concept,
    deck,
    example,
    health,
    language,
    review_state,
    root,
    rule,
    tag,
)

from auth.security import authorization_scheme
from db.db import create_db_and_tables
from middlewares.auth import AuthMiddleware

app = FastAPI(root_path=os.getenv("ROOT_PATH", ""))

app.title = "Vocabulary MS"
app.version = "1.0.0"

app.add_middleware(AuthMiddleware)

protected = [Depends(authorization_scheme)]

app.include_router(root.router)
app.include_router(health.router)
app.include_router(language.router, dependencies=protected)
app.include_router(deck.router, dependencies=protected)
app.include_router(concept.router, dependencies=protected)
app.include_router(rule.router, dependencies=protected)
app.include_router(card.router, dependencies=protected)
app.include_router(tag.router, dependencies=protected)
app.include_router(example.router, dependencies=protected)
app.include_router(review_state.router, dependencies=protected)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

import os

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

# Importado por su efecto secundario: registra todas las tablas
# (CardORM, DeckORM, LanguageORM, etc.) en SQLModel.metadata.
from db import orm_models  # noqa: F401

load_dotenv()

POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_SERVER = os.environ["POSTGRES_SERVER"]
POSTGRES_PORT = os.environ["POSTGRES_PORT"]
POSTGRES_DB = os.environ["POSTGRES_DB"]

url = (
    f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

engine = create_engine(url)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

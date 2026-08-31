# Arquitectura

`src/` está organizado en capas. Cada carpeta tiene su propio `README.md`
con las reglas puntuales; este documento explica cómo se conectan entre
sí y cuál es el camino real que sigue un request.

## Capas

    Cliente (HTTP)
        |
        v
    routes/            <-- valida con schemas/, traduce schema <-> models.Card
        |
        v  (models.Card)
    services/           <-- lógica de negocio, solo conoce la INTERFAZ de repositories/
        |
        v  (models.Card)
    repositories/        <-- interfaz CardRepository
        |
        v  implementada por
    PostgresCardRepository  <-- traduce models.Card <-> db/orm_models.CardORM
        |
        v
    db/                 <-- engine/session (SQLAlchemy), Postgres

| Carpeta | Sabe de | No sabe de |
|---|---|---|
| `routes/` | FastAPI, `schemas/`, `services/` | SQL, ORM, Postgres |
| `schemas/` | Pydantic (contratos HTTP) | `services/`, `repositories/`, DB |
| `services/` | `models/` (dominio), `repositories.CardRepository` (interfaz) | FastAPI, Pydantic, SQL, Postgres |
| `models/` | Nada (solo Python estándar) | Todo lo demás |
| `repositories/` | `models/` + la interfaz propia; la implementación concreta además conoce `db/` | `schemas/`, FastAPI |
| `db/` | SQLAlchemy/SQLModel, Postgres | `services/`, `routes/`, `schemas/` |

La dependencia siempre apunta "hacia adentro": `routes` depende de
`services`, `services` depende de la *interfaz* de `repositories`, nunca
al revés. `models/` no depende de nada — es el centro. Esto es
**Dependency Inversion**: la capa de negocio (`services`) no conoce
Postgres, conoce un contrato (`CardRepository`) que Postgres cumple.

## Camino de una función: `POST /cards/`

    Cliente
      | POST /cards/  (JSON)
      v
    routes/cards.py : create_card(payload: CardCreate)
      | FastAPI ya validó el body contra schemas/card.py:CardCreate
      | payload -> Card(**payload.model_dump())         [models/card.py]
      v
    services/card_service.py : CardService.create_card(card)
      | self.repository.create(card)   -- repository es CardRepository (interfaz)
      v
    repositories/postgres_card_repository.py : PostgresCardRepository.create(card)
      | Card -> CardORM                                 [db/orm_models.py]
      | session.add(orm_card); session.commit(); session.refresh(orm_card)
      v
    db/db.py (engine + Session) --> Postgres
      | INSERT INTO cards (...)
      v
    Postgres devuelve la fila con id generado
      |
      v (subiendo)
    PostgresCardRepository: CardORM -> Card (dominio)   -- nunca deja escapar un CardORM
      |
      v
    CardService: devuelve el mismo Card sin tocarlo (todavía no hay lógica de negocio extra)
      |
      v
    routes/cards.py: FastAPI serializa Card -> CardRead  [schemas/card.py], responde 201
      |
      v
    Cliente recibe el JSON

Paso a paso, con archivos y funciones concretas:

1. **`routes/cards.py: create_card`** recibe `payload: CardCreate`
   (validado automáticamente por FastAPI contra `schemas/card.py`).
2. Lo convierte a dominio: `card = Card(**payload.model_dump())`
   (`models/card.py`).
3. Llama a `service.create_card(card)`. El `service` fue inyectado por
   `Depends(get_card_service)`, que en ese mismo archivo arma
   `CardService(PostgresCardRepository(session))` — este es el único
   punto donde se decide *qué implementación concreta* del repositorio
   se usa.
4. **`services/card_service.py: create_card`** no hace nada de negocio
   extra todavía (es un passthrough) y delega directo en
   `self.repository.create(card)`. `self.repository` es de tipo
   `CardRepository` (la interfaz) — el servicio no sabe que del otro
   lado hay Postgres.
5. **`repositories/postgres_card_repository.py: create`** es donde
   realmente se toca la base: convierte el `Card` de dominio a un
   `CardORM` (`db/orm_models.py`), lo agrega a la `Session` (`db/db.py:
   get_session`) y hace `commit()` + `refresh()` para traer el `id`
   generado por Postgres. Convierte el resultado de vuelta a `Card` de
   dominio antes de devolverlo (nunca deja escapar un `CardORM` fuera de
   esta capa).
6. La respuesta sube sin cambios por `service` hasta `routes`, donde
   FastAPI la serializa usando `response_model=CardRead`
   (`schemas/card.py`) — ahí es donde el objeto de dominio se traduce al
   contrato público de la API.

El resto de los endpoints (`GET /cards/`, `GET /cards/{id}`,
`PUT /cards/{id}`, `DELETE /cards/{id}`) siguen exactamente el mismo
camino, solo cambia qué método de `CardRepository` se invoca
(`get_all`, `get`, `update`, `delete`).

## Qué cambia si se reemplaza Postgres

Solo `db/` y `repositories/postgres_card_repository.py` (o su
equivalente nuevo, p. ej. `repositories/mongo_card_repository.py`).
`models/`, `schemas/`, `services/` y `routes/` quedan intactos — lo
único que se toca ahí es una línea en
`routes/cards.py: get_card_service`, que pasa a instanciar el
repositorio nuevo.

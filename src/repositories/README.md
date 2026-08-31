# repositories/

Implementa el **patrón Repository**: abstrae el acceso a datos detrás de
una interfaz que habla en términos de `models/` (dominio), no de tablas.

- `card_repository.py`: interfaz (`ABC`) con el contrato — `create`, `get`,
  `get_all`, `update`, `delete`. Esto es lo único que `services/` conoce.
- `postgres_card_repository.py`: implementación concreta que usa
  `db/orm_models.py` y una `Session` de SQLAlchemy para cumplir ese
  contrato contra Postgres. Convierte entre `CardORM` (persistencia) y
  `Card` (dominio) en los bordes de cada método.

## Reglas

- Un repositorio siempre recibe y devuelve objetos de `models/`, nunca
  objetos de `db/orm_models.py` ni de `schemas/`.
- Toda query (SQL, ORM, lo que sea) vive acá adentro. `services/` no debe
  importar `sqlmodel`, `select`, `Session`, etc.

## Por qué

Este es el punto de **inversión de dependencias** que hace que el resto
de la app sea independiente de la tecnología: si el día de mañana se
cambia Postgres por otra base, se agrega una nueva clase (p. ej.
`MongoCardRepository`) que cumpla la misma interfaz, y solo cambia el
`Depends` en `routes/` que decide cuál instanciar. `services/` y
`routes/` no se tocan.

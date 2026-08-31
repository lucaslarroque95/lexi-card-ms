# db/

Infraestructura de persistencia. Es la **única** carpeta del proyecto que
sabe que la base de datos es Postgres.

- `db.py`: crea el `engine` a partir de variables de entorno (`.env`) y
  expone `get_session()`, una dependencia de FastAPI que entrega una
  `Session` de SQLAlchemy/SQLModel por request.
- `orm_models.py`: modelos `SQLModel(table=True)` que mapean 1:1 a las
  tablas reales. Son distintos de `models/` (dominio) y de `schemas/`
  (API): estos conocen columnas, tipos de columna, claves primarias, etc.

## Reglas

- Nada fuera de `repositories/` debería importar `orm_models.py` o
  `db.py` directamente. `services/` y `routes/` no deben saber que existe
  SQLAlchemy.
- Si en el futuro se cambia de motor (Mongo, DynamoDB, etc.), se agrega
  una carpeta nueva equivalente (p. ej. `mongo/`) y una implementación de
  repositorio nueva; esta carpeta puede convivir o desaparecer sin tocar
  `services/` ni `routes/`.

## Por qué

Aislar el ORM acá es lo que permite que el resto de la app no dependa de
la tecnología subyacente (patrón: **Dependency Inversion** vía
`repositories/`).

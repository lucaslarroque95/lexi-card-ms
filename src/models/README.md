# models/

Entidades de **dominio**: representan los conceptos del negocio (`Card`, etc.)
tal como los entiende la aplicación, sin ninguna relación con HTTP, la base
de datos o un ORM en particular.

## Reglas

- No importar `fastapi`, `sqlmodel`, `sqlalchemy` ni `pydantic` acá. Usar
  `dataclasses` o clases planas de Python.
- No tienen métodos de persistencia (`save()`, `create()`...). Eso vive en
  `repositories/`.
- Son el "idioma común" entre `services/` y `repositories/`: los
  repositorios reciben y devuelven estos objetos, nunca modelos de ORM ni
  schemas de API.

## Por qué

Si mañana cambia la base de datos (Postgres → Mongo) o el framework web,
esta carpeta no se toca. Es la parte más estable del proyecto porque
describe el negocio, no la infraestructura.

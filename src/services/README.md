# services/

Lógica de negocio y casos de uso. Es la capa donde vive todo lo que es
más que un simple CRUD: validaciones cruzadas, reglas del dominio,
orquestación de varios repositorios, efectos secundarios, etc.

- `card_service.py`: recibe un `CardRepository` (la interfaz, no una
  implementación concreta) por constructor — **inyección de
  dependencias** — y expone métodos de caso de uso (`create_card`,
  `list_cards`...).

## Reglas

- Solo conoce `models/` (dominio) y las interfaces de `repositories/`.
  Nunca importa `fastapi`, `sqlmodel`, `schemas/` ni `db/`.
- Si hoy un método es un simple passthrough al repositorio (como acá),
  está bien: el valor de esta capa es tener un lugar único donde crecer
  reglas de negocio sin tocar `routes/` ni `repositories/`.
- Se testea con un repositorio falso/en memoria que implemente
  `CardRepository`, sin levantar una base de datos real.

## Por qué

Separar esto de `routes/` permite reusar la misma lógica desde otro
lugar (un job, un CLI, otro protocolo) sin depender de FastAPI.

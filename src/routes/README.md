# routes/

Capa HTTP (FastAPI `APIRouter`). Traduce entre el mundo HTTP
(`schemas/`) y el mundo de negocio (`services/` + `models/`).

## Qué hace un endpoint acá

1. Recibe un `schemas.CardCreate`/`CardUpdate` validado por FastAPI.
2. Lo convierte a un `models.Card` (dominio).
3. Llama al método correspondiente del `service` (inyectado por
   `Depends`).
4. Devuelve el resultado (FastAPI lo serializa con `response_model`,
   normalmente un `schemas.CardRead`).
5. Traduce errores/estados de negocio a códigos HTTP (`404`, `409`, etc.)
   con `HTTPException`.

## Reglas

- Cero lógica de negocio acá: si hay un `if` que decide algo del dominio
  (no relacionado a HTTP), va en `services/`.
- La única función "de infraestructura" permitida en este archivo es el
  *provider* (`get_card_service`), que decide qué implementación
  concreta de repositorio se inyecta. Es el único lugar, junto con
  `main.py`, que conecta todas las capas entre sí.

## Por qué

Mantener las rutas finas hace que sean triviales de testear (o de
reemplazar por otro transporte, como un CLI o un worker) sin duplicar
lógica de negocio.

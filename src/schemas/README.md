# schemas/

DTOs (Data Transfer Objects) de la **API**: lo que un cliente HTTP manda y
recibe. Son clases Pydantic (`BaseModel`), a diferencia de `models/` que son
dataclasses de dominio.

## Convención

Por cada entidad, separar por intención en vez de tener un único schema:

- `<Entidad>Create`: campos requeridos para crear (sin `id`).
- `<Entidad>Update`: todos los campos opcionales (para PATCH/PUT parcial).
- `<Entidad>Read`: lo que se devuelve al cliente (incluye `id`).

## Reglas

- Solo se usan en `routes/`, para validar el request y serializar la
  respuesta (`response_model=...`). `services/` y `repositories/` no deben
  conocer estas clases.
- No poner lógica de negocio acá, solo validación de forma (tipos,
  campos requeridos).

## Por qué

Separar esto de `models/` evita que un cambio en la tabla de la base de
datos rompa el contrato público de la API, y viceversa: podés exponer menos
campos de los que existen en el dominio, o renombrarlos, sin tocar la
lógica interna.

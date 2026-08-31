from fastapi.security import APIKeyHeader

# Declarado únicamente para que FastAPI documente el requisito de auth en
# Swagger (botón "Authorize") y agregue el header a cada request de prueba.
# La validación real del JWT la hace middlewares/auth.py.
authorization_scheme = APIKeyHeader(
    name="Authorization",
    description='JWT RS256 emitido por lexi-users-ms (sin prefijo "Bearer ").',
    auto_error=False,
)

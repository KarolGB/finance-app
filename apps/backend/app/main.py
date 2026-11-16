from fastapi import FastAPI
from .core.config import settings
app = FastAPI(
    title="finance-app API",
    docs_url="/docs" if settings.environment == "DEVELOPMENT" else None,
    openapi_url="/openapi.json" if settings.environment == "DEVELOPMENT" else None,
    redoc_url="/redoc" if settings.environment == "DEVELOPMENT" else None
)


@app.get("/health")
def health() -> dict[str,str]:
    return {"status":"ok"}
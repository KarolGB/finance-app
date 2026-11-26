from fastapi import FastAPI
from .core.config import settings
from .auth.router import router as auth_router
from .users.router import router as user_router
from .workspaces.router import router as workspace_router
app = FastAPI(
    title="finance-app API",
    docs_url="/docs" if settings.environment == "DEVELOPMENT" else None,
    openapi_url="/openapi.json" if settings.environment == "DEVELOPMENT" else None,
    redoc_url="/redoc" if settings.environment == "DEVELOPMENT" else None
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(workspace_router)

@app.get("/health")
def health() -> dict[str,str]:
    return {"status":"ok"}
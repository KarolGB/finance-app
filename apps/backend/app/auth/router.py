from fastapi import APIRouter
from ..core.deps import dbSession
from .schema import RegisterSchema, AuthResponse, LoginScheme, RefreshRequest
from .service import register_user, login_user, refresh_tokens, logout_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register(userData : RegisterSchema , db : dbSession) -> AuthResponse:
    return register_user(userData,db)

@router.post("/login")
def login(userData : LoginScheme, db : dbSession) -> AuthResponse:
    return login_user(userData, db)

@router.post("/refresh")
def refresh(data : RefreshRequest, db : dbSession) -> AuthResponse:
    return refresh_tokens(data.refresh_token, db)

@router.post("/logout")
def logout(data : RefreshRequest, db : dbSession) -> dict[str, str]:
    return logout_user(data.refresh_token, db)
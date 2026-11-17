from fastapi import APIRouter
from ..core.deps import dbSession
from .schema import RegisterSchema, AuthResponse, LoginScheme, RefreshRequest
from .service import register_user, login_user, refresh_tokens

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register(userData : RegisterSchema , db : dbSession) -> AuthResponse:
    return register_user(userData,db)

@router.post("/login")
def login(userData : LoginScheme, db : dbSession) -> AuthResponse:
    return login_user(userData, db)

@router.post("/refresh")
def refresh(data : RefreshRequest, db : dbSession):
    return refresh_tokens(data.refresh_token, db)
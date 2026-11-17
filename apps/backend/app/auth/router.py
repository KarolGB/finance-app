from fastapi import APIRouter
from ..core.deps import dbSession
from .schema import RegisterSchema
from .service import register_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register(userData : RegisterSchema , db : dbSession):
    return register_user(userData,db)
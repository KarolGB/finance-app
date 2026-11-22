from fastapi import APIRouter, Depends
from app.core.deps import userDep
from .schema import UserSchema

router = APIRouter(prefix="/users", tags=["user"])

@router.get("/me", response_model=UserSchema)
def get_user(current_user : userDep):
    return current_user
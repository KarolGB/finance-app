from fastapi import Depends,HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from typing import Annotated
from sqlalchemy.orm import Session
from .database import get_db
from app.users.schema import UserSchema
from app.models.User import User
from .config import settings
from uuid import UUID

bearer_schema = HTTPBearer(auto_error=False)
dbSession = Annotated[Session,Depends(get_db)]

def get_current_user( db : dbSession, credentials : HTTPAuthorizationCredentials | None = Depends(bearer_schema)):
    unauthorized = HTTPException(
        status_code=401,
        detail="Invalid or missing authentication token",
    )
    if credentials is None:
        raise unauthorized
    token = credentials.credentials
    try:
        payload = jwt.decode(token,settings.secret_key,algorithms=settings.jwt_algorithm)
        raw_sub = payload.get("sub")
        if not raw_sub:
            raise unauthorized
        user_id = UUID(raw_sub)
    except:
        raise unauthorized
    
    user = db.query(User).where(User.id == user_id).first()
    if user is None:
        raise unauthorized
    return user

userDep = Annotated[User,Depends(get_current_user)]
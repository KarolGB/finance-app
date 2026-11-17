from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta,timezone
import jwt
from pwdlib import PasswordHash
from ..models.User import User
from ..models.RefreshToken import RefreshToken
from .schema import RegisterSchema, AuthResponse
from ..core.config import settings
import hashlib

password_hasher = PasswordHash.recommended()

def hash_string(str : str):
    return hashlib.sha256(str.encode("utf-8")).hexdigest()

def create_token(sub : str, expires_delta : timedelta):
    payload = {
        "sub" : sub,
        "exp" : datetime.now(timezone.utc) + expires_delta
    }
    return jwt.encode(payload,settings.secret_key,settings.jwt_algorithm)

def get_user_by_email(email : str, db : Session):
    user = db.query(User).where(User.email == email).scalar()
    if user:
        return user
    return None
    

def register_user(userData : RegisterSchema, db : Session) -> AuthResponse:
    user = get_user_by_email(userData.email,db)
    if user:
        raise HTTPException(status_code=400,detail="User With This Email Already Exists")
    password_hash = password_hasher.hash(userData.password)
    new_user = User(
        email = userData.email,
        first_name = userData.first_name,
        last_name = userData.last_name,
        password_hash = password_hash
    )
    db.add(new_user)
    try:
        db.flush()
        access_token = create_token(
            str(new_user.id),
            timedelta(minutes=settings.jwt_access_token_expire_minutes)
        )
        refresh_token = create_token(
            str(new_user.id),
            timedelta(days=settings.jwt_refresh_token_expire_days)
        )
        new_refresh_token = RefreshToken(
            user_id = new_user.id,
            token_hash = hash_string(refresh_token)
        )
        db.add(new_refresh_token)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(
            status_code=500, 
            detail="Could Not Complete Registration Process. Please Try Again."
        )
    return AuthResponse(access_token=access_token,refresh_token=refresh_token)
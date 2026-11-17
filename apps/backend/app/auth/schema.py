from pydantic import BaseModel, EmailStr

class RegisterSchema(BaseModel):
    email : EmailStr
    first_name : str
    last_name : str
    password : str
    
class LoginScheme(BaseModel):
    email : EmailStr
    password : str
    
class AuthResponse(BaseModel):
    access_token : str
    refresh_token : str
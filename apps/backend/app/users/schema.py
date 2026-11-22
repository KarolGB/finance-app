from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID

class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id : UUID
    email : EmailStr
    first_name : str
    last_name : str
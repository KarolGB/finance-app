from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
class WorkspaceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    currency: str
    role: str
    
class WorkspaceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    currency: str = Field(default="EUR", min_length=3, max_length=3)
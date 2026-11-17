from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session
from .database import get_db


dbSession = Annotated[Session,Depends(get_db)]
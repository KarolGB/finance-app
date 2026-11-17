from sqlalchemy import Column, String, Text, Boolean, Uuid, DateTime, func
from ..core.database import Base
from uuid import uuid7


class User(Base):
    __tablename__ = "users"
    
    id = Column(Uuid(as_uuid=True),primary_key=True,default=uuid7)
    email = Column(String(100),unique=True,nullable=False, index=True)
    first_name = Column(String(50),nullable=False)
    last_name = Column(String(100),nullable=False)
    password_hash = Column(Text,nullable=False)
    is_active = Column(Boolean,nullable=False, default=True)
    created_at = Column(DateTime(timezone=True),nullable=False, server_default=func.now())
    last_updated = Column(DateTime(timezone=True),nullable=False,server_default=func.now(), onupdate=func.now())
from sqlalchemy import Column, String, Uuid, DateTime, func, ForeignKey
from ..core.database import Base
from uuid import uuid7


class Workspace(Base):
    __tablename__ = "workspaces"
    
    id = Column(Uuid(as_uuid=True),primary_key=True,default=uuid7)
    name = Column(String(100),nullable=False)
    currency = Column(String(3), ForeignKey("currencies.code", ondelete="CASCADE"), nullable=False, default="EUR")
    created_by = Column(Uuid, ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True),nullable=False, server_default=func.now())
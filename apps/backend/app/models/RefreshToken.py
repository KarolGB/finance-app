from sqlalchemy import Column, String, Text, Boolean, Uuid, DateTime, func, Integer, ForeignKey
from ..core.database import Base

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    
    id = Column(Integer,primary_key=True, autoincrement=True)
    user_id = Column(Uuid, ForeignKey("users.id",ondelete="CASCADE"), nullable=False, index=True,)
    token_hash = Column(Text,nullable=False,index=True)
    is_revoked = Column(Boolean,nullable=False,default=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
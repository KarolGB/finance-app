from sqlalchemy import Column, String, Uuid, DateTime, func, ForeignKey, PrimaryKeyConstraint, CheckConstraint, Index
from ..core.database import Base

class WorkspaceMember(Base):
    __tablename__ = "workspace_members"
    
    workspace_id = Column(Uuid(as_uuid=True), ForeignKey("workspaces.id",ondelete="CASCADE"), nullable=False)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(50),nullable=False, default="member")
    invited_by = Column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    joined_at =  Column(DateTime(timezone=True),nullable=False, server_default=func.now())
    __table_args__ = (
        PrimaryKeyConstraint(
                "workspace_id","user_id"
            ),
        CheckConstraint(
            "role IN ('owner','admin','member','viewer')"
        )
    )
    
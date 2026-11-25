from sqlalchemy import Column, String, Uuid, DateTime, func, ForeignKey, SmallInteger, CheckConstraint, Boolean
from ..core.database import Base
from uuid import uuid7


class Currency(Base):
    __tablename__ = "currencies"
    
    code = Column(String(3),primary_key=True)
    name = Column(String(50), nullable=False)
    symbol = Column(String, nullable=False)
    decimals = Column(SmallInteger,nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    __table_args__ = (
        CheckConstraint(
            "decimals BETWEEN 0 AND 4"
        ),
    )
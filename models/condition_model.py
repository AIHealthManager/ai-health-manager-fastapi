import uuid

from sqlalchemy import Column, Text, TIMESTAMP, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID

from db import Base


class ConditionModel(Base):
    __tablename__ = "conditions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    event_date = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    name = Column(Text, nullable=False)               
    severity = Column(Text, nullable=True)           
    description = Column(Text, nullable=True)          
    outcome = Column(Text, nullable=True)              
    source = Column(Text, server_default="user", nullable=False) 

    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
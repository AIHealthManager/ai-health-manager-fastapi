import uuid

from sqlalchemy import Column, String, Text, TIMESTAMP, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from db import Base


class ConditionModel(Base):
    __tablename__ = "conditions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    condition_type = Column(String, nullable=False)     # e.g. "injury", "pain"
    name = Column(String, nullable=False)               # e.g. "broken leg"
    affected_area = Column(String, nullable=False)      # e.g. "leg"
    severity = Column(String, nullable=False)           # e.g. "moderate"
    description = Column(Text, nullable=True)           # Optional details

    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

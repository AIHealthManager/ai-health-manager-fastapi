import uuid

from sqlalchemy import Column, Date, String, Text, TIMESTAMP, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID

from db import Base


class VisitModel(Base):
    __tablename__ = "doctor_visits"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    visit_date = Column(String, nullable=False)
    doctor_name = Column(String(255), nullable=True)
    reason = Column(Text, nullable=False)
    diagnosis = Column(Text, nullable=False)
    notes = Column(Text, nullable=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

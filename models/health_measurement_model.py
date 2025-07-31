import uuid

from sqlalchemy import Column, Text, TIMESTAMP, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from db import Base


class HealthMeasurementModel(Base):
    __tablename__ = "health_measurements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    recorded_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    measurements = Column(Text, nullable=False)         # e.g. "BP: 120/80", "Weight: 150 lbs", "HR: 75 bpm"
    context = Column(Text, nullable=True)               # e.g. "after exercise", "morning reading", "at doctor's office"
    notes = Column(Text, nullable=True)                 # Additional observations or comments
    source = Column(Text, server_default="user", nullable=False)  # e.g. "user", "device", "doctor"

    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
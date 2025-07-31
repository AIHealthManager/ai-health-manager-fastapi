import uuid

from sqlalchemy import Column, Text, TIMESTAMP, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from db import Base


class MedicationIntakeModel(Base):
    __tablename__ = "medication_intakes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    intake_datetime = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    medication_name = Column(Text, nullable=False)      # e.g. "Ibuprofen", "Metformin", "Lisinopril"
    dosage = Column(Text, nullable=True)                # e.g. "200mg", "10mg twice daily", "1 tablet"
    reason = Column(Text, nullable=True)                # e.g. "headache", "diabetes management", "blood pressure"
    condition_id = Column(
        UUID(as_uuid=True), ForeignKey("conditions.id"), nullable=True
    )  # Link to related condition
    notes = Column(Text, nullable=True)                 # Additional notes or side effects
    source = Column(Text, server_default="user", nullable=False)  # e.g. "user", "prescription", "doctor"

    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
import uuid

from sqlalchemy import Column, Text, TIMESTAMP, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID

from db import Base


class DoctorVisitModel(Base):
    __tablename__ = "doctor_visits"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    visit_datetime = Column(TIMESTAMP, nullable=False)
    location = Column(Text, nullable=True)              # e.g. "City Hospital", "Dr. Smith's Clinic"
    doctor_name = Column(Text, nullable=True)           # e.g. "Dr. Sarah Johnson"
    referred_by = Column(Text, nullable=True)           # e.g. "Dr. Brown", "Emergency Room"
    reason = Column(Text, nullable=False)               # e.g. "routine checkup", "chest pain"
    observations = Column(Text, nullable=True)          # Doctor's observations during visit
    diagnosis = Column(Text, nullable=True)             # e.g. "hypertension", "viral infection"
    referred_to = Column(Text, nullable=True)           # e.g. "Cardiologist", "Physical Therapy"
    treatment = Column(Text, nullable=True)             # e.g. "prescribed antibiotics", "bed rest"
    intervention = Column(Text, nullable=True)          # e.g. "blood test", "X-ray", "surgery"
    user_feedback = Column(Text, nullable=True)         # Patient's thoughts on the visit

    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

import uuid

from sqlalchemy import Column, Text, TIMESTAMP, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from db import Base


class DiagnosticProcedureModel(Base):
    __tablename__ = "diagnostic_procedures"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    procedure_datetime = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    name = Column(Text, nullable=False)                 # e.g. "Complete Blood Count", "Chest X-Ray", "MRI Brain"
    type = Column(Text, server_default="lab", nullable=False)  # e.g. "lab", "imaging", "biopsy", "endoscopy"
    provider = Column(Text, nullable=True)              # e.g. "City Lab", "Dr. Johnson", "Radiology Dept"
    results = Column(Text, nullable=True)               # Test/procedure results and findings
    notes = Column(Text, nullable=True)                 # Additional notes or observations

    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    
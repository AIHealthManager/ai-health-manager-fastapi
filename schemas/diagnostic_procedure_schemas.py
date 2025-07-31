from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_serializer


class DiagnosticProcedureBase(BaseModel):
    """Base schema for diagnostic procedure data."""
    name: str
    provider: str | None = None
    results: str | None = None
    notes: str | None = None


class DiagnosticProcedureCreate(DiagnosticProcedureBase):
    """Schema for creating a new diagnostic procedure record."""
    procedure_datetime: datetime | None = None  # Optional, defaults to now() in DB
    type: str = "lab"  # Defaults to "lab" but can be overridden


class DiagnosticProcedure(DiagnosticProcedureBase):
    """Complete diagnostic procedure schema with all database fields."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    procedure_datetime: datetime
    type: str
    created_at: datetime

    @field_serializer("id", "user_id")
    def serialize_uuid(self, uuid_val: UUID, _info):
        return str(uuid_val)
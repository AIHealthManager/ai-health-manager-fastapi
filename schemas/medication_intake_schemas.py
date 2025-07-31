from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_serializer


class MedicationIntakeBase(BaseModel):
    """Base schema for medication intake data."""
    medication_name: str
    dosage: str | None = None
    reason: str | None = None
    condition_id: str | None = None
    notes: str | None = None


class MedicationIntakeCreate(MedicationIntakeBase):
    """Schema for creating a new medication intake record."""
    intake_datetime: datetime | None = None  # Optional, defaults to now() in DB
    source: str = "user"  # Defaults to "user" but can be overridden


class MedicationIntake(MedicationIntakeBase):
    """Complete medication intake schema with all database fields."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    intake_datetime: datetime
    source: str
    created_at: datetime

    @field_serializer("id", "user_id", "condition_id")
    def serialize_uuid(self, uuid_val: UUID | None, _info):
        return str(uuid_val) if uuid_val else None

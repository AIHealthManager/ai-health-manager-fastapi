from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_serializer


class HealthMeasurementBase(BaseModel):
    """Base schema for health measurement data."""
    measurements: str
    context: str | None = None
    notes: str | None = None


class HealthMeasurementCreate(HealthMeasurementBase):
    """Schema for creating a new health measurement record."""
    recorded_at: datetime | None = None  # Optional, defaults to now() in DB
    source: str = "user"  # Defaults to "user" but can be overridden


class HealthMeasurement(HealthMeasurementBase):
    """Complete health measurement schema with all database fields."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    recorded_at: datetime
    source: str
    created_at: datetime

    @field_serializer("id", "user_id")
    def serialize_uuid(self, uuid_val: UUID, _info):
        return str(uuid_val)
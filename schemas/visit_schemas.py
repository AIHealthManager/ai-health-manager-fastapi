from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_serializer


class VisitBase(BaseModel):
    """Base schema for doctor visit data."""
    visit_datetime: datetime
    location: str | None = None
    doctor_name: str | None = None
    referred_by: str | None = None
    reason: str
    observations: str | None = None
    diagnosis: str | None = None
    referred_to: str | None = None
    treatment: str | None = None
    intervention: str | None = None
    user_feedback: str | None = None


class VisitCreate(VisitBase):
    """Schema for creating a new doctor visit record."""
    pass


class VisitUpdate(BaseModel):
    """Schema for updating an existing doctor visit record."""
    visit_datetime: datetime | None = None
    location: str | None = None
    doctor_name: str | None = None
    referred_by: str | None = None
    reason: str | None = None
    observations: str | None = None
    diagnosis: str | None = None
    referred_to: str | None = None
    treatment: str | None = None
    intervention: str | None = None
    user_feedback: str | None = None


class Visit(VisitBase):
    """Complete doctor visit schema with all database fields."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    @field_serializer("id", "user_id")
    def serialize_uuid(self, uuid_val: UUID, _info):
        return str(uuid_val)
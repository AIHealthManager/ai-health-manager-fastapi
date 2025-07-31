from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_serializer


class ConditionBase(BaseModel):
    """Base schema for condition data."""
    name: str
    severity: str | None = None
    description: str | None = None
    outcome: str | None = None


class ConditionCreate(ConditionBase):
    """Schema for creating a new condition record."""
    event_date: datetime | None = None  # Optional, defaults to now() in DB
    source: str = "user"  # Defaults to "user" but can be overridden


class Condition(ConditionBase):
    """Complete condition schema with all database fields."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    event_date: datetime
    source: str
    created_at: datetime

    @field_serializer("id", "user_id")
    def serialize_uuid(self, uuid_val: UUID, _info):
        return str(uuid_val)

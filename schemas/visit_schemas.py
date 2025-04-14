from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_serializer


class VisitBase(BaseModel):
    visit_date: str
    doctor_name: str
    reason: str
    diagnosis: str
    notes: str


class VisitCreate(VisitBase):
    pass


class Visit(VisitBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    @field_serializer('id')
    def serialize_id(self, id: UUID, _info):
        return str(id)
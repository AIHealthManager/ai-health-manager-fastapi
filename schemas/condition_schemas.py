from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_serializer


class ConditionBase(BaseModel):
    condition_type: str          
    name: str                      
    affected_area: str            
    severity: str                   
    description: str | None = None  


class ConditionCreate(ConditionBase):
    pass


class Condition(ConditionBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    created_at: datetime

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info):
        return str(id)



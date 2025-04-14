from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_serializer


class UserBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=150)
    last_name: str = Field(..., min_length=1, max_length=150)
    email: EmailStr = Field(..., min_length=1, max_length=255)
    # password: Optional[str] = Field(None, min_length=1, max_length=255)


class UserCreate(UserBase):
    pass


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    @field_serializer('id')
    def serialize_id(self, id: UUID, _info):
        return str(id)

from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_serializer


class ProfileBase(BaseModel):
    sex: str
    birth_date: str
    blood_type: str


class ProfileData(ProfileBase):
    pass


class Profile(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info):
        return str(id)

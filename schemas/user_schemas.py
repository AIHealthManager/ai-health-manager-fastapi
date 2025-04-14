from pydantic import BaseModel, ConfigDict, Field, EmailStr


class UserBase(BaseModel):
    username: str = Field(..., min_length=1, max_length=150)
    email: EmailStr = Field(..., min_length=1, max_length=255)
    password: str = Field(..., min_length=1, max_length=255)


class UserCreate(UserBase):
    pass


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

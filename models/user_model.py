import uuid

from sqlalchemy import Column, String, Boolean, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID

from db import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(100))
    phone_number = Column(String(20))
    is_active = Column(Boolean, default=True)
    last_login = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

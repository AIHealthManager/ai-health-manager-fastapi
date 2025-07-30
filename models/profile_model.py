import uuid

from sqlalchemy import Column, Date, String, TIMESTAMP, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID

from db import Base


class ProfileModel(Base):
    __tablename__ = "profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    sex = Column(String(10), nullable=True)
    birth_date = Column(Date, nullable=True)
    blood_type = Column(String(5), nullable=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

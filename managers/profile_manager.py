from uuid import UUID
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select

from schemas.profile_schemas import ProfileData, Profile
from models.profile_model import ProfileModel


class ProfileManager:
    @staticmethod
    async def update_user_profile(profile_data: ProfileData, profile_id: str, db: AsyncSession):
        stmt = update(ProfileModel).where(ProfileModel.id == profile_id).values(**profile_data)
        result = await db.execute(stmt)
        updated_profile = result.scalar_one()
        await db.commit()
        return Profile.model_validate(updated_profile) 


    @staticmethod
    async def insert_user_profile(profile_data: ProfileData, user_id: str, db: AsyncSession) -> Profile:
        profile = ProfileModel(**profile_data.model_dump(), user_id=UUID(user_id))
        db.add(profile)
        await db.commit()
        return Profile.model_validate(profile)


    @staticmethod
    async def select_user_profile(user_id: str, db: AsyncSession) -> Optional[Profile]:
        profile = (await db.execute(select(ProfileModel).where(ProfileModel.user_id == UUID(user_id)))).scalar_one_or_none()
        if not profile:
            return None
        
        return Profile.model_validate(profile)

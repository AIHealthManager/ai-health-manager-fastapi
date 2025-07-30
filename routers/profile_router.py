from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from managers.profile_manager import ProfileManager
from schemas.profile_schemas import Profile, ProfileData
from auth.token import get_current_user_id
from db import get_db


profile_router = APIRouter(prefix="/profiles")


@profile_router.put("/")
async def put_user_profile(
    profile_data: ProfileData,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    existing_user_profile = await ProfileManager.select_user_profile(user_id, db)
    if not existing_user_profile:
        created_user_profile = await ProfileManager.insert_user_profile(
            profile_data, user_id, db
        )
        return created_user_profile, 201

    updated_user_profile = await ProfileManager.update_user_profile(
        profile_data, str(existing_user_profile.id), db
    )
    return updated_user_profile


@profile_router.get("/", response_model=Profile)
async def get_user_profile(
    user_id: str = Depends(get_current_user_id), db: AsyncSession = Depends(get_db)
):
    user_profile = await ProfileManager.select_user_profile(user_id, db)

    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User profile is not found!"
        )

    return user_profile

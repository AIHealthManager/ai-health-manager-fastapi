from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound

from db import get_db
from auth.token import get_current_user_id
from managers.user_manager import UserManager
from schemas.user_schemas import User


user_router = APIRouter(prefix="/user")


@user_router.get("/", response_model=User)
async def get_user(
    user_id: str = Depends(get_current_user_id), db: AsyncSession = Depends(get_db)
):
    try:
        user = await UserManager.select_user_by_id(user_id, db)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User not found")

    return user

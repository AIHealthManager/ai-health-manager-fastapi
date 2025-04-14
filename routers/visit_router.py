from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.visit_schemas import VisitCreate, Visit
from managers.visit_manager import VisitManager
from auth.token import get_current_user_id
from db import get_db


visit_router = APIRouter(prefix="/visit")


@visit_router.post("/", response_model=Visit, status_code=status.HTTP_201_CREATED)
async def post_visit(
    visit_data: VisitCreate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    visit = await VisitManager.insert_visit(visit_data, user_id, db)
    return visit


@visit_router.get("/user-visits", response_model=list[Visit])
async def get_user_visits(
    user_id: str = Depends(get_current_user_id), db: AsyncSession = Depends(get_db)
):
    visits = await VisitManager.select_user_visits(user_id, db)
    return visits

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.visit_model import VisitModel
from schemas.visit_schemas import VisitCreate, Visit


class VisitManager:
    @staticmethod
    async def insert_visit(visit_data: VisitCreate, user_id: str, db: AsyncSession) -> Visit:
        visit = VisitModel(**visit_data.model_dump(), user_id=UUID(user_id))
        db.add(visit)
        await db.commit()
        return Visit.model_validate(visit)

    @staticmethod
    async def select_user_visits(user_id: str, db: AsyncSession) -> list[Visit]:
        visits = (await db.execute(select(VisitModel).where(VisitModel.user_id == UUID(user_id)))).scalars().all()
        return [Visit.model_validate(visit) for visit in visits]

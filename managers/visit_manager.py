from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from models.visit_model import VisitModel
from schemas.visit_schemas import VisitCreate, Visit


class VisitManager:
    @staticmethod
    async def insert_visit(visit_data: VisitCreate, user_id: str, db: AsyncSession) -> Visit:
        visit = VisitModel(**visit_data.model_dump(), user_id=UUID(user_id))
        db.add(visit)
        await db.commit()
        return Visit.model_validate(visit)

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from models.visit_model import DoctorVisitModel
from schemas.visit_schemas import VisitCreate, VisitUpdate, Visit


class VisitManager:
    @staticmethod
    async def insert_doctor_visit(
        visit_data: VisitCreate, user_id: str, db: AsyncSession
    ) -> Visit:
        """
        Insert a new doctor visit record into the database.
        
        Args:
            visit_data: The doctor visit data to insert
            user_id: The user's unique identifier
            db: Database session
            
        Returns:
            The created doctor visit record
        """
        visit = DoctorVisitModel(**visit_data.model_dump(), user_id=UUID(user_id))
        db.add(visit)
        await db.commit()
        await db.refresh(visit)
        return Visit.model_validate(visit)

    @staticmethod
    async def select_user_doctor_visits_by_user_id(
        user_id: str, db: AsyncSession
    ) -> list[Visit]:
        """
        Retrieve all doctor visits for a specific user, ordered by visit date (most recent first).
        
        Args:
            user_id: The user's unique identifier
            db: Database session
            
        Returns:
            List of all doctor visits for the user
        """
        visits = (
            (
                await db.execute(
                    select(DoctorVisitModel)
                    .where(DoctorVisitModel.user_id == UUID(user_id))
                    .order_by(DoctorVisitModel.visit_datetime.desc())
                )
            )
            .scalars()
            .all()
        )
        return [Visit.model_validate(visit) for visit in visits]

    @staticmethod
    async def update_doctor_visit(
        visit_id: str, visit_data: VisitUpdate, user_id: str, db: AsyncSession
    ) -> Visit | None:
        """
        Update an existing doctor visit record.
        
        Args:
            visit_id: The visit's unique identifier
            visit_data: The updated visit data
            user_id: The user's unique identifier (for security)
            db: Database session
            
        Returns:
            The updated doctor visit record, or None if not found
        """
        # Only update fields that are not None
        update_data = {k: v for k, v in visit_data.model_dump().items() if v is not None}
        
        if not update_data:
            return None
            
        await db.execute(
            update(DoctorVisitModel)
            .where(
                DoctorVisitModel.id == UUID(visit_id),
                DoctorVisitModel.user_id == UUID(user_id)
            )
            .values(**update_data)
        )
        await db.commit()
        
        # Fetch and return updated record
        result = await db.execute(
            select(DoctorVisitModel).where(
                DoctorVisitModel.id == UUID(visit_id),
                DoctorVisitModel.user_id == UUID(user_id)
            )
        )
        visit = result.scalar_one_or_none()
        return Visit.model_validate(visit) if visit else None
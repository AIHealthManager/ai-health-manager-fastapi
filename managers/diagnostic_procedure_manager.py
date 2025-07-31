from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.diagnostic_procedure_model import DiagnosticProcedureModel
from schemas.diagnostic_procedure_schemas import DiagnosticProcedureCreate, DiagnosticProcedure


class DiagnosticProcedureManager:
    @staticmethod
    async def insert_diagnostic_procedure(
        procedure_data: DiagnosticProcedureCreate, user_id: str, db: AsyncSession
    ) -> DiagnosticProcedure:
        """
        Insert a new diagnostic procedure record into the database.
        
        Args:
            procedure_data: The diagnostic procedure data to insert
            user_id: The user's unique identifier
            db: Database session
            
        Returns:
            The created diagnostic procedure record
        """
        procedure = DiagnosticProcedureModel(**procedure_data.model_dump(), user_id=UUID(user_id))
        db.add(procedure)
        await db.commit()
        await db.refresh(procedure)
        return DiagnosticProcedure.model_validate(procedure)

    @staticmethod
    async def select_user_diagnostic_procedures_by_user_id(
        user_id: str, db: AsyncSession
    ) -> list[DiagnosticProcedure]:
        """
        Retrieve all diagnostic procedures for a specific user, ordered by procedure date (most recent first).
        
        Args:
            user_id: The user's unique identifier
            db: Database session
            
        Returns:
            List of all diagnostic procedures for the user
        """
        procedures = (
            (
                await db.execute(
                    select(DiagnosticProcedureModel)
                    .where(DiagnosticProcedureModel.user_id == UUID(user_id))
                    .order_by(DiagnosticProcedureModel.procedure_datetime.desc())
                )
            )
            .scalars()
            .all()
        )
        return [DiagnosticProcedure.model_validate(procedure) for procedure in procedures]
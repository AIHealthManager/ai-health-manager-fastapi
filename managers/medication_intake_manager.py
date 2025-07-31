from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.medication_intake_model import MedicationIntakeModel
from schemas.medication_intake_schemas import MedicationIntakeCreate, MedicationIntake


class MedicationIntakeManager:
    @staticmethod
    async def insert_medication_intake(
        intake_data: MedicationIntakeCreate, user_id: str, db: AsyncSession
    ) -> MedicationIntake:
        """
        Insert a new medication intake record into the database.
        
        Args:
            intake_data: The medication intake data to insert
            user_id: The user's unique identifier
            db: Database session
            
        Returns:
            The created medication intake record
        """
        # Convert condition_id string to UUID if provided
        intake_dict = intake_data.model_dump()
        if intake_dict.get("condition_id"):
            intake_dict["condition_id"] = UUID(intake_dict["condition_id"])
        
        intake = MedicationIntakeModel(**intake_dict, user_id=UUID(user_id))
        db.add(intake)
        await db.commit()
        await db.refresh(intake)
        return MedicationIntake.model_validate(intake)

    @staticmethod
    async def select_user_medication_intakes_by_user_id(
        user_id: str, db: AsyncSession
    ) -> list[MedicationIntake]:
        """
        Retrieve all medication intakes for a specific user, ordered by intake time (most recent first).
        
        Args:
            user_id: The user's unique identifier
            db: Database session
            
        Returns:
            List of all medication intakes for the user
        """
        intakes = (
            (
                await db.execute(
                    select(MedicationIntakeModel)
                    .where(MedicationIntakeModel.user_id == UUID(user_id))
                    .order_by(MedicationIntakeModel.intake_datetime.desc())
                )
            )
            .scalars()
            .all()
        )
        return [MedicationIntake.model_validate(intake) for intake in intakes]

    @staticmethod
    async def select_medication_intakes_by_condition(
        condition_id: str, user_id: str, db: AsyncSession
    ) -> list[MedicationIntake]:
        """
        Retrieve all medication intakes for a specific condition.
        
        Args:
            condition_id: The condition's unique identifier
            user_id: The user's unique identifier (for security)
            db: Database session
            
        Returns:
            List of medication intakes for the specific condition
        """
        intakes = (
            (
                await db.execute(
                    select(MedicationIntakeModel)
                    .where(
                        MedicationIntakeModel.condition_id == UUID(condition_id),
                        MedicationIntakeModel.user_id == UUID(user_id)
                    )
                    .order_by(MedicationIntakeModel.intake_datetime.desc())
                )
            )
            .scalars()
            .all()
        )
        return [MedicationIntake.model_validate(intake) for intake in intakes]
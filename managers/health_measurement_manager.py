from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.health_measurement_model import HealthMeasurementModel
from schemas.health_measurement_schemas import HealthMeasurementCreate, HealthMeasurement


class HealthMeasurementManager:
    @staticmethod
    async def insert_health_measurement(
        measurement_data: HealthMeasurementCreate, user_id: str, db: AsyncSession
    ) -> HealthMeasurement:
        """
        Insert a new health measurement record into the database.
        
        Args:
            measurement_data: The health measurement data to insert
            user_id: The user's unique identifier
            db: Database session
            
        Returns:
            The created health measurement record
        """
        measurement = HealthMeasurementModel(**measurement_data.model_dump(), user_id=UUID(user_id))
        db.add(measurement)
        await db.commit()
        await db.refresh(measurement)
        return HealthMeasurement.model_validate(measurement)

    @staticmethod
    async def select_user_health_measurements_by_user_id(
        user_id: str, db: AsyncSession
    ) -> list[HealthMeasurement]:
        """
        Retrieve all health measurements for a specific user, ordered by recorded date (most recent first).
        
        Args:
            user_id: The user's unique identifier
            db: Database session
            
        Returns:
            List of all health measurements for the user
        """
        measurements = (
            (
                await db.execute(
                    select(HealthMeasurementModel)
                    .where(HealthMeasurementModel.user_id == UUID(user_id))
                    .order_by(HealthMeasurementModel.recorded_at.desc())
                )
            )
            .scalars()
            .all()
        )
        return [HealthMeasurement.model_validate(measurement) for measurement in measurements]
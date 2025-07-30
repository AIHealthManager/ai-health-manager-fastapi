from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models.condition_model import ConditionModel
from schemas.condition_schemas import ConditionCreate, Condition


class ConditionManager:
    @staticmethod
    async def insert_condition(
        condition_data: ConditionCreate, user_id: str, db: AsyncSession
    ) -> Condition:
        condition = ConditionModel(**condition_data.model_dump(), user_id=UUID(user_id))
        db.add(condition)
        await db.commit()
        await db.refresh(condition)
        return Condition.model_validate(condition)

    @staticmethod
    async def select_user_conditions_by_user_id(
        user_id: str, db: AsyncSession
    ) -> list[Condition]:
        conditions = (
            (
                await db.execute(
                    select(ConditionModel).where(ConditionModel.user_id == UUID(user_id))
                )
            )
            .scalars()
            .all()
        )
        return [Condition.model_validate(condition) for condition in conditions]

from agents import function_tool, RunContextWrapper

from ai.context import AgentContext
from managers.visit_manager import VisitManager
from managers.condition_manager import ConditionManager
from schemas.visit_schemas import VisitCreate, Visit
from schemas.condition_schemas import ConditionCreate, Condition


@function_tool
async def create_visit(wrapper: RunContextWrapper[AgentContext], visit_data: VisitCreate) -> Visit:
    """
    Creates a new medical visit record for a patient.

    This function is used by the AI to store a new visit entry in the user's health history.
    The visit includes details such as date, doctor name, reason for the visit, diagnosis, and any notes.

    Args:
        visit_data (VisitCreate): A structured object containing visit details such as:
            - visit_date (str): The date of the medical visit.
            - doctor_name (str): The name of the attending doctor.
            - reason (str): The reason for the visit (e.g., symptoms, concerns).
            - diagnosis (str): Any diagnosis given during the visit.
            - notes (str): Additional notes or comments from the visit.
        user_id (str): The unique identifier of the patient whose record is being updated.

    Returns:
        Visit: A Visit object representing the stored visit, including its unique ID.

    Usage:
        The AI should use this tool when a user wants to record a new health visit or update their health history.
    """
    return await VisitManager.insert_visit(visit_data, wrapper.context.user_id, wrapper.context.db)


@function_tool
async def report_condition(
    wrapper: RunContextWrapper[AgentContext],
    condition_data: ConditionCreate,
) -> Condition:
    """
    Records a user-reported health condition such as a symptom, injury, or illness.

    Use this when a user reports a health issue (e.g. "I have stomach pain", "I broke my arm", "I feel dizzy").

    Args:
        wrapper: The AI agent's execution context, including DB access.
        condition_data (ConditionCreate): Structured condition input containing:
            - condition_type: e.g., "injury", "illness", "pain"
            - name: e.g., "broken leg", "blurred vision"
            - affected_area: e.g., "leg", "eyes"
            - severity: e.g., "mild", "moderate", "severe"
            - description (optional): Extra user context
        user_id (str): The unique user identifier (UUID as a string)

    Returns:
        Condition: The stored condition record with ID and timestamp.
    """
    return await ConditionManager.insert_condition(condition_data, wrapper.context.user_id, wrapper.context.db)

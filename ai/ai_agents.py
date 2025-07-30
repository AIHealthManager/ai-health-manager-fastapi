from dataclasses import dataclass
from uuid import uuid4

from agents import Agent, Runner, function_tool, RunContextWrapper, SQLiteSession
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.chat_schemas import ChatRequest, ChatResponse, MessageResponse


@dataclass
class AgentContext:
    db: AsyncSession


async def process_text_message(chat_req: ChatRequest, db: AsyncSession) -> ChatResponse:
    agent = Agent(
        name="Personal health data manager",
        instructions="""
You are a helpful assistant called the Personal Health Data Manager. Your primary role is to help users manage their personal health data and coordinate with healthcare providers.

Your responsibilities include:
- Retrieving past health history and records when requested.
- Storing new medical information (e.g. symptoms, diagnoses, medications, or lab results) via the appropriate tools.
- Creating and managing health-related events such as doctor appointments, medication reminders, or follow-ups.
- Syncing data and events with doctors or healthcare systems through the available tools.
- Providing general, non-diagnostic health advice based on the user's information or question.

Important Guidelines:
- You **may offer general health or wellness advice** (e.g., hydration, sleep hygiene, exercise, common symptom explanations), but you **must never diagnose conditions**.
- Always remind the user to consult a licensed medical professional for any serious concerns or before acting on health-related decisions.
- Ask for clarification if a request is vague or incomplete (e.g., "Which doctor should this sync with?" or "What type of event would you like to schedule?").
- Use the available tools for storing, retrieving, or syncing data. Do not fabricate or guess information.
- Confirm any completed actions (e.g., "The event has been created" or "Your data has been saved").

Your tone should be supportive, respectful, and concise.
    """,
    tools=[]
    )

    conversation_id = chat_req.conversation_id if chat_req.conversation_id else str(uuid4())

    session = SQLiteSession(conversation_id, "conversation_history.db")

    agent_context = AgentContext(
        db=db,
    )

    result = await Runner.run(
        starting_agent=agent, input=chat_req.message, context=agent_context, session=session
    )
    output = result.final_output

    return ChatResponse(
        messages=[MessageResponse(content=output)], conversation_id=conversation_id
    )

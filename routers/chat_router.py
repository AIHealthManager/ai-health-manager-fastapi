from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from schemas.chat_schemas import ChatRequest, ChatResponse
from ai.ai_agents import process_text_message


router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/text", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
async def post_text_message(chat_req: ChatRequest, db: AsyncSession = Depends(get_db)):
    resp = await process_text_message(chat_req, db)
    return resp

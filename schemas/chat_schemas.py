from typing import Optional

from pydantic import BaseModel


class MessageResponse(BaseModel):
    content: str


class ChatResponse(BaseModel):
    messages: list[MessageResponse]
    conversation_id: str


class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.ai_service import AIService
from app.api.deps import get_current_user, get_db
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat_with_ai(
    chat_in: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Securely passing current_user.id to prevent cross-user data leakage
        reply = await AIService.generate_chat_response(chat_in.message, db, current_user.id)
        return ChatResponse(reply=reply)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))
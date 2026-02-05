from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest
from app.services.chat_service import ChatService

router = APIRouter()
chat_service = ChatService()

@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Request에 history 필드가 있다면 받아서 넘겨줄 수 있음 (현재 스키마엔 없음)
        ai_response = await chat_service.generate_response(request.message)
        return {"response": ai_response}

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500, detail=f"AI 응답 생성 중 오류 발생: {str(e)}"
        )
    


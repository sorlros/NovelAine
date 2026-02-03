from fastapi import APIRouter, HTTPException
from groq import AsyncGroq
import os
from dotenv import load_dotenv
from app.schemas.chat import ChatRequest

load_dotenv()

router = APIRouter()

client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))


@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "당신은 몰입형 인터랙티브 스토리텔링 플랫폼의 AI 스토리텔러입니다. 사용자의 선택에 따라 흥미롭고 감정적인 이야기를 전개하세요.",
                },
                {"role": "user", "content": request.message},
            ],
            temperature=0.8,
            max_tokens=1000,
        )

        ai_response = response.choices[0].message.content
        return {"response": ai_response}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"AI 응답 생성 중 오류 발생: {str(e)}"
        )

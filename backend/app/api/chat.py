from fastapi import APIRouter, HTTPException
from groq import AsyncGroq
import os
from dotenv import load_dotenv
from app.schemas.chat import ChatRequest
from app.schemas.models import ApiResponse

load_dotenv()

router = APIRouter()

client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))


@router.post("/chat", response_model=ApiResponse)
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
        return ApiResponse.ok(data={"response": ai_response})

    except Exception as e:
        return ApiResponse.fail(error=f"AI generation failed: {str(e)}")

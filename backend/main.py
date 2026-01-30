from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    massage: str

@app.get("/")
def read_root():
    return {"status": "서버가 정상적으로 작동중"}

@app.post("/chat")
async def chat(request: ChatRequest):
    # GPT API 연결 코드
    return {"response": f"AI 캐릭터: '{request.message}'"}


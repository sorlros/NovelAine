from fastapi import FastAPI
from dotenv import load_dotenv
from app.schemas.models import ApiResponse
from app.api.chat import router as chat_router
from app.api.stories import router as stories_router
from app.api.characters import router as characters_router
from app.api.scenes import router as scenes_router

load_dotenv()

app = FastAPI(title="NovelAIne API", version="0.1.0")


@app.get("/", response_model=ApiResponse)
def read_root():
    return ApiResponse.ok(data={"status": "Server is running", "version": "0.1.0"})


app.include_router(chat_router, prefix="/api")
app.include_router(stories_router, prefix="/api")
app.include_router(characters_router, prefix="/api")
app.include_router(scenes_router, prefix="/api")

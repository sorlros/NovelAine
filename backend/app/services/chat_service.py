from groq import AsyncGroq
import os
from typing import List, Dict
from app.services.rag_service import RagService
from app.services.memory_service import MemoryService

class ChatService:
    def __init__(self):
        self.client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
        self.rag_service = RagService()
        self.memory_service = MemoryService(max_buffer_size=10)

    async def generate_response(self, user_message: str, history: List[Dict[str, str]] = []) -> str:
        """
        RAG와 Memory가 결합된 최종 응답 생성 로직
        """
        # 1. RAG: 관련 기억 검색 (최적화: 키워드 감지 시에만 호출)
        rag_context = ""
        try:
            if self._should_trigger_rag(user_message):
                rag_context = await self.rag_service.search_relevant_context(user_message)
        except Exception as e:
            print(f"RAG Error: {e}") 
            # RAG 실패해도 대화는 진행

        # 2. System Prompt 구성
        base_system_prompt = (
            "당신은 몰입형 인터랙티브 스토리텔링 플랫폼 'NovelAIne'의 AI 스토리텔러입니다.\n"
            "사용자의 선택에 따라 흥미롭고 감정적인 이야기를 전개하세요.\n"
            "문체는 소설처럼 서술적이고 묘사가 풍부해야 합니다.\n"
        )
        
        if rag_context:
            base_system_prompt += f"\n[참고할 캐릭터/설정 정보]\n{rag_context}\n"
            
        # 3. Message 구성 (Memory 적용)
        # 현재 요청에 시스템 프롬프트가 없다면 추가
        current_messages = [{"role": "system", "content": base_system_prompt}]
        
        # 이전 기록 추가 (User가 보낸 history가 있다면)
        if history:
            current_messages.extend(self.memory_service.format_history(history))
            
        # 현재 사용자 메시지 추가
        current_messages.append({"role": "user", "content": user_message})

        # 4. LLM 호출 (Groq Llama 3.3)
        response = await self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=current_messages,
            temperature=0.8,
            max_tokens=1000,
        )
        
        return response.choices[0].message.content

    def _should_trigger_rag(self, message: str) -> bool:
        """
        RAG 호출 여부를 결정합니다.
        모든 대화에 RAG를 쓰면 느리고 비싸므로, '질문'이나 '명사'가 있을 때만 호출합니다.
        """
        # 1. 명백한 질문
        if "?" in message or "누구" in message or "어떤" in message or "왜" in message:
            return True
        
        # 2. 길이가 긴 문장 (복잡한 묘사나 지시일 가능성)
        if len(message) > 20:
            return True
            
        return False

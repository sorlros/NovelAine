from typing import List, Dict

class MemoryService:
    def __init__(self, max_buffer_size: int = 10):
        # 실무에서는 Redis나 DB에 저장해야 하지만, 
        # 지금은 간단히 메모리 내 리스트로 시뮬레이션 하거나,
        # DB의 user_progress나 choices 테이블을 조회하는 방식으로 구현해야 합니다.
        # 여기서는 "요청에 포함된 지난 대화"를 다루는 헬퍼 함수로 구성합니다.
        self.max_buffer_size = max_buffer_size

    def format_history(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        토큰 절약을 위해 최근 N개의 대화만 유지합니다.
        (추후 요약 기능 추가 가능)
        """
        if not messages:
            return []
            
        # 시스템 프롬프트는 유지하고, 나머지 대화 중 최근 N개만 슬라이싱
        system_msgs = [m for m in messages if m["role"] == "system"]
        chat_msgs = [m for m in messages if m["role"] != "system"]
        
        recent_chat = chat_msgs[-self.max_buffer_size:]
        
        return system_msgs + recent_chat

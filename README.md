# 📖 AI-Powered Interactive Storytelling Platform

> **"당신의 선택이 곧 이야기가 되고, AI가 그 장면을 그려냅니다."**
> 
> 본 프로젝트는 유저의 선택과 감정 변화에 따라 실시간으로 스토리, 이미지, BGM이 변화하는 **몰입형 AI 독서 서비스**입니다. Flutter와 FastAPI를 기반으로 최적화된 사용자 경험을 제공합니다.

---

## ✨ Key Features

### 🎨 Intelligent Scene Imaging
* **Custom Character Creation:** 유저가 직접 이미지를 업로드하거나, 특정 화풍(Style)을 선택하여 주인공의 외형을 정의할 수 있습니다.
* **Smart Generation Scoring:** 모든 장면에 생성 비용(Token)을 낭비하지 않습니다. 스토리의 **감정 고조화**와 **서사적 중요도**를 점수화하여 임계값 이상인 주요 장면에서만 이미지를 생성합니다.
* **Character Consistency (RAG):** 캐릭터의 성장 배경, 성격, 프로필을 Vector DB(RAG)로 관리하여 스토리 전반에 걸쳐 일관된 캐릭터 묘사를 유지합니다.

### 🎵 Dynamic Multimedia Environment
* **Contextual BGM:** 스토리의 분위기를 학습한 모델이 현재 장면에 맞는 저작권 프리 음악을 실시간으로 재생합니다.
* **Automatic Background Transition:** 장소 변화나 분위기에 맞춰 실사가 아닌, 서사적 몰입감을 극대화하는 일러스트 스타일의 배경으로 자동 전환됩니다.

### 📱 Advanced UI/UX for Readers
* **Interactive Input:** 스토리 전개 시와 대화 시를 구분하여 하단 입력창이 유동적으로 변화하는 애니메이션 UI를 제공합니다.
* **Emotion Floating Card:** 캐릭터의 현재 감정 상태를 상단 카드로 시각화하여 상호작용의 재미를 더합니다.
* **Immersive Typography:** 타이핑 효과(Typewriter Effect)와 독서 전용 폰트를 통해 실제 소설을 읽는 듯한 몰입감을 부여합니다.
* **Narrative Loading:** 단순한 스피너 대신 "이야기를 구성하는 중..."과 같은 서사적 로딩 UI를 도입했습니다.

### ⚡ Performance & Optimization
* **Offline First & Caching:** 서버 부하를 줄이기 위해 로컬 DB와 캐싱 로직을 활용, 이전에 읽은 장면은 데이터 소모 없이 즉시 로드됩니다.
* **FastAPI Backend:** 비동기 처리를 통해 AI 모델의 응답 대기 시간을 최소화했습니다.

---

## 🛠 Tech Stack

### Frontend
<p>
  <img src="https://img.shields.io/badge/Flutter-02569B?style=for-the-badge&logo=Flutter&logoColor=white"/>
  <img src="https://img.shields.io/badge/Dart-0175C2?style=for-the-badge&logo=Dart&logoColor=white"/>
</p>

### Backend
<p>
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white"/>
</p>

### AI & Design Assets
* **LLM:** GPT-4o / Claude 3.5 Sonnet
* **Image Gen:** Stable Diffusion / Midjourney API
* **Icons:** Lucide Icons / Material Symbols
* **Vector DB:** Pinecone / Chroma (for RAG)

---

## 🏗 System Architecture

*사용자 입력 → FastAPI (비동기 처리) → LLM (스토리 생성 & 감정 분석) → Scoring Logic → Image/BGM Generation → Flutter UI 렌더링*

---

## 📋 Roadmap
- [ ] 캐릭터 일관성 유지용 RAG 파이프라인 고도화
- [ ] 스토리 장르별 특화 폰트 라이브러리 추가
- [ ] 유저 간 스토리 공유 및 커뮤니티 기능 추가
- [ ] 멀티 엔딩 시스템 도입
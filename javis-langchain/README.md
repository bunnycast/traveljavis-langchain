# 🔍 BGE-M3 + Weaviate 기반 벡터 검색 시스템

이 프로젝트는 [BGE-M3 임베딩 모델](https://huggingface.co/BAAI/bge-m3)을 사용해 문장을 벡터로 임베딩하고,  
[Weaviate 벡터 DB](https://weaviate.io/)에 저장 및 검색하는 전체 파이프라인을 제공합니다.  
FastAPI를 통해 검색 API도 제공합니다.

---

## 🚀 프로젝트 구성

```
app/                       프로젝트 폴더
  app.py                   🔌 FastAPI 서버:  
  embedder.py              🤖 BGE-M3 임베딩 로직
  Dokcerfile                Dockerfile
  requirements.txt         FastAPI + transformers 의존성 라이브러리
docker-compose.yml         도커 빌드 파일 생성
```
---

## ✅ 사전 준비

### 1. Python 가상환경 설정

```bash
mkdir project-langchain
cd project-langchain
python3.11 -m venv langchain  # python3.11이 없다면 별도 설치 이후 실행
source langchain/bin/activate
```

### 2. 패키지 설치  

```bash
pip install -r requirements.txt
```

---

## 🚀 실행 순서

### 🐳 Weaviate 실행 (Docker)

```bash
docker compose up --build
```

### ⚙️ Python 파일 패키지 
```bash
python setup_weaviate.py  # 스키마 생성
python insert_docs.py # 문서 삽입
python search.py  # 유사도 검색 > 쿼리를 BGE-M3로 임베딩하고 Weaviate에서 가장 유사한 문서를 검색
```

---

## 🔌 API 서버 실행 (FastAPI)

```bash
uvicorn app:app --reload
```

### ✅ Langchain API 사용 예

#### [POST] /search 
> 질의문을 임베딩하고 유사 문서 검색
```
Content-Type: application/json

{
  "query": "벡터 데이터 저장소"
}
```

#### [POST] /insert
> 문서를 벡터화하여 Weaviate에 저장 (관리자용)
```
# request
[{
  "title": "LLM이란?",
  "content": "대규모 언어 모델은 다양한 NLP 작업에 사용된다."
}
]

# response
 {
  "status": "inserted",
  "title": "LLM이란?"
}
```

#### [POST] /init-schema 
> Weaviate 스키마 생성 (관리자용)
```json
{
  "status": "schema created or already exists"
}
```
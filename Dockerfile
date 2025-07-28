FROM python:3.11

WORKDIR /app

# 소스 코드 복사
COPY . .

# .env 파일 복사
COPY .env /app/.env

# Python 패키지 설치
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# uvicorn 실행
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
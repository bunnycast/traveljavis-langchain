# BGE-M3 임베딩 모델을 로드하고, 텍스트를 벡터로 변환하는 함수 정의
from transformers import AutoModel, AutoTokenizer
import torch

tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-m3")
model = AutoModel.from_pretrained("BAAI/bge-m3")

def embed(text: str) -> list:
    input_text = f"query: {text}"
    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        output = model(**inputs)
        embedding = output.last_hidden_state[:, 0]
    return embedding[0].tolist()
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from embedder import embed
import weaviate

app = FastAPI()

client = weaviate.Client(
    "http://weaviate:8080",
    startup_period=60
)

class SearchRequest(BaseModel):
    query: str

class InsertRequest(BaseModel):
    title: str
    content: str

class Document(BaseModel):
    title: str
    content: str


@app.post("/search")
def search(req: SearchRequest):
    vec = embed(req.query)
    result = client.query.get("Document", ["title", "content", "_additional {certainty}"])
    result = result.with_near_vector({"vector": vec}).with_limit(3).do()
    return result

@app.post("/init-schema")
def init_schema():
    schema = {
        "class": "Document",
        "vectorizer": "none",
        "properties": [
            {"name": "title", "dataType": ["text"]},
            {"name": "content", "dataType": ["text"]}
        ]
    }
    if not client.schema.contains({"classes": [{"class": "Document"}]}):
        client.schema.create_class(schema)
    return {"status": "schema created or already exists"}

@app.post("/insert")
def insert_batch(docs: List[Document]):
    for doc in docs:
        embedding = embed(doc.content)
        client.data_object.create(
            data_object={"title": doc.title, "content": doc.content},
            class_name="Document",
            vector=embedding
        )
    return {"status": "success", "count": len(docs)}

@app.get("/list")
def list_documents():
    response = client.query.get("Document", ["title", "content"]).do()
    # .with_limit(limit)    limit 필요한 경우

    docs = response.get("data", {}).get("Get", {}).get("Document", [])
    return docs
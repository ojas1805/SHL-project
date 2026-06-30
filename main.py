from fastapi import FastAPI
from retrieval import Retriever

app = FastAPI()

retriever = Retriever()

@app.get("/")
def home():
    return {"message": "SHL Recommender API is running"}

@app.get("/health")
def health():
    return "OK"

@app.get("/recommend")
def recommend(query: str):
    results = retriever.search(query)
    return {"recommendations": results}

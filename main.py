from fastapi import FastAPI
from retrieval import retrieve
from reranker import rerank

app = FastAPI(
    title="SHL Assessment Recommendation API"
)


@app.get("/")
def home():
    return {
        "message": "SHL Assessment Recommendation API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "OK"
    }


@app.get("/recommend")
def recommend(query: str):

    # Step 1: Semantic Retrieval
    results = retrieve(query, top_k=30)

    # Step 2: Hybrid Re-ranking
    results = rerank(results, query)

    recommendations = []

    for item in results[:10]:
        recommendations.append({
            "name": item.get("name"),
            "url": item.get("link"),
            "remote": item.get("remote"),
            "adaptive": item.get("adaptive"),
            "duration": item.get("duration"),
            "job_levels": item.get("job_levels"),
            "description": item.get("description"),
            "categories": item.get("keys")
        })

    return {
        "query": query,
        "recommendations": recommendations
    }
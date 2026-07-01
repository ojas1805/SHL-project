from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from retrieval import retrieve
from reranker import rerank

app = FastAPI(
    title="SHL Assessment Recommendation API"
)

class ChatRequest(BaseModel):
    message: str
    remote: Optional[str] = None
    max_duration: Optional[int] = None
    job_level: Optional[str] = None
    adaptive: Optional[str] = None


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


# -----------------------------
# Clarification Endpoint
# -----------------------------
@app.get("/clarify")
def clarify(query: str):

    q = query.lower()

    # Software roles
    if any(word in q for word in [
        "developer",
        "engineer",
        "programmer",
        "software"
    ]):
        technologies = [
            "python",
            "java",
            "rust",
            "c++",
            "c#",
            "javascript",
            "sql",
            "aws",
            "docker"
        ]

        if not any(t in q for t in technologies):
            return {
                "needs_clarification": True,
                "question": "Which programming language or technology are you hiring for? (Python, Java, Rust, C++, SQL, AWS, etc.)"
            }

    # Manager roles
    if "manager" in q:
        if not any(x in q for x in [
            "sales",
            "project",
            "engineering",
            "operations",
            "hr"
        ]):
            return {
                "needs_clarification": True,
                "question": "Which type of manager? (Sales, HR, Operations, Project, Engineering...)"
            }

    # Graduate roles
    if "graduate" in q:
        if not any(x in q for x in [
            "finance",
            "engineering",
            "marketing",
            "it"
        ]):
            return {
                "needs_clarification": True,
                "question": "Which field is the graduate role in? (Finance, IT, Engineering, Marketing...)"
            }

    # Analyst roles
    if "analyst" in q:
        if not any(x in q for x in [
            "financial",
            "business",
            "data",
            "security"
        ]):
            return {
                "needs_clarification": True,
                "question": "What kind of analyst role? (Business, Financial, Data, Security...)"
            }

    return {
        "needs_clarification": False,
        "question": None
    }


# -----------------------------
# Recommendation Endpoint
# -----------------------------
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

@app.get("/refine")
def refine(
    query: str,
    remote: str = None,
    max_duration: int = None,
    job_level: str = None,
    adaptive: str = None
):

    # Retrieve and rerank results
    results = retrieve(query, top_k=50)
    results = rerank(results, query)

    filtered = []

    for item in results:

        # Filter by remote
        if remote:
            if item.get("remote", "").lower() != remote.lower():
                continue

        # Filter by adaptive
        if adaptive:
            if item.get("adaptive", "").lower() != adaptive.lower():
                continue

        # Filter by job level
        if job_level:
            if job_level not in item.get("job_levels", []):
                continue

        # Filter by duration
        if max_duration:

            duration = item.get("duration", "")

            digits = "".join(ch for ch in duration if ch.isdigit())

            if digits:
                if int(digits) > max_duration:
                    continue

        filtered.append(item)

    recommendations = []

    for item in filtered[:10]:
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
        "filters": {
            "remote": remote,
            "max_duration": max_duration,
            "job_level": job_level,
            "adaptive": adaptive
        },
        "recommendations": recommendations
    }

# -----------------------------
# Compare Assessments Endpoint
# -----------------------------
@app.get("/compare")
def compare(
    assessment1: str,
    assessment2: str
):

    catalog = retrieve("", top_k=500)

    item1 = None
    item2 = None

    for item in catalog:
        if item.get("name", "").lower() == assessment1.lower():
            item1 = item

        if item.get("name", "").lower() == assessment2.lower():
            item2 = item

    if item1 is None or item2 is None:
        return {
            "error": "One or both assessment names not found."
        }

    return {
        "assessment_1": {
            "name": item1.get("name"),
            "duration": item1.get("duration"),
            "remote": item1.get("remote"),
            "adaptive": item1.get("adaptive"),
            "job_levels": item1.get("job_levels"),
            "categories": item1.get("keys"),
            "description": item1.get("description"),
            "url": item1.get("link")
        },
        "assessment_2": {
            "name": item2.get("name"),
            "duration": item2.get("duration"),
            "remote": item2.get("remote"),
            "adaptive": item2.get("adaptive"),
            "job_levels": item2.get("job_levels"),
            "categories": item2.get("keys"),
            "description": item2.get("description"),
            "url": item2.get("link")
        }
    }

@app.post("/chat")
def chat(request: ChatRequest):

    query = request.message

    # ---------- Clarification ----------
    clarification = clarify(query)

    if clarification["needs_clarification"]:
        return {
            "type": "clarification",
            "response": clarification["question"]
        }

    # ---------- Recommendation ----------
    results = retrieve(query, top_k=50)
    results = rerank(results, query)

    filtered = []

    for item in results:

        if request.remote:
            if item.get("remote", "").lower() != request.remote.lower():
                continue

        if request.adaptive:
            if item.get("adaptive", "").lower() != request.adaptive.lower():
                continue

        if request.job_level:
            if request.job_level not in item.get("job_levels", []):
                continue

        if request.max_duration:

            duration = item.get("duration", "")

            digits = "".join(c for c in duration if c.isdigit())

            if digits and int(digits) > request.max_duration:
                continue

        filtered.append(item)

    recommendations = []

    for item in filtered[:10]:
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
        "type": "recommendation",
        "query": query,
        "recommendations": recommendations
    }
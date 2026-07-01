import json
import re
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

print("Loading SHL catalog...")

with open("data/shl_catalog_fixed.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)


def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    return text


print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Loading precomputed embeddings...")
embeddings = np.load("data/catalog_embeddings.npy")

print("Retriever Ready!")


def metadata_score(item, query):
    score = 0

    q = query.lower()

    text = (
        item.get("name", "") + " " +
        item.get("description", "") + " " +
        " ".join(item.get("keys", []))
    ).lower()

    keywords = [
        "python", "java", "sql", "aws", "docker",
        "excel", "word", "sales", "graduate",
        "leadership", "customer", "finance",
        "health", "safety", "cloud", "linux"
    ]

    for word in keywords:
        if word in q and word in text:
            score += 0.15

    if "graduate" in q:
        if any("Graduate" in x for x in item.get("job_levels", [])):
            score += 0.3

    if "manager" in q or "leadership" in q:
        if any(
            x in item.get("job_levels", [])
            for x in ["Manager", "Director", "Executive"]
        ):
            score += 0.3

    if item.get("remote") == "yes":
        score += 0.05

    return score


def retrieve(query, top_k=10):

    query = preprocess(query)

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    )

    similarities = cosine_similarity(
        query_embedding,
        embeddings
    )[0]

    ranked = []

    for sim, item in zip(similarities, catalog):
        ranked.append(
            (sim + metadata_score(item, query), item)
        )

    ranked.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [item for _, item in ranked[:top_k]]
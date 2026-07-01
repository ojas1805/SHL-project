import json
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

print("Loading SHL catalog...")

with open("data/shl_catalog_fixed.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)


def preprocess(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    return text


documents = []

for item in catalog:
    text = f"""
    Name: {item.get('name', '')}
    Description: {item.get('description', '')}
    Categories: {' '.join(item.get('keys', []))}
    Job Levels: {' '.join(item.get('job_levels', []))}
    Duration: {item.get('duration', '')}
    Remote: {item.get('remote', '')}
    Adaptive: {item.get('adaptive', '')}
    """

    documents.append(preprocess(text))

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(
    documents,
    show_progress_bar=True,
    convert_to_numpy=True
)

print("Retriever Ready!")


def metadata_score(item, query):
    score = 0

    q = query.lower()

    name = item.get("name", "").lower()
    desc = item.get("description", "").lower()
    categories = " ".join(item.get("keys", [])).lower()
    text = name + " " + desc + " " + categories

    # Leadership
    if any(x in q for x in ["leadership", "leader", "executive", "director"]):
        if "leadership" in text:
            score += 0.8
        if "opq" in text:
            score += 0.5
        if "verify interactive g" in text:
            score += 0.4

    # Software
    if any(x in q for x in ["python", "java", "spring", "sql", "aws", "docker"]):
        for skill in ["python", "java", "spring", "sql", "aws", "docker", "rest"]:
            if skill in q and skill in text:
                score += 0.6

        if "automata" in text:
            score += 0.4

    # Office/Admin
    if any(x in q for x in ["excel", "word", "office", "admin"]):
        if any(k in text for k in ["excel", "word", "office"]):
            score += 0.7

    # Graduate
    if "graduate" in q:
        if "graduate" in text:
            score += 0.8
        if "verify interactive g" in text:
            score += 0.5
        if "opq" in text:
            score += 0.4

    # Sales
    if "sales" in q:
        if "sales" in text:
            score += 0.8
        if "global skills" in text:
            score += 0.7
        if "opq mq sales" in text:
            score += 0.6

    # Safety
    if any(x in q for x in ["plant", "safety", "chemical", "operator"]):
        if "dependability" in text:
            score += 0.8
        if "safety" in text:
            score += 0.8
        if "workplace health" in text:
            score += 0.6

    # Healthcare
    if any(x in q for x in ["health", "hipaa", "medical", "patient"]):
        if any(k in text for k in ["hipaa", "medical", "healthcare"]):
            score += 0.8
        if "opq" in text:
            score += 0.4
        if "dependability" in text:
            score += 0.4

    # Manager boost
    if "manager" in q:
        if any(level in item.get("job_levels", [])
               for level in ["Manager", "Director", "Executive"]):
            score += 0.3

    # Graduate boost
    if "graduate" in q:
        if "Graduate" in item.get("job_levels", []):
            score += 0.3

    # Remote boost
    if item.get("remote") == "yes":
        score += 0.05

    return score


def retrieve(query, top_k=10):

    processed_query = preprocess(query)

    query_embedding = model.encode(
        [processed_query],
        convert_to_numpy=True
    )

    similarities = cosine_similarity(
        query_embedding,
        embeddings
    )[0]

    ranked = []

    for similarity, item in zip(similarities, catalog):
        final_score = similarity + metadata_score(item, processed_query)
        ranked.append((final_score, item))

    ranked.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [item for _, item in ranked[:top_k]]
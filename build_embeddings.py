import json
import re
import numpy as np
from sentence_transformers import SentenceTransformer

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

print("Generating embeddings...")

embeddings = model.encode(
    documents,
    show_progress_bar=True,
    convert_to_numpy=True
)

np.save("data/catalog_embeddings.npy", embeddings)

print("Done!")
print("Saved to data/catalog_embeddings.npy")
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json

class Retriever:
    def __init__(self):
        print("Loading model...")

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        with open("data/shl_catalog.json") as f:
            self.data = json.load(f)

        self.texts = [
            item["name"] + " " + item["description"]
            for item in self.data
        ]

        self.embeddings = self.model.encode(self.texts)

        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(self.embeddings))

        print("Retriever ready!")

    def search(self, query, k=5):
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(query_embedding, k)

        results = [self.data[i] for i in indices[0]]
        return results

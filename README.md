# SHL Conversational Assessment Recommender

## Overview

This project is a conversational recommendation system that suggests the most relevant SHL assessments based on a hiring requirement or job description. I built it using FastAPI and a retrieval-based approach that combines semantic search with metadata-based reranking.

The goal was to recommend suitable assessments, ask follow-up questions when a query is too broad, allow users to refine their search, and compare different assessments.

---

## Features

- Semantic search using Sentence Transformers
- Hybrid ranking using embeddings and metadata
- Clarification questions for vague queries
- Recommendation refinement using filters
- Assessment comparison
- Conversational `/chat` endpoint
- FastAPI REST API
- Railway deployment

---

## Project Structure

```
SHL-project/
│
├── data/
│   ├── shl_catalog.json
│   ├── shl_catalog_fixed.json
│   └── catalog_embeddings.npy
│
├── main.py
├── retrieval.py
├── reranker.py
├── evaluation.py
├── build_embeddings.py
├── repair_catalog.py
├── requirements.txt
├── README.md
└── test_retrieval.py
```

---

## How it works

The recommendation process happens in two stages.

First, every SHL assessment is converted into an embedding using the **all-MiniLM-L6-v2** Sentence Transformer model. When a user enters a query, the query is embedded and compared with all assessment embeddings using cosine similarity.

The retrieved results are then reranked using metadata from the SHL catalog. For example, the reranking considers things like leadership keywords, technical skills, job level, remote availability, assessment duration, and other role-specific information. This helped improve recommendation quality compared to relying only on semantic similarity.

To make deployment faster, I precomputed the embeddings and stored them in `catalog_embeddings.npy` instead of generating them every time the application starts.

---

## API Endpoints

### GET `/health`

Checks whether the API is running.

### POST `/chat`

Main conversational endpoint.

Example:

```json
{
  "message": "Python developer with coding skills"
}
```

The API either asks a clarification question or returns recommended assessments.

### GET `/clarify`

Returns a clarification question if the query is too broad.

### GET `/recommend`

Returns the top assessment recommendations.

### GET `/refine`

Allows users to filter recommendations using:

- Remote availability
- Maximum duration
- Job level
- Adaptive testing

### GET `/compare`

Compares two SHL assessments using information from the catalog.

---

## Running the project

Clone the repository:

```bash
git clone https://github.com/ojas1805/SHL-project.git
cd SHL-project
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the API:

```bash
uvicorn main:app --reload
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## Deployment

The application is deployed on Railway.

Base URL

```
https://shl-project-production.up.railway.app
```

Swagger

```
https://shl-project-production.up.railway.app/docs
```

Health Check

```
https://shl-project-production.up.railway.app/health
```

---

## Evaluation

To check whether the recommendations were improving, I created an evaluation script (`evaluation.py`) using representative C1–C10-style queries.

The evaluation reports:

- Precision@5
- Precision@10
- Mean Reciprocal Rank (MRR)

I also manually reviewed the recommendations to make sure they matched the expected SHL assessments.

Run the evaluation using:

```bash
python evaluation.py
```

---

## Challenges

One challenge was that semantic search alone sometimes returned assessments that were relevant in meaning but not the best match for the job role. Adding metadata-based reranking made the recommendations much more consistent.

Another issue was deployment time. Initially, the application generated embeddings every time it started, which made Railway deployments slow. Precomputing the embeddings solved this problem.

---

## Technologies Used

- Python
- FastAPI
- Sentence Transformers
- scikit-learn
- NumPy
- Railway
- GitHub

---

## AI Assistance

I used ChatGPT (OpenAI) as a development assistant for discussing implementation ideas, debugging, and reviewing code. The final retrieval logic, hybrid reranking, API endpoints, testing, deployment, and evaluation were implemented, integrated, and validated by me.

---

## Author

**Ojas Singh**

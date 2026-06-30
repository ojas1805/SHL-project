from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "working"}

@app.get("/health")
def health():
    return "OK"

@app.get("/chat")
def chat(query: str):
    return {
        "response": f"Recommended results for: {query}"
    }
